from fastapi import Depends

from aimarketing.domain.campaign.model import Campaign
from aimarketing.domain.campaign.repository import CampaignRepository
from aimarketing.domain.campaign.schema import (
    CampaignCreateRequest,
    CampaignListRequest,
    CampaignUpdateRequest,
)


class CampaignService:
    def __init__(self, repository: CampaignRepository = Depends()):
        self.repository = repository

    async def create(self, request: CampaignCreateRequest) -> Campaign:
        return await self.repository.create(request)

    async def get(self, campaign_id: str) -> Campaign | None:
        return await self.repository.get(campaign_id)

    async def search(self, request: CampaignListRequest) -> list[Campaign]:
        return await self.repository.search(request)

    async def update(
        self, campaign_id: str, request: CampaignUpdateRequest
    ) -> Campaign | None:
        return await self.repository.update(campaign_id, request)

    async def delete(self, campaign_id: str) -> None:
        await self.repository.delete(campaign_id)
