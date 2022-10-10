import logging.config
import os

from typing import Optional

URL_BASE_ZENODO = "https://zenodo.org"
URL_BASE_SANDBOX = "https://sandbox.zenodo.org"

URL_DICT = {
    "depositions": "api/deposit/depositions",
    "records": "api/records",
}

GLOBAL_CONFIG = {
    "log_level": os.environ.get("PY2ZENODO_LOG_LEVEL") or "INFO",
}

_logger_config = {
    "version": 1,
    "formatters": {
        "default_formatter": {
            "format": "[%(asctime)s][%(name)s][%(funcName)s][%(levelname)s] %(message)s",
        },
    },
    "handlers": {
        "stream_handler": {
            "class": "logging.StreamHandler",
            "formatter": "default_formatter",
            "level": "DEBUG",
        },
    },
    "loggers": {
        "py2zenodo": {
            "handlers": ["stream_handler"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
logging.config.dictConfig(_logger_config)


def get_logger(name, /, *, log_level: Optional[str] = None):
    logger = logging.getLogger(name)
    logger.setLevel(log_level or GLOBAL_CONFIG["log_level"])
    return logger


__all__ = [
    "URL_BASE_ZENODO",
    "URL_BASE_SANDBOX",
    "URL_DICT",
    "GLOBAL_CONFIG",
    "get_logger",
]
