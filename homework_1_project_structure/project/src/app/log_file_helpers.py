import os
import re
from typing import Dict, List, Optional, Tuple

from src.app.logger import logger
from src.app.regex_helpers import generate_log_file_name_search_pattern


def extract_log_data(
    log_line: str, regex_pattern: re.Pattern[str]
) -> Optional[Tuple[str, str]]:
    match = re.search(regex_pattern, log_line)
    if match:
        logger.debug(
            "Extracted log data",
            log_line=log_line,
            url=match.group(2),
            request_time=match.group(3),
        )
        return match.group(2), match.group(3)
    return None


def collect_log_file_names(log_folder: str) -> List[str]:
    logger.info("Collecting log file names")
    return [file_name for file_name in os.listdir(log_folder)]


def validate_log_file_names(
    log_file_names: List[str], pattern: re.Pattern[str]
) -> List[str]:
    logger.info("Validating log file names")
    return [file_name for file_name in log_file_names if pattern.match(file_name)]


def get_latest_log_file(log_folder: str, latest_date: str) -> str:
    logger.info("Getting latest log file", latest_date=latest_date)
    return f"{log_folder}/nginx-access-ui.log-{latest_date}"


def find_log_file_name_and_date(config: Dict[str, str]) -> Optional[Tuple[str, str]]:
    file_name_search_pattern = generate_log_file_name_search_pattern()
    log_folder = config.get("LOG_DIR")
    if not log_folder:
        logger.warning("LOG_DIR not found in config")
        return None

    log_file_names = collect_log_file_names(log_folder)
    validated_log_files = validate_log_file_names(
        log_file_names, file_name_search_pattern
    )
    log_file_dates = [file_date.split("-")[-1] for file_date in validated_log_files]

    if not log_file_dates:
        logger.warning("No log files found in the log directory")
        return None

    latest_log_file_date = max(log_file_dates)
    log_file_name = get_latest_log_file(log_folder, latest_log_file_date)
    return log_file_name, latest_log_file_date
