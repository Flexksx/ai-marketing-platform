import public
from fastapi import Depends
from sqlalchemy import delete, desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.session_factory import DbSessionFactory
from aimarketing.domain.campaign.entity import CampaignRecord, CampaignState
from aimarketing.domain.campaign.model import Campaign
from aimarketing.domain.campaign.schema import (
    CampaignCreateRequest,
    CampaignListRequest,
    CampaignUpdateRequest,
)
from aimarketing.utils import new_id


@public.add
class CampaignRepository:
    def __init__(self, session_factory: DbSessionFactory = Depends()):
        self._session_factory = session_factory

    async def create(self, request: CampaignCreateRequest) -> Campaign:
        async with self._session_factory.session() as session:
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

    async def get(self, campaign_id: str) -> Campaign | None:
        async with self._session_factory.session() as session:
            campaign_record = await self._get_by_id(session, campaign_id)
            if not campaign_record:
                return None
            return Campaign.model_validate(campaign_record, from_attributes=True)

    async def search(self, request: CampaignListRequest) -> list[Campaign]:
        async with self._session_factory.session() as session:
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
        self, campaign_id: str, request: CampaignUpdateRequest
    ) -> Campaign | None:
        async with self._session_factory.session() as session:
            campaign_record = await self._get_by_id(session, campaign_id)
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

    async def delete(self, campaign_id: str) -> None:
        async with self._session_factory.session() as session:
            campaign_record = await self._get_by_id(session, campaign_id)
            if not campaign_record:
                raise ValueError(f"Campaign not found: {campaign_id}")
            stmt = delete(CampaignRecord).where(CampaignRecord.id == campaign_id)
            await session.execute(stmt)
            await session.commit()

    async def _get_by_id(
        self, session: AsyncSession, campaign_id: str
    ) -> CampaignRecord | None:
        stmt = select(CampaignRecord).filter(CampaignRecord.id == campaign_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
