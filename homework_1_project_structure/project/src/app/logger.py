import logging
from typing import Optional

import structlog


def configure_logging(log_file_path: Optional[str] = None) -> None:
    processors = [
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M.%S"),
        structlog.processors.add_log_level,
        structlog.processors.format_exc_info,
        structlog.dev.ConsoleRenderer(),
    ]

    structlog.configure(
        processors=processors,
    )

    if log_file_path:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(message)s",
            handlers=[logging.FileHandler(log_file_path), logging.StreamHandler()],
        )
    else:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(message)s",
            handlers=[logging.StreamHandler()],
        )


logger = structlog.get_logger()
