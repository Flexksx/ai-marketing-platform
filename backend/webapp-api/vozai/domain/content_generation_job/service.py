import vozai.domain.content.service as content_service
import vozai.domain.content_generation_job.repository as content_generation_job_repository
from db.session_factory import DbSessionFactory
from vozai.domain.content import TextOnlyContentData
from vozai.domain.content.schema import ContentCreateRequest
from vozai.domain.content_generation_job.content_type.text_with_single_image import (
    TextWithSingleImageContentGenerationJobResult,
)
from vozai.domain.content_generation_job.errors import (
    ContentGenerationJobNoResultException,
    ContentGenerationJobUnsupportedWorkflowTypeException,
)
from vozai.domain.content_generation_job.model import ContentGenerationJob
from vozai.domain.content_generation_job.schema import (
    ContentGenerationJobCreateRequest,
    ContentGenerationJobSearchRequest,
    ContentGenerationJobUpdateRequest,
)
from vozai.lib.cloudtasks.service import CloudTasksService


async def create(
    session_factory: DbSessionFactory,
    request: ContentGenerationJobCreateRequest,
) -> ContentGenerationJob:
    return await content_generation_job_repository.create(session_factory, request)


async def get(
    session_factory: DbSessionFactory,
    job_id: str,
) -> ContentGenerationJob:
    return await content_generation_job_repository.get(session_factory, job_id)


async def update(
    session_factory: DbSessionFactory,
    job_id: str,
    request: ContentGenerationJobUpdateRequest,
) -> ContentGenerationJob:
    return await content_generation_job_repository.update(
        session_factory,
        job_id,
        request,
    )


async def search(
    session_factory: DbSessionFactory,
    request: ContentGenerationJobSearchRequest,
) -> list[ContentGenerationJob]:
    return await content_generation_job_repository.search(session_factory, request)


async def start(
    session_factory: DbSessionFactory,
    tasks_service: CloudTasksService,
    request: ContentGenerationJobCreateRequest,
) -> ContentGenerationJob:
    job = await create(session_factory, request)
    await tasks_service.enqueue_content_generation(job.id)
    return job


async def accept(session_factory: DbSessionFactory, job_id: str):
    job = await get(session_factory, job_id)
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
        return await content_service.create(session_factory, request)

    return job
