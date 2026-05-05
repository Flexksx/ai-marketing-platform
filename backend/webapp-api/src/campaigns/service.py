import src.campaigns.repository as campaign_repository
from lib.db.session_factory import DbSessionFactory
from src.campaigns.model import (
    Campaign,
    CampaignCreateRequest,
    CampaignListRequest,
    CampaignUpdateRequest,
)


async def create(
    session_factory: DbSessionFactory,
    request: CampaignCreateRequest,
) -> Campaign:
    return await campaign_repository.create(session_factory, request)


async def get(
    session_factory: DbSessionFactory,
    campaign_id: str,
) -> Campaign | None:
    return await campaign_repository.get(session_factory, campaign_id)


async def search(
    session_factory: DbSessionFactory,
    request: CampaignListRequest,
) -> list[Campaign]:
    return await campaign_repository.search(session_factory, request)


async def update(
    session_factory: DbSessionFactory,
    campaign_id: str,
    request: CampaignUpdateRequest,
) -> Campaign | None:
    return await campaign_repository.update(session_factory, campaign_id, request)


async def delete(session_factory: DbSessionFactory, campaign_id: str) -> None:
    await campaign_repository.delete(session_factory, campaign_id)
