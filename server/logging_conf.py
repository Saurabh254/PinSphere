import logging
import sys
from logging.handlers import RotatingFileHandler

import structlog

LOG_LEVEL = logging.getLevelName(logging.root.level)
LOG_FILENAME = "/var/log/fastapi.log" if LOG_LEVEL == logging.INFO else "fastapi.log"


# Custom log format
def configure_logging():
    logging.basicConfig(
        level=LOG_LEVEL,
        format="%(message)s",  # Structlog will handle formatting
        handlers=[
            logging.StreamHandler(sys.stdout),  # Console logs
            RotatingFileHandler(
                LOG_FILENAME, maxBytes=10 * 1024 * 1024, backupCount=5
            ),  # File logs with rotation
        ],
    )

    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


# Initialize logging
configure_logging()
log = structlog.get_logger()
