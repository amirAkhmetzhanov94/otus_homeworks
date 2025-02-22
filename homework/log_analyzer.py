import os
import re
import json
import argparse
import logging
import structlog
from statistics import median
from datetime import datetime, timedelta
from typing import Optional, Tuple, List, Dict, TextIO


config = {
    "REPORT_SIZE": 1000,
    "REPORT_DIR": "./reports",
    "LOG_DIR": "./log",
    "TEMPLATE_FILE": "report.html",
    "LOG_FILE": None
}


logger = structlog.get_logger()


def configure_logging(log_file_path: Optional[str] = None):
    processors = [
        structlog.stdlib.filter_by_level,
        structlog.processors.JSONRenderer()
    ]

    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    if log_file_path:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(message)s",
            handlers=[
                logging.FileHandler(log_file_path),
                logging.StreamHandler()
            ]
        )
    else:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(message)s",
            handlers=[logging.StreamHandler()]
        )


def generate_search_pattern() -> re.Pattern:
    logger.info("Generating search pattern")
    return re.compile(r'\"([A-Z]+) (/[^\s]+) HTTP/1\.[01]\"\s.*\s(\d+\.\d+)$')


def generate_log_file_name_search_pattern() -> re.Pattern:
    logger.info("Generating log file name search pattern")
    return re.compile(r'nginx-access-ui\.log-\d{8}(\.gz)?')


def extract_log_data(log_line: str, regex_pattern: re.Pattern) -> Optional[Tuple[str, str]]:
    match = re.search(regex_pattern, log_line)
    if match:
        logger.debug(
            "Extracted log data",
            log_line=log_line,
            url=match.group(2),
            request_time=match.group(3)
        )
        return match.group(2), match.group(3)


def collect_log_file_names(log_folder: str) -> List[str]:
    logger.info("Collecting log file names")
    return [file_name for file_name in os.listdir(log_folder)]


def validate_log_file_names(log_file_names: list, pattern: re.Pattern) -> List[str]:
    logger.info("Validating log file names")
    return [file_name for file_name in log_file_names if pattern.match(file_name)]


def get_latest_log_file(log_folder: str, latest_date: str) -> str:
    logger.info("Getting latest log file", latest_date=latest_date)
    return f'{log_folder}/nginx-access-ui.log-{latest_date}'


def count_percentile(number_of_requests: float, total_count: float) -> float:
    return (number_of_requests / total_count) * 100


def find_log_file_name_and_date() -> tuple[str, str]:
    file_name_search_pattern = generate_log_file_name_search_pattern()
    log_file_names = collect_log_file_names(config.get('LOG_DIR'))
    validated_log_files = validate_log_file_names(log_file_names, file_name_search_pattern)
    log_file_dates = [file_date.split('-')[-1] for file_date in validated_log_files]

    if not log_file_dates:
        logger.warning("No log files found in the log directory")
        return

    latest_log_file_date = max(log_file_dates)
    log_file_name = get_latest_log_file(config.get('LOG_DIR'), latest_log_file_date)
    return log_file_name, latest_log_file_date


def count_total(requests_data: dict, key: str) -> float:
    count_array = []
    for request in requests_data.values():
        if isinstance(request[key], list):
            count_array.append(sum(request[key]))
            continue
        count_array.append(request[key])
    return sum(count_array)


def generate_percentiles_report(
    requests_data: dict,
    key_to_count: str,
    total_count: float
) -> Dict[str, float]:
    percentiles = {}
    for url, data in requests_data.items():
        if isinstance(data[key_to_count], list):
            percentile = count_percentile(sum(data[key_to_count]), total_count)
            percentiles[url] = percentile
            continue
        percentile = count_percentile(data[key_to_count], total_count)
        percentiles[url] = percentile
    return percentiles


def collect_request_data(log_data: list) -> dict:
    request_data = {}
    for data in log_data:
        if data:
            url, request_time = data
            if url in request_data:
                request_data[url]['count'] += 1
                request_data[url]['times'].append(float(request_time))
                continue
            request_data[url] = {'count': 1, 'times': [float(request_time)]}
    return request_data


def count_time_statistics(request_time_array: dict) -> dict:
    time_stats = {}
    for url, data in request_time_array.items():
        time_stats[url] = {
            'sum': sum(data['times']),
            'avg': sum(data['times']) / len(data['times']),
            'max': max(data['times']),
            'med': median(data['times'])
        }
    return time_stats


def generate_report_data(
    time_stats: dict,
    requests_data: dict,
    time_percentiles: Dict[str, float],
    count_percentiles: Dict[str, float]
):
    reports = []
    for url, data in requests_data.items():
        report = {
            'count': data['count'],
            'url': url,
            'count_perc': float(f'{count_percentiles.get(url):.10f}'),
            'time_perc': float(f'{time_percentiles.get(url):.10f}'),
            'time_sum': float(f'{time_stats[url]["sum"]:.10f}'),
            'time_avg': float(f'{time_stats[url]["avg"]:.10f}'),
            'time_med': float(f'{time_stats[url]["med"]:.10f}'),
            'time_max': float(f'{time_stats[url]["max"]:.10f}')
        }
        reports.append(report)
    return reports


def generate_reports(log_file: TextIO, search_pattern: re.Pattern):
    log_data = [extract_log_data(line, search_pattern) for line in log_file.readlines()]
    requests_data = collect_request_data(log_data)

    requests_total_count = count_total(requests_data, 'count')
    requests_total_times_count = count_total(requests_data, 'times')

    requests_count_percentiles = generate_percentiles_report(
        requests_data,
        'count',
        requests_total_count
    )
    requests_time_percentiles = generate_percentiles_report(
        requests_data,
        'times',
        requests_total_times_count
    )

    time_statistics = count_time_statistics(requests_data)

    reports = generate_report_data(
        time_statistics,
        requests_data,
        requests_count_percentiles,
        requests_time_percentiles
    )
    return reports


def generate_report_file_name(file_date: str):
    try:
        date = datetime.strptime(file_date, "%Y%m%d")
    except ValueError:
        year, month = int(file_date[:4]), int(file_date[4:6])
        date = datetime(year, month, 1) + timedelta(days=31)
        date = date.replace(day=1) - timedelta(days=1)

    return f"/report-{date.strftime('%Y.%m.%d')}.html"


def generate_report_file(reports: list, latest_log_file_date):
    report_file_name = generate_report_file_name(latest_log_file_date)

    with open(config.get('TEMPLATE_FILE'), "r", encoding="utf-8") as file:
        template_html = file.read()

    json_data = json.dumps(reports, indent=2, ensure_ascii=False)

    updated_html = template_html.replace("$table_json", json_data)

    output_path = config.get("REPORT_DIR") + report_file_name

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(updated_html)


def main():
    parser = argparse.ArgumentParser(
        prog='Log Analyzer'
    )
    parser.add_argument('--config', type=str)
    config_file_path = parser.parse_args()

    if config_file_path.config:
        try:
            with open(config_file_path.config, 'r') as conf:
                external_conf_data = json.loads(conf.read())
                config.update(external_conf_data)
                configure_logging(config.get("LOG_FILE"))

        except FileNotFoundError:
            logger.error("Config file not found", config_file_path=config_file_path.config)

    log_file_name, latest_date = find_log_file_name_and_date()

    search_pattern = generate_search_pattern()

    logger.info("Starting log analysis", config=config)

    try:
        with open(log_file_name, 'r') as log_file:
            reports = generate_reports(log_file=log_file, search_pattern=search_pattern)
            generate_report_file(reports, latest_date)
    except FileNotFoundError:
        logger.error("Log file not found", config_file_path=config_file_path.config)

    logger.info("Log analysis completed")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except BaseException as e:
        logger.error("Unexpected error occurred", exc_info=True)
