import public
from pydantic import BaseModel

from src.shared.model import ContentChannelName, ContentFormat


@public.add
class TextWithSingleImageContent(BaseModel):
    text: str
    image_url: str
    channel: ContentChannelName
    content_type: ContentFormat
