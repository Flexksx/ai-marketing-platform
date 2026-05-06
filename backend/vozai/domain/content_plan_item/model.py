from datetime import datetime

import public
from pydantic import BaseModel, ConfigDict

from vozai.domain.brand_settings.content_pillar.model import ContentTypeName
from vozai.domain.content.model import ContentData
from vozai.domain.content_channel.model import ContentChannelName, ContentFormat
from vozai.lib.job import JobStatus


@public.add
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
