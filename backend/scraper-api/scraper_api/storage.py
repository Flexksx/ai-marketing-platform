import logging
import uuid
from enum import Enum

from pydantic import BaseModel
from supabase import AsyncClient, create_async_client

from scraper_api.config import get_settings


logger = logging.getLogger(__name__)

_client: AsyncClient | None = None


class StorageBucket(str, Enum):
    BRAND_EXTRACTION = "brand-extraction"


class StorageUploadRequest(BaseModel):
    bucket: StorageBucket
    path: str
    content: bytes
    content_type: str | None = None


class StorageUploadResult(BaseModel):
    path: str
    public_url: str


async def get_storage_client() -> AsyncClient | None:
    global _client  # noqa: PLW0603
    settings = get_settings()
    if not settings.supabase_url or not settings.supabase_service_role_key:
        logger.warning("Supabase credentials not set — screenshot upload disabled")
        return None
    if _client is None:
        _client = await create_async_client(
            settings.supabase_url, settings.supabase_service_role_key
        )
    return _client


def _unique_path(path: str) -> str:
    from pathlib import Path

    p = Path(path)
    uid = uuid.uuid4().hex[:8]
    return str(p.parent / f"{p.stem}_{uid}{p.suffix}")


async def upload_public(request: StorageUploadRequest) -> StorageUploadResult | None:
    client = await get_storage_client()
    if client is None:
        return None
    try:
        bucket = client.storage.from_(request.bucket.value)
        unique_path = _unique_path(request.path)
        await bucket.upload(
            path=unique_path,
            file=request.content,
            file_options=(
                {"content-type": request.content_type} if request.content_type else None
            ),
        )
        public_url = await bucket.get_public_url(unique_path)
        return StorageUploadResult(path=unique_path, public_url=public_url)
    except Exception as e:
        logger.warning(f"Screenshot upload failed (non-critical): {e}")
        return None
