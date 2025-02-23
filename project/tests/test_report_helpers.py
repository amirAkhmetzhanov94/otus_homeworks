import re
from typing import List, Tuple

import pytest
from src.app.report_helpers import (
    collect_request_data,
    generate_percentiles_report,
    generate_report_data,
    generate_report_file_name,
    generate_reports,
)


def test_generate_percentiles_report_valid() -> None:
    requests_data = {
        "url1": {"count": 10, "times": [1.0, 2.0, 3.0]},
        "url2": {"count": 5, "times": [4.0, 5.0]},
    }
    total_count = 15
    result = generate_percentiles_report(
        requests_data,
        "count",
        total_count,
    )
    assert result == {
        "url1": 66.66666666666666,
        "url2": 33.33333333333333,
    }


def test_generate_percentiles_report_with_lists() -> None:
    requests_data = {
        "url1": {"count": [5, 5], "times": [1.0, 2.0, 3.0]},
        "url2": {"count": [3, 2], "times": [4.0, 5.0]},
    }
    total_count = 15
    result = generate_percentiles_report(
        requests_data,
        "count",
        total_count,
    )
    assert result == {
        "url1": 66.66666666666666,
        "url2": 33.33333333333333,
    }


def test_generate_percentiles_report_zero_total_count() -> None:
    requests_data = {"url1": {"count": 10}}
    total_count = 0
    with pytest.raises(ZeroDivisionError):
        generate_percentiles_report(requests_data, "count", total_count)


def test_collect_request_data_valid() -> None:
    log_data: List[Tuple[str, str]] = [
        ("url1", "1.0"),
        ("url2", "2.0"),
        ("url1", "3.0"),
    ]
    result = collect_request_data(log_data)
    expected_result = {
        "url1": {"count": 2, "times": [1.0, 3.0]},
        "url2": {"count": 1, "times": [2.0]},
    }
    assert result == expected_result


def test_collect_request_data_empty_log_data() -> None:
    log_data: List[Tuple[str, str]] = []
    result = collect_request_data(log_data)
    assert result == {}


def test_generate_report_data_valid() -> None:
    time_stats = {
        "url1": {"sum": 4.0, "avg": 2.0, "max": 3.0, "med": 2.0},
        "url2": {"sum": 9.0, "avg": 4.5, "max": 5.0, "med": 5.0},
    }
    requests_data = {
        "url1": {"count": 2, "times": [1.0, 3.0]},
        "url2": {"count": 1, "times": [4.0, 5.0]},
    }
    time_percentiles = {"url1": 40.0, "url2": 60.0}
    count_percentiles = {"url1": 66.67, "url2": 33.33}
    result = generate_report_data(
        time_stats, requests_data, time_percentiles, count_percentiles
    )
    expected_result = [
        {
            "count": 2,
            "url": "url1",
            "count_perc": 66.67,
            "time_perc": 40.0,
            "time_sum": 4.0,
            "time_avg": 2.0,
            "time_med": 2.0,
            "time_max": 3.0,
        },
        {
            "count": 1,
            "url": "url2",
            "count_perc": 33.33,
            "time_perc": 60.0,
            "time_sum": 9.0,
            "time_avg": 4.5,
            "time_med": 5.0,
            "time_max": 5.0,
        },
    ]
    assert result == expected_result


def test_generate_report_file_name_valid() -> None:
    file_date = "20231010"
    result = generate_report_file_name(file_date)
    assert result == "/report-2023.10.10.html"


def test_generate_report_file_name_invalid_format() -> None:
    file_date = "202310"  # Missing day
    result = generate_report_file_name(file_date)
    assert result == "/report-2023.10.31.html"


def test_generate_reports_valid(mocker) -> None:
    mock_log_lines = [
        "127.0.0.1 - - [10/Oct/2023:13:55:36 +0000] "
        '"GET /url1 HTTP/1.1" 200 1234 '
        '"-" "curl/7.64.1" 1.0',
        "127.0.0.1 - - [10/Oct/2023:13:55:37 +0000] "
        '"GET /url2 HTTP/1.1" 200 1234 '
        '"-" "curl/7.64.1" 2.0',
        "127.0.0.1 - - [10/Oct/2023:13:55:38 +0000] "
        '"GET /url1 HTTP/1.1" 200 1234 '
        '"-" "curl/7.64.1" 3.0',
    ]
    search_pattern = re.compile(r"\"([A-Z]+) (/[^\s]+) HTTP/1\.[01]\"\s.*\s(\d+\.\d+)$")
    mocker.patch("builtins.open", mocker.mock_open(read_data="\n".join(mock_log_lines)))
    mock_log_file = open("mock_log_file")
    result = generate_reports(mock_log_file, search_pattern)
    assert len(result) == 2
    assert result[0]["url"] == "/url1"
    assert result[1]["url"] == "/url2"
