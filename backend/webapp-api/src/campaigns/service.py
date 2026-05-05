import src.campaigns.repository as campaign_repository
from src.campaigns.model import (
    Campaign,
    CampaignCreateRequest,
    CampaignListRequest,
    CampaignUpdateRequest,
)


async def create(request: CampaignCreateRequest) -> Campaign:
    return await campaign_repository.create(request)


async def get(campaign_id: str) -> Campaign | None:
    return await campaign_repository.get(campaign_id)


async def search(request: CampaignListRequest) -> list[Campaign]:
    return await campaign_repository.search(request)


async def update(campaign_id: str, request: CampaignUpdateRequest) -> Campaign | None:
    return await campaign_repository.update(campaign_id, request)


async def remove(campaign_id: str) -> None:
    await campaign_repository.remove(campaign_id)
