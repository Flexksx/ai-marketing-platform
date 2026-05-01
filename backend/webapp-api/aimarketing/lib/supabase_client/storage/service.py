import uuid
from pathlib import Path

import httpx
import public
from fastapi import Depends
from supabase import AsyncClient

from aimarketing.auth import get_async_supabase_service_client
from aimarketing.lib.supabase_client.storage.schema import (
    ImageByUrlStorageUploadRequest,
    StorageBucket,
    StorageUploadRequest,
    StorageUploadResult,
)


@public.add
class SupabaseStorageService:
    def __init__(
        self, client: AsyncClient = Depends(get_async_supabase_service_client)
    ):
        self.client = client

    def _generate_unique_filename(self, original_filename: str) -> str:
        path = Path(original_filename)
        unique_id = uuid.uuid4().hex[:8]
        return f"{path.stem}_{unique_id}{path.suffix}"

    async def upload_public(self, request: StorageUploadRequest) -> StorageUploadResult:
        bucket_value = request.bucket.value
        storage_bucket = self.client.storage.from_(bucket_value)

        if "/" in request.path:
            directory, filename = request.path.rsplit("/", 1)
            unique_filename = self._generate_unique_filename(filename)
            unique_path = f"{directory}/{unique_filename}"
        else:
            unique_path = self._generate_unique_filename(request.path)

        response = await storage_bucket.upload(
            path=unique_path,
            file=request.content,
            file_options=(
                {"content-type": request.content_type} if request.content_type else None
            ),
        )

        if hasattr(response, "error") and response.error:
            raise ValueError(str(response.error))

        public_url = await self.get_public_url(request.bucket, unique_path)
        return StorageUploadResult(path=unique_path, public_url=public_url)

    async def upload_from_url(
        self, request: ImageByUrlStorageUploadRequest
    ) -> StorageUploadResult:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            response = await client.get(request.image_url)
            response.raise_for_status()

            content_type = response.headers.get("content-type", "image/jpeg")
            ext_map = {
                "image/png": "png",
                "image/webp": "webp",
                "image/gif": "gif",
            }
            ext = ext_map.get(content_type, "jpg")

            filename = f"image_{uuid.uuid4().hex[:8]}.{ext}"
            path = (
                f"{request.path_prefix}/{filename}" if request.path_prefix else filename
            )

            upload_request = StorageUploadRequest(
                bucket=request.bucket,
                path=path,
                content=response.content,
                content_type=content_type,
            )
            return await self.upload_public(upload_request)

    async def get_public_url(self, bucket: StorageBucket, path: str) -> str:
        bucket_value = bucket.value
        storage_bucket = self.client.storage.from_(bucket_value)
        return await storage_bucket.get_public_url(path)
