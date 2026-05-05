from enum import Enum

from pydantic import BaseModel


class StorageBucket(str, Enum):
    POSTS = "posts"
    BRAND_EXTRACTION = "brand-extraction"
    BRAND_LOGOS = "brand_logos"
    CAMPAIGN_USER_MEDIA = "campaign_user_media"
    CONTENT_GENERATION_JOBS_USER_MEDIA = "content_generation_jobs_user_media"
    CONTENT_GENERATION_AI_IMAGES = "content_generation_ai_images"


class StorageUploadRequest(BaseModel):
    bucket: StorageBucket
    path: str
    content: bytes
    content_type: str | None = None


class ImageByUrlStorageUploadRequest(BaseModel):
    bucket: StorageBucket
    image_url: str
    path_prefix: str = ""


class StorageUploadResult(BaseModel):
    path: str
    public_url: str
