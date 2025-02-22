import re
from src.app.logger import logger


def generate_search_pattern() -> re.Pattern:
    logger.info("Generating search pattern")
    return re.compile(r'\"([A-Z]+) (/[^\s]+) HTTP/1\.[01]\"\s.*\s(\d+\.\d+)$')


def generate_log_file_name_search_pattern() -> re.Pattern:
    logger.info("Generating log file name search pattern")
    return re.compile(r'nginx-access-ui\.log-\d{8}(\.gz)?')