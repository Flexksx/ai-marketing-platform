import logging

from fastapi import Depends, Header, HTTPException
from supabase import AsyncClient, create_async_client

from src.config import get_settings


logger = logging.getLogger(__name__)

_async_supabase_client: AsyncClient | None = None
_async_supabase_service_client: AsyncClient | None = None


async def get_async_supabase_client() -> AsyncClient:
    global _async_supabase_client  # noqa: PLW0603
    if _async_supabase_client is None:
        settings = get_settings()
        if not settings.supabase_url or not settings.supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY are required.")

        _async_supabase_client = await create_async_client(
            settings.supabase_url, settings.supabase_key
        )
    return _async_supabase_client


async def get_async_supabase_service_client() -> AsyncClient:
    global _async_supabase_service_client  # noqa: PLW0603
    if _async_supabase_service_client is None:
        settings = get_settings()
        service_role_key = settings.supabase_service_role_key or settings.supabase_key

        if not settings.supabase_url or not service_role_key:
            raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are required.")

        _async_supabase_service_client = await create_async_client(
            settings.supabase_url, service_role_key
        )
    return _async_supabase_service_client


async def get_current_user_id(
    authorization: str | None = Header(None, alias="Authorization"),
    async_supabase_client: AsyncClient = Depends(get_async_supabase_service_client),
) -> str:
    """
    Extract and verify user ID from Authorization header.
    """
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header is required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    parts = authorization.split(" ")
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header format. Expected: Bearer <token>",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = parts[1]

    try:
        response = await async_supabase_client.auth.get_user(jwt=token)

        if not response or not response.user:
            raise HTTPException(
                status_code=401,
                detail="User not found in token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return response.user.id

    except HTTPException:
        raise
    except Exception as e:
        logger.warning(f"Token validation failed: {e!s}")
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
