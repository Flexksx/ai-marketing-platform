import json
import logging
from datetime import UTC, datetime
from logging.config import dictConfig
from typing import Any


def _get_log_level(level: str) -> int:
    if not level:
        return logging.INFO
    normalized = level.upper()
    if normalized not in logging._nameToLevel:
        return logging.INFO
    return logging._nameToLevel[normalized]


class JsonFormatter(logging.Formatter):
    def __init__(self, service_name: str = "scraper-api") -> None:
        super().__init__()
        self.service_name = service_name

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "severity": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "timestamp": datetime.now(UTC).isoformat(),
            "service": self.service_name,
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str, ensure_ascii=False)


def configure_logging(level: str = "INFO", service_name: str = "scraper-api") -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "json": {
                    "()": "src.logging_config.JsonFormatter",
                    "service_name": service_name,
                },
            },
            "handlers": {
                "default": {
                    "class": "logging.StreamHandler",
                    "formatter": "json",
                },
                "null": {
                    "class": "logging.NullHandler",
                },
            },
            "loggers": {
                "uvicorn.access": {
                    "handlers": ["null"],
                    "propagate": False,
                },
                "uvicorn.error": {
                    "handlers": ["default"],
                    "propagate": False,
                },
                "uvicorn": {
                    "handlers": ["default"],
                    "propagate": False,
                },
            },
            "root": {
                "level": _get_log_level(level),
                "handlers": ["default"],
            },
        }
    )
