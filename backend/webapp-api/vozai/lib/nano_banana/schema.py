from pydantic import BaseModel, Field


class NanoBananaRequest(BaseModel):
    prompt: str = Field(..., description="The text prompt for image generation")
    image_urls: list[str] = Field(
        default_factory=list, description="List of image URLs to use as input"
    )
    aspect_ratio: str = Field(
        default="1:1", description="Aspect ratio for the generated image"
    )
    image_size: str = Field(
        default="1K", description="Resolution of the generated image"
    )


class NanoBananaResponse(BaseModel):
    image_data_base64: str = Field(
        ..., description="The generated image data encoded in base64"
    )
    mime_type: str = Field(
        default="image/png", description="The mime type of the image"
    )
