from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from src.brand.model import ContentTypeName
from src.content.model import ContentData
from src.shared.model import ContentChannelName, ContentFormat, JobStatus


class ContentPlanItem(BaseModel):
    id: str
    job_id: str
    description: str
    channel: ContentChannelName
    content_type: ContentTypeName
    content_format: ContentFormat
    image_urls: list[str] = []
    scheduled_at: datetime
    content_data: ContentData | None = None
    status: JobStatus = JobStatus.PENDING

    model_config = ConfigDict(from_attributes=True)


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


class RestContentPlanItemUpdateRequest(BaseModel):
    scheduled_at: datetime | None = None
    content_data: ContentData | None = None
