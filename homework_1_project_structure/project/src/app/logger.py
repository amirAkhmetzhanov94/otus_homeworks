import logging
from typing import Optional

import structlog


def configure_logging(log_file_path: Optional[str] = None) -> None:
    processors = [structlog.stdlib.filter_by_level, structlog.processors.JSONRenderer()]

    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
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
