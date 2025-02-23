import json
import argparse
import gzip

from src.app.regex_helpers import generate_search_pattern
from src.app.report_helpers import generate_reports, generate_report_file
from src.app.logger import configure_logging, logger
from src.app.log_file_helpers import find_log_file_name_and_date

config = {
    "REPORT_SIZE": 1000,
    "REPORT_DIR": "./reports",
    "LOG_DIR": "./log",
    "TEMPLATE_FILE": "report.html",
    "LOG_FILE": None
}


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

    log_file_name, latest_date = find_log_file_name_and_date(config)

    search_pattern = generate_search_pattern()

    logger.info("Starting log analysis", config=config)

    try:
        if log_file_name.endswith('gz'):
            with gzip.open(log_file_name, 'rt', encoding='utf-8') as log_file:
                reports = generate_reports(log_file=log_file, search_pattern=search_pattern)
                generate_report_file(reports, config, latest_date)
        else:
            with open(log_file_name, 'r') as log_file:
                reports = generate_reports(log_file=log_file, search_pattern=search_pattern)
                generate_report_file(reports, config, latest_date)
    except FileNotFoundError:
        logger.error("Log file not found", config_file_path=config_file_path.config)

    logger.info("Log analysis completed")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except BaseException as e:
        logger.error(e)
        logger.error("Unexpected error occurred", exc_info=True)