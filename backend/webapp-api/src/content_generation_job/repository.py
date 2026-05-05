from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from lib.db.session_factory import DbSessionFactory
from lib.utils import new_id
from src.content_generation_job.entity import ContentGenerationJobRecord
from src.content_generation_job.errors import (
    ContentGenerationJobNotFoundException,
)
from src.content_generation_job.model import (
    ContentGenerationJob,
    ContentGenerationJobCreateRequest,
    ContentGenerationJobSearchRequest,
    ContentGenerationJobUpdateRequest,
)
from src.shared.model import JobStatus


async def create(
    session_factory: DbSessionFactory,
    request: ContentGenerationJobCreateRequest,
) -> ContentGenerationJob:
    async with session_factory.session() as session:
        user_input_dict = request.user_input.model_dump(mode="json")
        record = ContentGenerationJobRecord(
            id=new_id(),
            brand_id=request.brand_id,
            user_input=user_input_dict,
            content_format=request.content_format,
            status=JobStatus.PENDING,
            result=None,
        )
        session.add(record)
        await session.commit()
        await session.refresh(record)
        return ContentGenerationJob.model_validate(record)


async def update(
    session_factory: DbSessionFactory,
    job_id: str,
    request: ContentGenerationJobUpdateRequest,
) -> ContentGenerationJob:
    async with session_factory.session() as session:
        record = await _get_by_id(session, job_id)
        if request.status is not None:
            record.status = request.status
        if request.result is not None:
            record.result = request.result.model_dump(mode="json")
        await session.commit()
        await session.refresh(record)
        return ContentGenerationJob.model_validate(record)


async def get(
    session_factory: DbSessionFactory,
    job_id: str,
) -> ContentGenerationJob:
    async with session_factory.session() as session:
        record = await _get_by_id(session, job_id)
        return ContentGenerationJob.model_validate(record)


async def search(
    session_factory: DbSessionFactory,
    request: ContentGenerationJobSearchRequest,
) -> list[ContentGenerationJob]:
    async with session_factory.session() as session:
        query = select(ContentGenerationJobRecord)
        if request.brand_id is not None:
            query = query.where(ContentGenerationJobRecord.brand_id == request.brand_id)
        query = query.order_by(desc(ContentGenerationJobRecord.created_at))
        result = await session.execute(query)
        records = result.scalars().all()
        return [ContentGenerationJob.model_validate(record) for record in records]


async def _get_by_id(session: AsyncSession, job_id: str) -> ContentGenerationJobRecord:
    statement = select(ContentGenerationJobRecord).filter(
        ContentGenerationJobRecord.id == job_id
    )
    result = await session.execute(statement)
    record = result.scalar_one_or_none()
    if not record:
        raise ContentGenerationJobNotFoundException(job_id)
    return record
