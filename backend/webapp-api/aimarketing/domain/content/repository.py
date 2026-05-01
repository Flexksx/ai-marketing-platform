import public
from fastapi import Depends
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.session_factory import DbSessionFactory
from aimarketing.domain.content.entity import ContentRecord
from aimarketing.domain.content.errors import ContentNotFoundException
from aimarketing.domain.content.model import Content
from aimarketing.domain.content.schema import (
    ContentCreateRequest,
    ContentListRequest,
    ContentUpdateRequest,
)
from aimarketing.utils import new_id


@public.add
class ContentRepository:
    def __init__(self, session_factory: DbSessionFactory = Depends()):
        self._session_factory = session_factory

    async def create(self, request: ContentCreateRequest) -> Content:
        async with self._session_factory.session() as session:
            record = ContentRecord(
                id=new_id(),
                brand_id=request.brand_id,
                campaign_id=request.campaign_id,
                channel=request.channel,
                content_format=request.content_format,
                data=request.data.model_dump(mode="json"),
                scheduled_at=request.scheduled_at,
            )
            session.add(record)
            await session.commit()
            await session.refresh(record)
            return Content.model_validate(record)

    async def get(self, post_id: str) -> Content:
        async with self._session_factory.session() as session:
            post_record = await self._get_by_id(session, post_id)
            return Content.model_validate(post_record)

    async def search(self, request: ContentListRequest) -> list[Content]:
        async with self._session_factory.session() as session:
            stmt = select(ContentRecord)
            if request.brand_id:
                stmt = stmt.filter(ContentRecord.brand_id == request.brand_id)
            if request.campaign_id:
                stmt = stmt.filter(ContentRecord.campaign_id == request.campaign_id)
            if request.scheduled_after:
                stmt = stmt.filter(
                    ContentRecord.scheduled_at >= request.scheduled_after
                )
            if request.scheduled_before:
                stmt = stmt.filter(
                    ContentRecord.scheduled_at <= request.scheduled_before
                )
            if request.channel:
                stmt = stmt.filter(ContentRecord.channel == request.channel)
            stmt = (
                stmt.order_by(desc(ContentRecord.created_at))
                .limit(request.limit)
                .offset(request.offset)
            )
            result = await session.execute(stmt)
            post_records = result.scalars().all()
            return [Content.model_validate(post_record) for post_record in post_records]

    async def update(self, post_id: str, request: ContentUpdateRequest) -> Content:
        async with self._session_factory.session() as session:
            post_record = await self._get_by_id(session, post_id)
            update_data = request.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(post_record, key, value)
            await session.commit()
            await session.refresh(post_record)
            return Content.model_validate(post_record)

    async def _get_by_id(self, session: AsyncSession, post_id: str) -> ContentRecord:
        stmt = select(ContentRecord).filter(ContentRecord.id == post_id)
        result = await session.execute(stmt)
        record = result.scalar_one_or_none()
        if not record:
            raise ContentNotFoundException(post_id)
        return record
