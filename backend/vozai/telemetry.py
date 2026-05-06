import logging
import os

from fastapi import FastAPI


logger = logging.getLogger(__name__)


def setup_telemetry(app: FastAPI, service_name: str, environment: str) -> None:
    """Configure OpenTelemetry via logfire.

    No-ops when OTEL_EXPORTER_OTLP_ENDPOINT is not set, so local dev without
    the observability stack running stays unaffected.

    Instruments:
    - FastAPI (HTTP spans, route attributes)
    - HTTPX (outbound HTTP calls)
    - SQLAlchemy (query spans)
    - pydantic-ai agents (LLM calls, token counts, tool calls) — automatic
      when logfire is configured, because pydantic-ai emits logfire spans.
    """
    otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    if not otlp_endpoint:
        logger.debug("OTEL_EXPORTER_OTLP_ENDPOINT not set — telemetry disabled")
        return

    try:
        import logfire
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
            OTLPSpanExporter,
        )
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
    except ImportError as exc:
        logger.warning("logfire/opentelemetry not installed — telemetry disabled: %s", exc)
        return

    traces_endpoint = otlp_endpoint.rstrip("/") + "/v1/traces"

    logfire.configure(
        service_name=service_name,
        environment=environment,
        send_to_logfire=False,
        additional_span_processors=[
            BatchSpanProcessor(OTLPSpanExporter(endpoint=traces_endpoint))
        ],
    )

    logfire.instrument_fastapi(app)
    logfire.instrument_httpx()
    logfire.instrument_sqlalchemy()

    logger.info(
        "Telemetry configured",
        extra={"service": service_name, "otlp_endpoint": traces_endpoint},
    )
