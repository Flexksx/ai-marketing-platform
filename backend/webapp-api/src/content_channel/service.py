from lib.model import ContentChannelName, ContentFormat
from src.content_channel.model import (
    ContentChannel,
    ContentChannelImageSpecification,
    ImageAspectRatio,
    ImageResolution,
)


_INSTAGRAM_CONTENT_CHANNEL = ContentChannel(
    name=ContentChannelName.INSTAGRAM,
    allowed_content_formats=[ContentFormat.TEXT_WITH_SINGLE_IMAGE],
    image_specification=ContentChannelImageSpecification(
        aspect_ratio=ImageAspectRatio.SQUARE,
        resolution=ImageResolution.STANDARD,
    ),
)
_LINKEDIN_CONTENT_CHANNEL = ContentChannel(
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

_CHANNELS_DATA: dict[ContentChannelName, ContentChannel] = {
    ContentChannelName.INSTAGRAM: _INSTAGRAM_CONTENT_CHANNEL,
    ContentChannelName.LINKEDIN: _LINKEDIN_CONTENT_CHANNEL,
}


def get(name: ContentChannelName) -> ContentChannel:
    return _CHANNELS_DATA[name]


def search() -> list[ContentChannel]:
    return list(_CHANNELS_DATA.values())
