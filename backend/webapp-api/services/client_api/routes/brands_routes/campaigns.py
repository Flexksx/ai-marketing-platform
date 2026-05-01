from fastapi import APIRouter, Depends, Path, Query

from db.session_factory import DbSessionFactory
from services.client_api.auth.access_validation import validate_brand_access
import vozai.domain.campaign.service as campaign_service
from vozai.domain.campaign.entity import CampaignState
from vozai.domain.campaign.schema import CampaignListRequest, CampaignResponse


router = APIRouter(tags=["Brand Campaigns"])


@router.get("", response_model=list[CampaignResponse])
async def list(
    brand_id: str = Depends(validate_brand_access),
    state: CampaignState | None = Query(None),  # noqa: B008
    limit: int = Query(5, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session_factory: DbSessionFactory = Depends(),
):
    return await campaign_service.search(
        session_factory,
        CampaignListRequest(
            brand_id=brand_id,
            state=state,
            limit=limit,
            offset=offset,
        ),
    )


@router.delete("/{campaign_id}")
async def delete_campaign(
    brand_id: str = Depends(validate_brand_access),  # noqa: ARG001
    campaign_id: str = Path(...),
    session_factory: DbSessionFactory = Depends(),
):
    return await campaign_service.delete(session_factory, campaign_id)
