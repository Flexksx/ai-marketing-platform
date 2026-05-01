from pydantic import BaseModel


class CampaignGenerationTaskPayload(BaseModel):
    job_id: str
    user_id: str


class BrandGenerationTaskPayload(BaseModel):
    job_id: str


class PostGenerationTaskPayload(BaseModel):
    job_id: str
    user_id: str
    brand_brief: str
    campaign_brief: str
    channel: str
    topic: str
    image_url: str
    scheduled_at: str


class ContentGenerationTaskPayload(BaseModel):
    job_id: str
