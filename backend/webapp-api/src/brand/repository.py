import builtins

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from lib.db.session_manager import get_session
from lib.utils import new_id
from src.brand.entity import BrandRecord
from src.brand.errors import BrandNotFoundError
from src.brand.model import (
    Brand,
    BrandCreateRequest,
    BrandSearchRequest,
    BrandUpdateRequest,
)


async def create(
    user_id: str,
    request: BrandCreateRequest,
) -> Brand:
    async with get_session() as session:
        brand_record = BrandRecord(
            id=new_id(),
            user_id=user_id,
            name=request.name,
            data=request.data.model_dump(mode="json"),
        )
        session.add(brand_record)
        await session.commit()
        await session.refresh(brand_record)
        return Brand.model_validate(brand_record, from_attributes=True)


async def get(brand_id: str) -> Brand:
    async with get_session() as session:
        brand_record = await _record_by_id(session, brand_id)
        return Brand.model_validate(brand_record, from_attributes=True)


async def search(
    request: BrandSearchRequest,
) -> builtins.list[Brand]:
    async with get_session() as session:
        statement = select(BrandRecord).filter(BrandRecord.user_id == request.user_id)
        if request.name:
            statement = statement.filter(BrandRecord.name.ilike(f"%{request.name}%"))
        statement = (
            statement.order_by(desc(BrandRecord.created_at))
            .limit(request.limit)
            .offset(request.offset)
        )
        result = await session.execute(statement)
        brand_records = result.scalars().all()
        return [
            Brand.model_validate(brand_record, from_attributes=True)
            for brand_record in brand_records
        ]


async def update(
    brand_id: str,
    request: BrandUpdateRequest,
) -> Brand:
    async with get_session() as session:
        brand_record = await _record_by_id(session, brand_id)
        brand_record_data = brand_record.data
        if brand_record_data is None:
            brand_record_data = {}
        if request.name is not None:
            brand_record.name = request.name  # ty:ignore[invalid-assignment]
        if request.data is not None:
            current = (brand_record.data or {}).copy()
            data_update = request.data.model_dump(mode="json", exclude_unset=True)
            for key, value in data_update.items():
                current[key] = value  # ty:ignore[invalid-assignment]
            brand_record.data = current  # ty:ignore[invalid-assignment]
        await session.commit()
        await session.refresh(brand_record)
        return Brand.model_validate(brand_record, from_attributes=True)


async def remove(brand_id: str) -> Brand:
    async with get_session() as session:
        brand_record = await _record_by_id(session, brand_id)
        await session.delete(brand_record)
        await session.commit()
        return Brand.model_validate(brand_record, from_attributes=True)


async def exists_for_user(
    brand_id: str,
    user_id: str,
) -> bool:
    async with get_session() as session:
        statement = select(BrandRecord).filter(
            BrandRecord.id == brand_id,
            BrandRecord.user_id == user_id,
        )
        result = await session.execute(statement)
        return result.scalar_one_or_none() is not None


async def _record_by_id(session: AsyncSession, brand_id: str) -> BrandRecord:
    statement = select(BrandRecord).filter(BrandRecord.id == brand_id)
    result = await session.execute(statement)
    record = result.scalar_one_or_none()
    if not record:
        raise BrandNotFoundError(brand_id)
    return record
