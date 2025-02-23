import pytest
from src.app.math_helpers import count_percentile, count_total, count_time_statistics


def test_count_percentile_valid():
    result = count_percentile(50, 100)
    assert result == 50.0


def test_count_percentile_zero_requests():
    result = count_percentile(0, 100)
    assert result == 0.0


def test_count_percentile_zero_total_count():
    with pytest.raises(ZeroDivisionError):
        count_percentile(50, 0)


def test_count_total_single_values():
    requests_data = {
        'request1': {'key': 10},
        'request2': {'key': 20},
        'request3': {'key': 30}
    }
    result = count_total(requests_data, 'key')
    assert result == 60


def test_count_total_list_values():
    requests_data = {
        'request1': {'key': [10, 20]},
        'request2': {'key': [30, 40]},
        'request3': {'key': [50]}
    }
    result = count_total(requests_data, 'key')
    assert result == 150


def test_count_total_mixed_values():
    requests_data = {
        'request1': {'key': 10},
        'request2': {'key': [20, 30]},
        'request3': {'key': 40}
    }
    result = count_total(requests_data, 'key')
    assert result == 100


def test_count_total_empty_dict():
    requests_data = {}
    result = count_total(requests_data, 'key')
    assert result == 0


def test_count_time_statistics_valid():
    request_time_array = {
        'url1': {'times': [1.0, 2.0, 3.0]},
        'url2': {'times': [4.0, 5.0, 6.0]}
    }
    expected_result = {
        'url1': {'sum': 6.0, 'avg': 2.0, 'max': 3.0, 'med': 2.0},
        'url2': {'sum': 15.0, 'avg': 5.0, 'max': 6.0, 'med': 5.0}
    }
    result = count_time_statistics(request_time_array)
    assert result == expected_result


def test_count_time_statistics_single_url():
    request_time_array = {
        'url1': {'times': [1.0, 2.0, 3.0]}
    }
    expected_result = {
        'url1': {'sum': 6.0, 'avg': 2.0, 'max': 3.0, 'med': 2.0}
    }
    result = count_time_statistics(request_time_array)
    assert result == expected_result


def test_count_time_statistics_empty_dict():
    request_time_array = {}
    result = count_time_statistics(request_time_array)
    assert result == {}
