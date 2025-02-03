import os
from logging.config import dictConfig
from pathlib import Path

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"},
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(pathname)s:%(lineno)d]"
        },
        "json": {
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s %(pathname)s %(lineno)s %(funcName)s %(process)d %(thread)d %(threadName)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "detailed",
            "filename": "logs/error.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "level": "ERROR",
        },
        "app_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "json",
            "filename": "logs/app.log",
            "when": "midnight",
            "interval": 1,
            "backupCount": 30,
        },
        "celery_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "json",
            "filename": "logs/celery.log",
            "maxBytes": 10485760,
            "backupCount": 5,
        },
        "sqlalchemy_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "detailed",
            "filename": "logs/sqlalchemy.log",
            "maxBytes": 10485760,
            "backupCount": 5,
        },
    },
    "loggers": {
        "": {  # Root logger
            "handlers": ["console", "error_file"],
            "level": LOG_LEVEL,
        },
        "app": {"handlers": ["app_file"], "level": LOG_LEVEL, "propagate": True},
        "uvicorn": {
            "handlers": ["app_file"],
            "level": LOG_LEVEL,
            "propagate": True,  # Changed to False
        },
        "uvicorn.error": {
            "level": LOG_LEVEL,
            "propagate": False,  # Added this logger
        },
    },
}


def setup_logging():
    """Initialize logging configuration"""
    dictConfig(LOGGING_CONFIG)
