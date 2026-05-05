from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class JobStatus(StrEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"
    ACCEPTED = "accepted"


class ContentChannelName(StrEnum):
    INSTAGRAM = "INSTAGRAM"
    LINKEDIN = "LINKEDIN"


class ContentFormat(StrEnum):
    TEXT = "TEXT"
    TEXT_WITH_SINGLE_IMAGE = "TEXT_WITH_SINGLE_IMAGE"


class ImageAspectRatio(StrEnum):
    SQUARE = "1:1"
    PORTRAIT_4_5 = "4:5"
    PORTRAIT_3_4 = "3:4"
    PORTRAIT_2_3 = "2:3"
    PORTRAIT_9_16 = "9:16"
    LANDSCAPE_16_9 = "16:9"
    LANDSCAPE_4_3 = "4:3"
    LANDSCAPE_3_2 = "3:2"
    LANDSCAPE_5_4 = "5:4"
    LANDSCAPE_21_9 = "21:9"


class ImageResolution(StrEnum):
    STANDARD = "1K"
    HIGH = "2K"


class ContentChannelImageSpecification(BaseModel):
    aspect_ratio: ImageAspectRatio
    resolution: ImageResolution

    model_config = ConfigDict(from_attributes=True)


class ContentChannel(BaseModel):
    name: ContentChannelName
    allowed_content_formats: list[ContentFormat]
    image_specification: ContentChannelImageSpecification

    model_config = ConfigDict(from_attributes=True)


class ContentGenerationJobWorkflowType(StrEnum):
    TEXT_ONLY = "TEXT_ONLY"
    TEXT_WITH_SINGLE_IMAGE_FROM_USER_MEDIA = "TEXT_WITH_SINGLE_IMAGE_FROM_USER_MEDIA"
    TEXT_WITH_SINGLE_IMAGE_AI_GENERATED = "TEXT_WITH_SINGLE_IMAGE_AI_GENERATED"
    TEXT_WITH_SINGLE_IMAGE_PRODUCT_LIFESTYLE = (
        "TEXT_WITH_SINGLE_IMAGE_PRODUCT_LIFESTYLE"
    )


class CampaignGenerationJobWorkflowType(StrEnum):
    USER_MEDIA_ONLY = "USER_MEDIA_ONLY"
    AI_GENERATED = "AI_GENERATED"
    PRODUCT_LIFESTYLE = "PRODUCT_LIFESTYLE"
