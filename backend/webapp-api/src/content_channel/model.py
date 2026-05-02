from enum import StrEnum

import public
from pydantic import BaseModel, ConfigDict

from webapp_api_contract.shared import ImageAspectRatio, ImageResolution


@public.add
class ContentChannelName(StrEnum):
    INSTAGRAM = "INSTAGRAM"
    LINKEDIN = "LINKEDIN"


@public.add
class ContentFormat(StrEnum):
    TEXT = "TEXT"
    TEXT_WITH_SINGLE_IMAGE = "TEXT_WITH_SINGLE_IMAGE"


@public.add
class ContentChannelImageSpecification(BaseModel):
    aspect_ratio: ImageAspectRatio
    resolution: ImageResolution

    model_config = ConfigDict(from_attributes=True)


@public.add
class ContentChannel(BaseModel):
    name: ContentChannelName
    allowed_content_formats: list[ContentFormat]
    image_specification: ContentChannelImageSpecification

    model_config = ConfigDict(from_attributes=True)
