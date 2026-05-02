from beartype.typing import Final

from webapp_api_contract.shared import (
    ContentChannel,
    ContentChannelImageSpecification,
    ContentChannelName,
    ContentFormat,
    ImageAspectRatio,
    ImageResolution,
)


INSTAGRAM_CONTENT_CHANNEL: Final[ContentChannel] = ContentChannel(
    name=ContentChannelName.INSTAGRAM,
    allowed_content_formats=[ContentFormat.TEXT_WITH_SINGLE_IMAGE],
    image_specification=ContentChannelImageSpecification(
        aspect_ratio=ImageAspectRatio.SQUARE,
        resolution=ImageResolution.STANDARD,
    ),
)


LINKEDIN_CONTENT_CHANNEL: Final[ContentChannel] = ContentChannel(
    name=ContentChannelName.LINKEDIN,
    allowed_content_formats=[ContentFormat.TEXT, ContentFormat.TEXT_WITH_SINGLE_IMAGE],
    image_specification=ContentChannelImageSpecification(
        aspect_ratio=ImageAspectRatio.LANDSCAPE_4_3,
        resolution=ImageResolution.STANDARD,
    ),
)


AVAILABLE_CONTENT_CHANNELS: Final[list[ContentChannel]] = [
    INSTAGRAM_CONTENT_CHANNEL,
    LINKEDIN_CONTENT_CHANNEL,
]
