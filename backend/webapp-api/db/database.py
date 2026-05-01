import logging
import os
from functools import lru_cache

import public
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from aimarketing.config import get_settings


logger = logging.getLogger(__name__)

settings = get_settings()


@public.add
class Base(DeclarativeBase):
    pass


@lru_cache
def get_database_url() -> str:
    database_url = (
        os.getenv("DIRECT_URL")
        or os.getenv("DATABASE_URL")
        or settings.effective_database_url
    )
    if not database_url:
        raise ValueError(
            "DIRECT_URL or DATABASE_URL must be set. "
            "For migrations, use DIRECT_URL (direct connection, port 5432) "
            "instead of transaction pooler (port 6543)."
        )
    return database_url


def get_async_database_url() -> str:
    url = get_database_url()
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    if "postgresql+asyncpg://" in url:
        return url
    return url


def get_pool_size() -> int:
    pool_size = int(os.getenv("DB_POOL_SIZE", "20"))
    return max(1, pool_size)


def get_max_overflow() -> int:
    max_overflow = int(os.getenv("DB_MAX_OVERFLOW", "10"))
    return max(0, max_overflow)


def get_pool_timeout() -> int:
    pool_timeout = int(os.getenv("DB_POOL_TIMEOUT", "30"))
    return max(1, pool_timeout)


engine = create_async_engine(
    get_async_database_url(),
    pool_pre_ping=True,
    pool_size=get_pool_size(),
    max_overflow=get_max_overflow(),
    pool_timeout=get_pool_timeout(),
    pool_recycle=3600,
    echo=False,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


def get_pool_status() -> dict:
    pool = engine.pool
    try:
        return {
            "size": getattr(pool, "_pool", {}).get("size", get_pool_size()),
            "checked_in": len(getattr(pool, "_checked_in", [])),
            "checked_out": len(getattr(pool, "_checked_out", [])),
            "overflow": getattr(pool, "_overflow", 0),
            "max_overflow": get_max_overflow(),
            "pool_size": get_pool_size(),
        }
    except Exception as e:
        logger.warning(f"Could not get detailed pool status: {e}")
        return {
            "pool_size": get_pool_size(),
            "max_overflow": get_max_overflow(),
            "status": "unknown",
        }
