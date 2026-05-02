from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from webapp_api_contract.brand import BrandData


class Brand(BaseModel):
    id: str
    user_id: str
    name: str
    data: BrandData = Field(default_factory=BrandData)
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
