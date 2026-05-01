from datetime import datetime
from typing import Annotated, Literal

import public
from pydantic import BaseModel, ConfigDict, Field

from aimarketing.domain.content_channel import ContentFormat
from aimarketing.domain.content_channel.model import ContentChannelName


@public.add
class TextWithSingleImageContentData(BaseModel):
    caption: str
    image_url: str
    content_format: Literal[ContentFormat.TEXT_WITH_SINGLE_IMAGE] = (
        ContentFormat.TEXT_WITH_SINGLE_IMAGE
    )


@public.add
class TextOnlyContentData(BaseModel):
    caption: str
    content_format: Literal[ContentFormat.TEXT] = ContentFormat.TEXT


ContentData = Annotated[
    TextWithSingleImageContentData | TextOnlyContentData,
    Field(discriminator="content_format"),
]


@public.add
class Content(BaseModel):
    id: str
    brand_id: str
    campaign_id: str | None = None
    channel: ContentChannelName
    content_format: ContentFormat
    data: ContentData
    created_at: datetime
    updated_at: datetime
    scheduled_at: datetime

    model_config = ConfigDict(from_attributes=True)
