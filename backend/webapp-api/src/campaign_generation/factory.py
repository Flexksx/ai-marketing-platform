import asyncio

from fastapi import UploadFile

from webapp_api_contract.campaign_generation import (
    CampaignGenerationJobCreateRequest,
    ProductLifestyleCampaignGenerationJobUserInput,
    UserMediaOnlyCampaignGenerationJobUserInput,
)
from lib.supabase_client import (
    StorageBucket,
    StorageUploadRequest,
    StorageUploadResult,
    SupabaseStorageService,
)


async def get_from_request_form(
    brand_id: str,
    request_data: str,
    request_files: list[UploadFile],
    supabase_storage_service: SupabaseStorageService,
) -> CampaignGenerationJobCreateRequest:
    request = CampaignGenerationJobCreateRequest.model_validate_json(request_data)
    request.brand_id = brand_id
    user_input = request.user_input

    if isinstance(
        user_input,
        (
            UserMediaOnlyCampaignGenerationJobUserInput,
            ProductLifestyleCampaignGenerationJobUserInput,
        ),
    ):
        media_urls = await __upload_user_media(
            brand_id, request_files, supabase_storage_service
        )
        user_input.image_urls = media_urls

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
                bucket=StorageBucket.CAMPAIGN_USER_MEDIA,
                path=f"campaigns_generation_jobs/{brand_id}/{image_file.filename}",
                content=await image_file.read(),
                content_type=image_file.content_type,
            )
        )
        upload_tasks.append(task)
    upload_results: list[StorageUploadResult] = await asyncio.gather(*upload_tasks)
    return [result.public_url for result in upload_results]
