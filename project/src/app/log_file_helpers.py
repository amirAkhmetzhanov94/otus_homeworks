import re
import os
from typing import Optional, Tuple, List

from src.app.logger import logger
from src.app.regex_helpers import generate_log_file_name_search_pattern


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


def find_log_file_name_and_date(config: dict) -> tuple[str, str]:
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
