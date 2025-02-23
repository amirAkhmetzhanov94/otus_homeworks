import re

from src.app.log_file_helpers import extract_log_data, collect_log_file_names, validate_log_file_names, get_latest_log_file, find_log_file_name_and_date, generate_log_file_name_search_pattern

from unittest.mock import patch


def test_extract_log_data_valid():
    log_line = '127.0.0.1 - - [10/Oct/2023:13:55:36 +0000] "GET /api/v1/resource HTTP/1.1" 200 1234 "-" "curl/7.64.1" 0.005'
    regex_pattern = re.compile(r'\"([A-Z]+) (/[^\s]+) HTTP/1\.[01]\"\s.*\s(\d+\.\d+)$')
    result = extract_log_data(log_line, regex_pattern)
    assert result == ('/api/v1/resource', '0.005')


def test_extract_log_data_invalid():
    log_line = 'Invalid log line format'
    regex_pattern = re.compile(r'\"([A-Z]+) (/[^\s]+) HTTP/1\.[01]\"\s.*\s(\d+\.\d+)$')
    result = extract_log_data(log_line, regex_pattern)
    assert result is None


@patch('os.listdir')
def test_collect_log_file_names(mock_listdir):
    mock_listdir.return_value = ['nginx-access-ui.log-20231010', 'nginx-access-ui.log-20231009.gz']
    log_folder = '/path/to/logs'
    result = collect_log_file_names(log_folder)
    assert result == ['nginx-access-ui.log-20231010', 'nginx-access-ui.log-20231009.gz']


@patch('os.listdir')
def test_collect_log_file_names_empty_directory(mock_listdir):
    mock_listdir.return_value = []
    log_folder = '/path/to/logs'
    result = collect_log_file_names(log_folder)
    assert result == []


def test_validate_log_file_names_valid():
    log_file_names = ['nginx-access-ui.log-20231010.gz', 'nginx-access-ui.log-20231009.gz', 'other-file.txt']
    pattern = re.compile(r'^nginx-access-ui\.log-\d{8}\.gz$')
    result = validate_log_file_names(log_file_names, pattern)
    assert result == ['nginx-access-ui.log-20231010.gz', 'nginx-access-ui.log-20231009.gz']


def test_validate_log_file_names_invalid():
    log_file_names = ['nginx-access-ui.log-20231010.gz', 'invalid-log-file', 'other-file.txt']
    pattern = re.compile(r'^nginx-access-ui\.log-\d{8}\.gz$')
    result = validate_log_file_names(log_file_names, pattern)
    assert result == ['nginx-access-ui.log-20231010.gz']


def test_get_latest_log_file():
    log_folder = '/path/to/logs'
    latest_date = '20231010'
    result = get_latest_log_file(log_folder, latest_date)
    assert result == '/path/to/logs/nginx-access-ui.log-20231010'


@patch('src.app.log_file_helpers.collect_log_file_names')
@patch('src.app.log_file_helpers.validate_log_file_names')
@patch('src.app.log_file_helpers.get_latest_log_file')
def test_find_log_file_name_and_date(mock_get_latest_log_file, mock_validate_log_file_names, mock_collect_log_file_names):
    config = {'LOG_DIR': '/path/to/logs'}
    mock_collect_log_file_names.return_value = ['nginx-access-ui.log-20231010.gz', 'nginx-access-ui.log-20231009.gz']
    mock_validate_log_file_names.return_value = ['nginx-access-ui.log-20231010.gz', 'nginx-access-ui.log-20231009.gz']
    mock_get_latest_log_file.return_value = '/path/to/logs/nginx-access-ui.log-20231010'

    result = find_log_file_name_and_date(config)
    assert result == ('/path/to/logs/nginx-access-ui.log-20231010', '20231010.gz')


@patch('src.app.log_file_helpers.collect_log_file_names')
@patch('src.app.log_file_helpers.validate_log_file_names')
def test_find_log_file_name_and_date_no_logs(mock_validate_log_file_names, mock_collect_log_file_names):
    config = {'LOG_DIR': '/path/to/logs'}
    mock_collect_log_file_names.return_value = []
    mock_validate_log_file_names.return_value = []

    result = find_log_file_name_and_date(config)
    assert result is None