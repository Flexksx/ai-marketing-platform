import vozai.domain.brand.service as brand_service
import vozai.domain.brand_extraction.repository as brand_generation_job_repository
from db.session_factory import DbSessionFactory
from vozai.domain.brand.model import Brand
from vozai.domain.brand.schema import BrandCreateRequest
from vozai.domain.brand_extraction.model import BrandGenerationJob
from vozai.domain.brand_extraction.schema import (
    BrandGenerationJobAcceptRequest,
    BrandGenerationJobCreateRequest,
    BrandGenerationJobUpdateRequest,
)
from vozai.lib.cloudtasks.service import CloudTasksService


async def create(
    session_factory: DbSessionFactory,
    user_id: str,
    request: BrandGenerationJobCreateRequest,
) -> BrandGenerationJob:
    return await brand_generation_job_repository.create(
        session_factory,
        user_id,
        request,
    )


async def get(
    session_factory: DbSessionFactory,
    job_id: str,
) -> BrandGenerationJob:
    return await brand_generation_job_repository.get(session_factory, job_id)


async def update(
    session_factory: DbSessionFactory,
    job_id: str,
    request: BrandGenerationJobUpdateRequest,
) -> BrandGenerationJob:
    return await brand_generation_job_repository.update(
        session_factory,
        job_id,
        request,
    )


async def start(
    session_factory: DbSessionFactory,
    tasks_service: CloudTasksService,
    user_id: str,
    request: BrandGenerationJobCreateRequest,
) -> BrandGenerationJob:
    job = await create(session_factory, user_id, request)
    await tasks_service.enqueue_brand_generation(job.id)
    return job


async def accept(
    session_factory: DbSessionFactory,
    job_id: str,
    request: BrandGenerationJobAcceptRequest,
) -> Brand:
    job = await get(session_factory, job_id)
    brand_input = BrandCreateRequest(name=request.name, data=request.data)
    return await brand_service.create(
        session_factory,
        job.user_id,
        brand_input,
    )


async def validate_access(
    session_factory: DbSessionFactory,
    job_id: str,
    user_id: str,
) -> bool:
    return await brand_generation_job_repository.exists_for_user(
        session_factory,
        job_id,
        user_id,
    )
