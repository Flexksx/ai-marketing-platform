from fastapi import APIRouter, Depends, Path, Query

from services.client_api.auth.access_validation import validate_brand_access
from aimarketing.domain.campaign.entity import CampaignState
from aimarketing.domain.campaign.schema import CampaignListRequest, CampaignResponse
from aimarketing.domain.campaign.service import CampaignService


router = APIRouter(tags=["Brand Campaigns"])


@router.get("", response_model=list[CampaignResponse])
async def list(
    brand_id: str = Depends(validate_brand_access),
    state: CampaignState | None = Query(None),  # noqa: B008
    limit: int = Query(5, ge=1, le=100),
    offset: int = Query(0, ge=0),
    campaign_service: CampaignService = Depends(),
):
    return await campaign_service.search(
        CampaignListRequest(
            brand_id=brand_id,
            state=state,
            limit=limit,
            offset=offset,
        )
    )


@router.delete("/{campaign_id}")
async def delete_campaign(
    brand_id: str = Depends(validate_brand_access),  # noqa: ARG001
    campaign_id: str = Path(...),
    campaign_service: CampaignService = Depends(),
):
    return await campaign_service.delete(campaign_id)
