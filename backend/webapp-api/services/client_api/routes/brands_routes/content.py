from datetime import datetime

from fastapi import APIRouter, Depends, Query

from services.client_api.auth.access_validation import validate_brand_access
from aimarketing.domain.content.schema import (
    ContentListRequest,
    ContentResponse,
)
from aimarketing.domain.content.service import ContentService
from aimarketing.domain.content_channel.model import ContentChannelName


router = APIRouter(tags=["Brand Content"])


@router.get("", response_model=list[ContentResponse])
async def search(
    brand_id: str = Depends(validate_brand_access),
    scheduled_after: datetime | None = Query(None),  # noqa: B008
    scheduled_before: datetime | None = Query(None),  # noqa: B008
    limit: int = Query(10, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    channel: ContentChannelName | None = Query(None),  # noqa: B008
    post_service: ContentService = Depends(),
):
    return await post_service.search(
        ContentListRequest(
            brand_id=brand_id,
            scheduled_after=scheduled_after,
            scheduled_before=scheduled_before,
            channel=channel,
            limit=limit,
            offset=offset,
        )
    )
