import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, TextIO, Union

from src.app.log_file_helpers import extract_log_data
from src.app.math_helpers import count_percentile, count_time_statistics, count_total


def generate_percentiles_report(
    requests_data: dict, key_to_count: str, total_count: float
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


def collect_request_data(
    log_data: list,
) -> Dict[str, Dict[str, Union[int, List[float]]]]:
    request_data: dict = {}
    for data in log_data:
        if data:
            url, request_time = data
            if url in request_data:
                request_data[url]["count"] += 1
                request_data[url]["times"].append(float(request_time))
                continue
            request_data[url] = {"count": 1, "times": [float(request_time)]}
    return request_data


def generate_report_data(
    time_stats: dict,
    requests_data: dict,
    time_percentiles: Dict[str, float],
    count_percentiles: Dict[str, float],
):
    reports = []
    for url, data in requests_data.items():
        report = {
            "count": data["count"],
            "url": url,
            "count_perc": float(f"{count_percentiles.get(url):.10f}"),
            "time_perc": float(f"{time_percentiles.get(url):.10f}"),
            "time_sum": float(f'{time_stats[url]["sum"]:.10f}'),
            "time_avg": float(f'{time_stats[url]["avg"]:.10f}'),
            "time_med": float(f'{time_stats[url]["med"]:.10f}'),
            "time_max": float(f'{time_stats[url]["max"]:.10f}'),
        }
        reports.append(report)
    return reports


def generate_reports(log_file: TextIO, search_pattern: re.Pattern):
    log_data = [extract_log_data(line, search_pattern) for line in log_file.readlines()]
    requests_data = collect_request_data(log_data)

    requests_total_count = count_total(requests_data, "count")
    requests_total_times_count = count_total(requests_data, "times")

    requests_count_percentiles = generate_percentiles_report(
        requests_data, "count", requests_total_count
    )
    requests_time_percentiles = generate_percentiles_report(
        requests_data, "times", requests_total_times_count
    )

    time_statistics = count_time_statistics(requests_data)

    reports = generate_report_data(
        time_statistics,
        requests_data,
        requests_count_percentiles,
        requests_time_percentiles,
    )
    return reports


def generate_report_file_name(file_date: str) -> str:
    try:
        date = datetime.strptime(file_date, "%Y%m%d")
    except ValueError:
        year, month = int(file_date[:4]), int(file_date[4:6])
        date = datetime(year, month, 1) + timedelta(days=31)
        date = date.replace(day=1) - timedelta(days=1)
    return f"/report-{date.strftime('%Y.%m.%d')}.html"


def generate_report_file(reports: list, config: dict, latest_log_file_date: str) -> None:
    report_file_name = generate_report_file_name(latest_log_file_date)

    with open(config["TEMPLATE_FILE"], "r", encoding="utf-8") as file:
        template_html = file.read()

    json_data = json.dumps(reports, indent=2, ensure_ascii=False)

    updated_html = template_html.replace("$table_json", json_data)

    output_path = config.get("REPORT_DIR", "") + report_file_name

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(updated_html)
