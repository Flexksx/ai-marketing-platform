from datetime import datetime

from pydantic import BaseModel, ConfigDict

from webapp_api_contract.campaigns import CampaignData, CampaignState


class Campaign(BaseModel):
    id: str
    brand_id: str
    state: CampaignState
    data: CampaignData | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
