from datetime import datetime

import public
from pydantic import BaseModel, ConfigDict, Field

from vozai.domain.brand_settings.content_pillar.model import ContentTypeName
from vozai.domain.content.model import ContentData
from vozai.domain.content_channel.model import ContentChannelName, ContentFormat
from vozai.lib.job import JobStatus


@public.add
class ContentPlanItemCreateRequest(BaseModel):
    job_id: str
    description: str
    channel: ContentChannelName
    content_type: ContentTypeName
    content_format: ContentFormat
    image_urls: list[str] = Field(default_factory=list)
    scheduled_at: datetime
    content_data: ContentData | None = Field(default=None)
    status: JobStatus = Field(default=JobStatus.PENDING)

    model_config = ConfigDict(from_attributes=True)


@public.add
class ContentPlanItemUpdateRequest(BaseModel):
    description: str | None = None
    channel: ContentChannelName | None = None
    content_type: ContentTypeName | None = None
    content_format: ContentFormat | None = None
    image_urls: list[str] | None = None
    scheduled_at: datetime | None = None
    content_data: ContentData | None = None
    status: JobStatus | None = None

    model_config = ConfigDict(from_attributes=True)


@public.add
class RestContentPlanItemUpdateRequest(BaseModel):
    scheduled_at: datetime | None = None
    content_data: ContentData | None = None

    model_config = ConfigDict(from_attributes=True)
