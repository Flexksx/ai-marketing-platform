import public
from faker import Faker
from pydantic_extra_types.language_code import LanguageAlpha2

from src.brand.archetype.model import BrandArchetypeName
from src.brand.model import (
    BrandAudience,
    BrandAudienceAgeRange,
    BrandAudienceGender,
    BrandAudienceIncomeRange,
    BrandColor,
    BrandData,
    BrandToneOfVoice,
)


fake = Faker()


@public.add
class BrandMockFactory:
    @staticmethod
    def create_tone_of_voice() -> BrandToneOfVoice:
        return BrandToneOfVoice(
            archetype=fake.random_element(elements=list(BrandArchetypeName)),
            jargon_density=fake.random_int(min=1, max=4),
            visual_density=fake.random_int(min=1, max=4),
            must_use_words=[fake.word() for _ in range(2)],
            forbidden_words=[fake.word() for _ in range(2)],
        )

    @classmethod
    def create_brand_data(cls) -> BrandData:
        return BrandData(
            logo_url=fake.image_url(),
            media_urls=[fake.image_url() for _ in range(2)],
            colors=[
                BrandColor(name="Primary", hex_value=fake.hex_color()),
                BrandColor(name="Secondary", hex_value=fake.hex_color()),
            ],
            brand_mission=fake.sentence(nb_words=10),
            locale=LanguageAlpha2("en"),
            audiences=[
                cls.create_brand_audience(),
                cls.create_brand_audience(),
            ],
            tone_of_voice=BrandMockFactory.create_tone_of_voice(),
        )

    @classmethod
    def create_brand_audience(cls) -> BrandAudience:
        return BrandAudience(
            name=fake.word(),
            age_range=fake.random_element(elements=list(BrandAudienceAgeRange)),
            gender=fake.random_element(elements=list(BrandAudienceGender)),
            income_range=fake.random_element(elements=list(BrandAudienceIncomeRange)),
            pain_points=[fake.word() for _ in range(3)],
            objections=[fake.word() for _ in range(2)],
        )
