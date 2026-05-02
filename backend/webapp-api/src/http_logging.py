import logging
import time
from collections.abc import Awaitable, Callable

from fastapi import Request, Response


logger = logging.getLogger(__name__)


_SILENT_PATHS = {"/health", "/"}


async def http_logging_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    if request.url.path in _SILENT_PATHS:
        return await call_next(request)

    start = time.perf_counter()
    response = await call_next(request)
    elapsed = time.perf_counter() - start

    http_request = {
        "requestMethod": request.method,
        "requestUrl": str(request.url),
        "status": response.status_code,
        "userAgent": request.headers.get("user-agent"),
        "remoteIp": request.client.host if request.client else None,
        "latency": f"{elapsed:.6f}s",
    }

    logger.info(
        "http_request",
        extra={
            "http_request": http_request,
        },
    )

    return response
