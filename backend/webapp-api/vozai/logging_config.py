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
    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.now(UTC).isoformat()
        payload: dict[str, Any] = {
            "severity": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "timestamp": timestamp,
        }

        service = getattr(record, "service", None)
        environment = getattr(record, "environment", None)
        http_request = getattr(record, "http_request", None)
        trace_id = getattr(record, "trace_id", None)
        span_id = getattr(record, "span_id", None)
        job_id = getattr(record, "job_id", None)

        if service:
            payload["service"] = service
        if environment:
            payload["environment"] = environment
        if http_request:
            payload["httpRequest"] = http_request
        if trace_id:
            payload["trace_id"] = trace_id
        if span_id:
            payload["span_id"] = span_id
        if job_id:
            payload["job_id"] = job_id

        return json.dumps(payload, default=str, ensure_ascii=False)


def configure_logging(level: str, service_name: str, environment: str) -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "json": {
                    "()": "vozai.logging_config.JsonFormatter",
                },
            },
            "handlers": {
                "default": {
                    "class": "logging.StreamHandler",
                    "formatter": "json",
                },
            },
            "root": {
                "level": _get_log_level(level),
                "handlers": ["default"],
            },
        }
    )

    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        if isinstance(handler.formatter, JsonFormatter):
            handler.addFilter(
                _ContextFilter(
                    service_name=service_name,
                    environment=environment,
                )
            )


class _ContextFilter(logging.Filter):
    def __init__(self, service_name: str, environment: str) -> None:
        super().__init__()
        self.service_name = service_name
        self.environment = environment

    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "service"):
            record.service = self.service_name
        if not hasattr(record, "environment"):
            record.environment = self.environment
        return True
