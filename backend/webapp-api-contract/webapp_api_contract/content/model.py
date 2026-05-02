from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

from webapp_api_contract.shared import ContentChannelName, ContentFormat


class TextWithSingleImageContentData(BaseModel):
    caption: str
    image_url: str
    content_format: Literal[ContentFormat.TEXT_WITH_SINGLE_IMAGE] = (
        ContentFormat.TEXT_WITH_SINGLE_IMAGE
    )

    model_config = ConfigDict(from_attributes=True)


class TextOnlyContentData(BaseModel):
    caption: str
    content_format: Literal[ContentFormat.TEXT] = ContentFormat.TEXT

    model_config = ConfigDict(from_attributes=True)


ContentData = TextWithSingleImageContentData | TextOnlyContentData


class Content(BaseModel):
    id: str
    brand_id: str
    campaign_id: str | None = None
    channel: ContentChannelName
    content_format: ContentFormat
    data: ContentData
    created_at: datetime
    updated_at: datetime
    scheduled_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
