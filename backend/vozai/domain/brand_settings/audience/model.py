import public
from pydantic import BaseModel, ConfigDict, Field
from strenum import StrEnum

from vozai.domain.content_channel import ContentChannelName
from vozai.utils import new_id


@public.add
class BrandAudienceAgeRange(StrEnum):
    TEENS = "TEENS"
    YOUNG_ADULTS = "YOUNG_ADULTS"
    ADULTS = "ADULTS"
    MIDDLE_AGED = "MIDDLE_AGED"
    SENIORS = "SENIORS"
    ANY = "ANY"


@public.add
class BrandAudienceGender(StrEnum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    ANY = "ANY"


@public.add
class BrandAudienceIncomeRange(StrEnum):
    LOW_INCOME = "LOW_INCOME"
    MIDDLE_INCOME = "MIDDLE_INCOME"
    UPPER_MIDDLE_INCOME = "UPPER_MIDDLE_INCOME"
    HIGH_INCOME = "HIGH_INCOME"
    ANY = "ANY"


@public.add
class BrandAudience(BaseModel):
    id: str = Field(default_factory=new_id)
    name: str = Field(default="")

    age_range: BrandAudienceAgeRange = Field(BrandAudienceAgeRange.ANY)
    gender: BrandAudienceGender = Field(BrandAudienceGender.ANY)
    income_range: BrandAudienceIncomeRange = Field(BrandAudienceIncomeRange.ANY)

    pain_points: list[str] = Field(default_factory=list)
    objections: list[str] = Field(default_factory=list)

    channels: list[ContentChannelName] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
