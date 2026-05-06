from enum import Enum

import public
from pydantic import BaseModel


@public.add
class StorageBucket(str, Enum):
    POSTS = "posts"
    BRAND_EXTRACTION = "brand-extraction"
    BRAND_LOGOS = "brand_logos"
    CAMPAIGN_USER_MEDIA = "campaign_user_media"
    CONTENT_GENERATION_JOBS_USER_MEDIA = "content_generation_jobs_user_media"
    CONTENT_GENERATION_AI_IMAGES = "content_generation_ai_images"


@public.add
class StorageUploadRequest(BaseModel):
    bucket: StorageBucket
    path: str
    content: bytes
    content_type: str | None = None


@public.add
class ImageByUrlStorageUploadRequest(BaseModel):
    bucket: StorageBucket
    image_url: str
    path_prefix: str = ""


@public.add
class StorageUploadResult(BaseModel):
    path: str
    public_url: str
