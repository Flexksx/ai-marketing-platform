import asyncio

import public
from fastapi import UploadFile

from aimarketing.domain.content_generation_job import (
    ContentGenerationJobCreateRequest,
    FromUserMediaTextWithSingleImageContentGenerationJobUserInput,
    ProductLifestyleTextWithSingleImageContentGenerationJobUserInput,
)
from aimarketing.lib.supabase_client import (
    StorageBucket,
    StorageUploadRequest,
    StorageUploadResult,
    SupabaseStorageService,
)


IMAGE_INPUT_TYPES = (
    FromUserMediaTextWithSingleImageContentGenerationJobUserInput,
    ProductLifestyleTextWithSingleImageContentGenerationJobUserInput,
)


@public.add
async def get_from_request_form(
    brand_id: str,
    request_data: str,
    request_files: list[UploadFile],
    supabase_storage_service: SupabaseStorageService,
) -> ContentGenerationJobCreateRequest:
    request = ContentGenerationJobCreateRequest.model_validate_json(request_data)
    request.brand_id = brand_id
    user_input = request.user_input
    if isinstance(user_input, IMAGE_INPUT_TYPES):
        if not request_files:
            raise ValueError("Files are required for USER_MEDIA workflow type")
        media_urls = await __upload_user_media(
            brand_id, request_files, supabase_storage_service
        )
        if not media_urls:
            raise ValueError("Failed to upload media files")
        user_input.image_url: str = media_urls[0]
    request.user_input = user_input
    return request


async def __upload_user_media(
    brand_id: str,
    request_files: list[UploadFile],
    supabase_storage_service: SupabaseStorageService,
) -> list[str]:
    upload_tasks = []
    for image_file in request_files:
        task = supabase_storage_service.upload_public(
            StorageUploadRequest(
                bucket=StorageBucket.CONTENT_GENERATION_JOBS_USER_MEDIA,
                path=f"content_generation_jobs/{brand_id}/{image_file.filename}",
                content=await image_file.read(),
                content_type=image_file.content_type,
            )
        )
        upload_tasks.append(task)
    upload_results: list[StorageUploadResult] = await asyncio.gather(*upload_tasks)
    return [result.public_url for result in upload_results]
