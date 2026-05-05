import src.content.service as content_service
import src.content_generation_job.repository as content_generation_job_repository
from src.content.model import ContentCreateRequest, TextOnlyContentData
from src.content_generation_job.errors import (
    ContentGenerationJobNoResultException,
    ContentGenerationJobUnsupportedWorkflowTypeException,
)
from src.content_generation_job.model import (
    ContentGenerationJob,
    ContentGenerationJobCreateRequest,
    ContentGenerationJobSearchRequest,
    ContentGenerationJobUpdateRequest,
    TextWithSingleImageContentGenerationJobResult,
)


async def create(request: ContentGenerationJobCreateRequest) -> ContentGenerationJob:
    return await content_generation_job_repository.create(request)


async def get(job_id: str) -> ContentGenerationJob:
    return await content_generation_job_repository.get(job_id)


async def update(
    job_id: str,
    request: ContentGenerationJobUpdateRequest,
) -> ContentGenerationJob:
    return await content_generation_job_repository.update(job_id, request)


async def search(request: ContentGenerationJobSearchRequest) -> list[ContentGenerationJob]:
    return await content_generation_job_repository.search(request)


async def accept(job_id: str):
    job = await get(job_id)
    result = job.result
    if result is None:
        raise ContentGenerationJobNoResultException(job_id)

    if isinstance(result, TextOnlyContentData):
        raise ContentGenerationJobUnsupportedWorkflowTypeException(
            job_id,
            job.user_input.workflow_type,
        )

    if isinstance(result, TextWithSingleImageContentGenerationJobResult):
        user_input = job.user_input
        request = ContentCreateRequest(
            brand_id=job.brand_id,
            campaign_id=None,
            content_format=result.data.content_format,
            data=result.data,
            channel=result.channel,
            scheduled_at=user_input.scheduled_at,
        )
        return await content_service.create(request)

    return job
