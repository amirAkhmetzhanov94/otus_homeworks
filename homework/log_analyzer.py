import os
import re
import json
from statistics import median
from datetime import datetime, timedelta
from typing import Optional, Tuple, List, Dict, TextIO

# log_format ui_short '$remote_addr  $remote_user $http_x_real_ip [$time_local] "$request" '
#                     '$status $body_bytes_sent "$http_referer" '
#                     '"$http_user_agent" "$http_x_forwarded_for" "$http_X_REQUEST_ID" "$http_X_RB_USER" '
#                     '$request_time';

config = {
    "REPORT_SIZE": 1000,
    "REPORT_DIR": "./reports",
    "LOG_DIR": "./log",
    "TEMPLATE_FILE": "report.html"
}


def generate_search_pattern() -> re.Pattern:
    return re.compile(r'\"([A-Z]+) (/[^\s]+) HTTP/1\.[01]\"\s.*\s(\d+\.\d+)$')


def extract_log_data(log_line: str, regex_pattern: re.Pattern) -> Optional[Tuple[str, str]]:
    match = re.search(regex_pattern, log_line)
    if match:
        return match.group(2), match.group(3)


def parse_log_file_dates(log_folder: str) -> List[str]:
    return [file_name.split('-')[-1] for file_name in os.listdir(log_folder)]


def get_latest_log_file(log_folder: str, latest_date: str) -> str:
    return f'{log_folder}/nginx-access-ui.log-{latest_date}'


def count_percentile(number_of_requests: float, total_count: float) -> float:
    return (number_of_requests / total_count) * 100


def count_total(requests_data: dict, key: str) -> float:
    count_array = []
    for request in requests_data.values():
        if isinstance(request[key], list):
            count_array.append(sum(request[key]))
            continue
        count_array.append(request[key])
    return sum(count_array)


def generate_percentiles_report(requests_data: dict, key_to_count: str, total_count: float) -> Dict[str, float]:
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
            'time_avg':  float(f'{time_stats[url]["avg"]:.10f}'),
            'time_med':  float(f'{time_stats[url]["med"]:.10f}'),
            'time_max': float(f'{time_stats[url]["max"]:.10f}')
        }
        reports.append(report)
    return reports


def generate_reports(log_file: TextIO, search_pattern: re.Pattern):
    log_data = [extract_log_data(line, search_pattern) for line in log_file.readlines()]
    requests_data = collect_request_data(log_data)

    requests_total_count = count_total(requests_data, 'count')
    requests_total_times_count = count_total(requests_data, 'times')

    requests_count_percentiles = generate_percentiles_report(requests_data, 'count', requests_total_count)
    requests_time_percentiles = generate_percentiles_report(requests_data, 'times', requests_total_times_count)

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
    log_file_dates = parse_log_file_dates(config.get('LOG_DIR'))
    if not log_file_dates:
        return

    latest_log_file_date = max(log_file_dates)

    log_file_name = get_latest_log_file(config.get('LOG_DIR'), latest_log_file_date)

    search_pattern = generate_search_pattern()

    with open(log_file_name, 'r') as log_file:
        reports = generate_reports(log_file=log_file, search_pattern=search_pattern)
    generate_report_file(reports, latest_log_file_date)


if __name__ == "__main__":
    main()
