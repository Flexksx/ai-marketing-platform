from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lib.db.session_factory import DbSessionFactory
from lib.utils import new_id
from src.brand_generation_job.entity import BrandGenerationJobRecord
from src.brand_generation_job.errors import BrandGenerationJobNotFoundError
from src.brand_generation_job.model import (
    BrandGenerationJob,
    BrandGenerationJobCreateRequest,
    BrandGenerationJobUpdateRequest,
)
from src.shared.model import JobStatus


async def create(
    session_factory: DbSessionFactory,
    user_id: str,
    request: BrandGenerationJobCreateRequest,
) -> BrandGenerationJob:
    async with session_factory.session() as session:
        job_record = BrandGenerationJobRecord(
            id=new_id(),
            status=JobStatus.PENDING,
            website_url=request.website_url,
            user_id=user_id,
            extra_routes=request.extra_routes,
            result=None,
        )
        session.add(job_record)
        await session.commit()
        await session.refresh(job_record)
        return BrandGenerationJob.model_validate(job_record)


async def update(
    session_factory: DbSessionFactory,
    job_id: str,
    request: BrandGenerationJobUpdateRequest,
) -> BrandGenerationJob:
    async with session_factory.session() as session:
        job = await _record_by_id(session, job_id)
        if request.result is not None:
            result_dict = request.result.model_dump(mode="json")
        if request.status is not None:
            job.status = request.status  # pyright: ignore[reportAttributeAccessIssue]
        if request.result is not None:
            job.result = result_dict  # pyright: ignore[reportAttributeAccessIssue]
        await session.commit()
        await session.refresh(job)
        return BrandGenerationJob.model_validate(job)


async def get(session_factory: DbSessionFactory, job_id: str) -> BrandGenerationJob:
    async with session_factory.session() as session:
        job = await _record_by_id(session, job_id)
        return BrandGenerationJob.model_validate(job)


async def exists_for_user(
    session_factory: DbSessionFactory,
    job_id: str,
    user_id: str,
) -> bool:
    async with session_factory.session() as session:
        statement = select(BrandGenerationJobRecord).filter(
            BrandGenerationJobRecord.id == job_id,
            BrandGenerationJobRecord.user_id == user_id,
        )
        result = await session.execute(statement)
        record = result.scalar_one_or_none()
        return record is not None


async def _record_by_id(session: AsyncSession, job_id: str) -> BrandGenerationJobRecord:
    stmt = select(BrandGenerationJobRecord).filter(
        BrandGenerationJobRecord.id == job_id
    )
    result = await session.execute(stmt)
    record = result.scalar_one_or_none()
    if not record:
        raise BrandGenerationJobNotFoundError(job_id)
    return record
