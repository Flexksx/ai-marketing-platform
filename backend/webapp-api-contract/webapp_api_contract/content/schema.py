from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from webapp_api_contract.content.model import ContentData
from webapp_api_contract.shared import ContentChannelName, ContentFormat


class ContentCreateRequest(BaseModel):
    brand_id: str
    campaign_id: str | None
    channel: ContentChannelName
    content_format: ContentFormat
    data: ContentData
    scheduled_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ContentUpdateRequest(BaseModel):
    channel: ContentChannelName | None = None
    content_format: ContentFormat | None = None
    data: ContentData | None = None
    scheduled_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class ContentListRequest(BaseModel):
    brand_id: str | None = None
    campaign_id: str | None = None
    channel: ContentChannelName | None = None
    scheduled_after: datetime | None = None
    scheduled_before: datetime | None = None
    limit: int | None = Field(default=10, ge=1, le=100)
    offset: int | None = Field(default=0, ge=0)

    model_config = ConfigDict(from_attributes=True)


class ContentResponse(BaseModel):
    id: str
    brand_id: str
    campaign_id: str | None = None
    channel: ContentChannelName
    content_format: ContentFormat
    data: ContentData
    scheduled_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
