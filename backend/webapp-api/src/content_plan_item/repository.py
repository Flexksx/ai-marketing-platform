from datetime import UTC

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lib.db.session_manager import get_session
from lib.utils import new_id
from src.content_plan_item.entity import ContentPlanItemRecord
from src.content_plan_item.errors import ContentPlanItemNotFoundException
from src.content_plan_item.model import (
    ContentPlanItem,
    ContentPlanItemCreateRequest,
    ContentPlanItemUpdateRequest,
)


async def create(
    request: ContentPlanItemCreateRequest,
) -> ContentPlanItem:
    async with get_session() as session:
        record = ContentPlanItemRecord(
            id=new_id(),
            job_id=request.job_id,
            description=request.description,
            channel=request.channel,
            content_type=request.content_type,
            content_format=request.content_format,
            image_urls=request.image_urls,
            status=request.status,
            scheduled_at=request.scheduled_at,
            content_data=(
                request.content_data.model_dump(mode="json")
                if request.content_data
                else None
            ),
        )
        session.add(record)
        await session.commit()
        await session.refresh(record)
        return ContentPlanItem.model_validate(record)


async def create_many(
    requests: list[ContentPlanItemCreateRequest],
) -> list[ContentPlanItem]:
    if not requests:
        return []

    async with get_session() as session:
        records: list[ContentPlanItemRecord] = []
        for request in requests:
            record = ContentPlanItemRecord(
                id=new_id(),
                job_id=request.job_id,
                description=request.description,
                channel=request.channel,
                content_type=request.content_type,
                content_format=request.content_format,
                image_urls=request.image_urls,
                status=request.status,
                scheduled_at=request.scheduled_at,
                content_data=(
                    request.content_data.model_dump(mode="json")
                    if request.content_data
                    else None
                ),
            )
            session.add(record)
            records.append(record)

        await session.commit()

        for record in records:
            await session.refresh(record)

        return [ContentPlanItem.model_validate(record) for record in records]


async def get(item_id: str) -> ContentPlanItem:
    async with get_session() as session:
        record = await _record_by_id(session, item_id)
        return ContentPlanItem.model_validate(record)


async def search(job_id: str) -> list[ContentPlanItem]:
    async with get_session() as session:
        stmt = (
            select(ContentPlanItemRecord)
            .where(ContentPlanItemRecord.job_id == job_id)
            .order_by(ContentPlanItemRecord.scheduled_at)
        )
        result = await session.execute(stmt)
        records = result.scalars().all()
        return [ContentPlanItem.model_validate(record) for record in records]


async def update(
    item_id: str,
    request: ContentPlanItemUpdateRequest,
) -> ContentPlanItem:
    async with get_session() as session:
        record = await _record_by_id(session, item_id)

        update_data = request.model_dump(exclude_unset=True, exclude={"content_data"})

        for key, value in update_data.items():
            if key != "scheduled_at":
                setattr(record, key, value)
                continue
            if value is None:
                record.scheduled_at = None
                continue
            if value.tzinfo is None:
                record.scheduled_at = value.replace(tzinfo=UTC)
                continue
            record.scheduled_at = value.astimezone(UTC)

        if "content_data" in request.model_fields_set:
            record.content_data = (
                request.content_data.model_dump(mode="json")
                if request.content_data
                else None
            )

        await session.commit()
        await session.refresh(record)
        return ContentPlanItem.model_validate(record)


async def remove(item_id: str) -> None:
    async with get_session() as session:
        record = await _record_by_id(session, item_id)
        await session.delete(record)
        await session.commit()


async def _record_by_id(session: AsyncSession, item_id: str) -> ContentPlanItemRecord:
    stmt = select(ContentPlanItemRecord).where(ContentPlanItemRecord.id == item_id)
    result = await session.execute(stmt)
    record = result.scalar_one_or_none()
    if not record:
        raise ContentPlanItemNotFoundException(item_id)
    return record
