from typing import ClassVar

import public

from vozai.domain.content_channel.model import (
    ContentChannel,
    ContentChannelImageSpecification,
    ContentChannelName,
    ContentFormat,
)
from vozai.domain.image_generation import ImageAspectRatio, ImageResolution


@public.add
class ContentChannelService:
    __INSTAGRAM_CONTENT_CHANNEL = ContentChannel(
        name=ContentChannelName.INSTAGRAM,
        allowed_content_formats=[ContentFormat.TEXT_WITH_SINGLE_IMAGE],
        image_specification=ContentChannelImageSpecification(
            aspect_ratio=ImageAspectRatio.SQUARE,
            resolution=ImageResolution.STANDARD,
        ),
    )
    __LINKEDIN_CONTENT_CHANNEL = ContentChannel(
        name=ContentChannelName.LINKEDIN,
        allowed_content_formats=[
            ContentFormat.TEXT_WITH_SINGLE_IMAGE,
            ContentFormat.TEXT,
        ],
        image_specification=ContentChannelImageSpecification(
            aspect_ratio=ImageAspectRatio.LANDSCAPE_4_3,
            resolution=ImageResolution.STANDARD,
        ),
    )

    __CHANNELS_DATA: ClassVar[dict[ContentChannelName, ContentChannel]] = {
        ContentChannelName.INSTAGRAM: __INSTAGRAM_CONTENT_CHANNEL,
        ContentChannelName.LINKEDIN: __LINKEDIN_CONTENT_CHANNEL,
    }

    def get(self, name: ContentChannelName) -> ContentChannel:
        return self.__CHANNELS_DATA[name]

    def search(self) -> list[ContentChannel]:
        return list(self.__CHANNELS_DATA.values())
