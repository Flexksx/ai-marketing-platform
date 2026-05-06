import public
from pydantic import BaseModel, ConfigDict, Field


@public.add
class PositioningBrandData(BaseModel):
    description: str = Field(default="")
    points_of_difference: list[str] = Field(default_factory=list)
    points_of_parity: list[str] = Field(default_factory=list)
    product_description: str = Field(default="")

    model_config = ConfigDict(from_attributes=True)
