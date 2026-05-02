from sqlalchemy import delete, desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from lib.db.session_factory import DbSessionFactory
from src.campaigns.entity import CampaignRecord, CampaignState
from webapp_api_contract.campaigns import Campaign
from webapp_api_contract.campaigns import (
    CampaignCreateRequest,
    CampaignListRequest,
    CampaignUpdateRequest,
)
from lib.utils import new_id


async def create(
    session_factory: DbSessionFactory,
    request: CampaignCreateRequest,
) -> Campaign:
    async with session_factory.session() as session:
        campaign_record = CampaignRecord(
            id=new_id(),
            brand_id=request.brand_id,
            state=CampaignState.DRAFT,
            data=request.data.model_dump(mode="json"),
        )
        session.add(campaign_record)
        await session.commit()
        await session.refresh(campaign_record)
        return Campaign.model_validate(campaign_record, from_attributes=True)


async def get(
    session_factory: DbSessionFactory,
    campaign_id: str,
) -> Campaign | None:
    async with session_factory.session() as session:
        campaign_record = await _record_by_id(session, campaign_id)
        if not campaign_record:
            return None
        return Campaign.model_validate(campaign_record, from_attributes=True)


async def search(
    session_factory: DbSessionFactory,
    request: CampaignListRequest,
) -> list[Campaign]:
    async with session_factory.session() as session:
        stmt = select(CampaignRecord).filter(
            CampaignRecord.brand_id == request.brand_id
        )
        if request.state:
            stmt = stmt.filter(CampaignRecord.state == request.state)
        stmt = (
            stmt.order_by(desc(CampaignRecord.created_at))
            .limit(request.limit)
            .offset(request.offset)
        )
        result = await session.execute(stmt)
        campaign_records = result.scalars().all()
        return [
            Campaign.model_validate(campaign_record, from_attributes=True)
            for campaign_record in campaign_records
        ]


async def update(
    session_factory: DbSessionFactory,
    campaign_id: str,
    request: CampaignUpdateRequest,
) -> Campaign | None:
    async with session_factory.session() as session:
        campaign_record = await _record_by_id(session, campaign_id)
        if not campaign_record:
            return None
        if request.state is not None:
            campaign_record.state = request.state
        if request.data is not None:
            current = (campaign_record.data or {}).copy()
            data_update = request.data.model_dump(mode="json", exclude_unset=True)
            for key, value in data_update.items():
                current[key] = value  # ty:ignore[invalid-assignment]
            campaign_record.data = current
        await session.commit()
        await session.refresh(campaign_record)
        return Campaign.model_validate(campaign_record, from_attributes=True)


async def delete(session_factory: DbSessionFactory, campaign_id: str) -> None:
    async with session_factory.session() as session:
        campaign_record = await _record_by_id(session, campaign_id)
        if not campaign_record:
            raise ValueError(f"Campaign not found: {campaign_id}")
        stmt = delete(CampaignRecord).where(CampaignRecord.id == campaign_id)
        await session.execute(stmt)
        await session.commit()


async def _record_by_id(
    session: AsyncSession,
    campaign_id: str,
) -> CampaignRecord | None:
    stmt = select(CampaignRecord).filter(CampaignRecord.id == campaign_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
