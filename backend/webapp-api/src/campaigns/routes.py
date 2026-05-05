from fastapi import APIRouter, Depends, Path, Query

import src.campaigns.service as campaign_service
from src.auth_access import validate_brand_access
from src.campaigns.entity import CampaignState
from src.campaigns.model import CampaignListRequest, CampaignResponse


router = APIRouter(tags=["Brand Campaigns"])


@router.get("", response_model=list[CampaignResponse])
async def list(
    brand_id: str = Depends(validate_brand_access),
    state: CampaignState | None = Query(None),  # noqa: B008
    limit: int = Query(5, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    return await campaign_service.search(
        CampaignListRequest(brand_id=brand_id, state=state, limit=limit, offset=offset),
    )


@router.delete("/{campaign_id}")
async def delete_campaign(
    brand_id: str = Depends(validate_brand_access),  # noqa: ARG001
    campaign_id: str = Path(...),
):
    return await campaign_service.delete(campaign_id)
