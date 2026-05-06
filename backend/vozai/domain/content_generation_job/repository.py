import logging

from fastapi import Depends
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.session_factory import DbSessionFactory
from vozai.domain.content_generation_job.entity import ContentGenerationJobRecord
from vozai.domain.content_generation_job.errors import (
    ContentGenerationJobNotFoundException,
)
from vozai.domain.content_generation_job.model import ContentGenerationJob
from vozai.domain.content_generation_job.schema import (
    ContentGenerationJobCreateRequest,
    ContentGenerationJobSearchRequest,
    ContentGenerationJobUpdateRequest,
)
from vozai.lib.job.model import JobStatus
from vozai.utils import new_id


logger = logging.getLogger(__name__)


class ContentGenerationJobRepository:
    def __init__(self, session_factory: DbSessionFactory = Depends()):
        self._session_factory = session_factory

    async def create(
        self, request: ContentGenerationJobCreateRequest
    ) -> ContentGenerationJob:
        async with self._session_factory.session() as session:
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
        self, job_id: str, request: ContentGenerationJobUpdateRequest
    ) -> ContentGenerationJob:
        async with self._session_factory.session() as session:
            record = await self._get_by_id(session, job_id)
            if request.status is not None:
                record.status = request.status
            if request.result is not None:
                record.result = request.result.model_dump(mode="json")
            await session.commit()
            await session.refresh(record)
            return ContentGenerationJob.model_validate(record)

    async def get(self, job_id: str) -> ContentGenerationJob:
        async with self._session_factory.session() as session:
            record = await self._get_by_id(session, job_id)
            return ContentGenerationJob.model_validate(record)

    async def search(
        self, request: ContentGenerationJobSearchRequest
    ) -> list[ContentGenerationJob]:
        async with self._session_factory.session() as session:
            query = select(ContentGenerationJobRecord)
            if request.brand_id is not None:
                query = query.where(
                    ContentGenerationJobRecord.brand_id == request.brand_id
                )
            query = query.order_by(desc(ContentGenerationJobRecord.created_at))
            result = await session.execute(query)
            records = result.scalars().all()
            return [ContentGenerationJob.model_validate(record) for record in records]

    async def _get_by_id(
        self, session: AsyncSession, job_id: str
    ) -> ContentGenerationJobRecord:
        statement = select(ContentGenerationJobRecord).filter(
            ContentGenerationJobRecord.id == job_id
        )
        result = await session.execute(statement)
        record = result.scalar_one_or_none()
        if not record:
            raise ContentGenerationJobNotFoundException(job_id)
        return record
