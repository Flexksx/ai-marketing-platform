from datetime import datetime

import public
from pydantic import BaseModel, ConfigDict

from webapp_api_contract.brand_settings import ContentTypeName
from webapp_api_contract.content import ContentData
from webapp_api_contract.shared import ContentChannelName, ContentFormat, JobStatus


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
