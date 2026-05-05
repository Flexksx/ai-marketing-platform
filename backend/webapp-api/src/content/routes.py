from datetime import datetime

from fastapi import APIRouter, Depends, Query

import src.content.service as content_service
from lib.model import ContentChannelName
from src.auth_access import validate_brand_access
from src.content.model import (
    ContentListRequest,
    ContentResponse,
)


router = APIRouter(tags=["Brand Content"])


@router.get("", response_model=list[ContentResponse])
async def search(
    brand_id: str = Depends(validate_brand_access),
    scheduled_after: datetime | None = Query(None),  # noqa: B008
    scheduled_before: datetime | None = Query(None),  # noqa: B008
    limit: int = Query(10, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    channel: ContentChannelName | None = Query(None),  # noqa: B008
):
    return await content_service.search(
        ContentListRequest(
            brand_id=brand_id,
            scheduled_after=scheduled_after,
            scheduled_before=scheduled_before,
            channel=channel,
            limit=limit,
            offset=offset,
        ),
    )
