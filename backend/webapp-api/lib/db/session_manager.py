import asyncio
import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager, suppress

from sqlalchemy.exc import DisconnectionError, OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

from lib.db.database import AsyncSessionLocal


logger = logging.getLogger(__name__)

MAX_RETRIES = 3
INITIAL_RETRY_DELAY = 0.1
MAX_RETRY_DELAY = 2.0


def _calculate_retry_delay(attempt: int) -> float:
    delay = INITIAL_RETRY_DELAY * (2**attempt)
    return min(delay, MAX_RETRY_DELAY)


def _is_retryable_error(error: Exception) -> bool:
    if isinstance(error, (OperationalError, DisconnectionError)):
        error_str = str(error).lower()
        retryable_keywords = [
            "connection",
            "timeout",
            "closed",
            "lost",
            "broken",
            "pool",
            "server has gone away",
            "connection reset",
            "maxclientsinsessionmode",
            "max clients reached",
        ]
        return any(keyword in error_str for keyword in retryable_keywords)
    error_str = str(error).lower()
    return bool(
        "maxclientsinsessionmode" in error_str or "max clients reached" in error_str
    )


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession]:
    last_error = None

    for attempt in range(MAX_RETRIES):
        session = None
        try:
            session = AsyncSessionLocal()
            try:
                yield session
                return
            except Exception:
                await session.rollback()
                raise
        except Exception as e:
            if _is_retryable_error(e) and attempt < MAX_RETRIES - 1:
                logger.warning(
                    f"Session creation failed (attempt {attempt + 1}/{MAX_RETRIES}): {e}. Retrying..."
                )
                last_error = e
                await asyncio.sleep(_calculate_retry_delay(attempt))
                continue
            raise
        finally:
            if session:
                with suppress(Exception):
                    await session.close()

    if last_error:
        logger.error(f"Failed to get database session after {MAX_RETRIES} attempts")
        raise last_error
