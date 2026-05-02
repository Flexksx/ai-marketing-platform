from sqlalchemy import Column, ForeignKey, Integer, String, func
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import DateTime

from db import Base
from webapp_api_contract.campaign_generation import (
    CampaignGenerationJobWorkflowType,
)
from webapp_api_contract.shared import JobStatus


class CampaignGenerationJobRecord(Base):
    __tablename__ = "campaign_generation_jobs"

    id = Column(String, primary_key=True)
    brand_id = Column(String, ForeignKey("brands.id", ondelete="CASCADE"))
    workflow_type = Column(
        SQLAlchemyEnum(CampaignGenerationJobWorkflowType), nullable=False
    )
    user_input = Column(JSONB, nullable=False)
    status = Column(
        SQLAlchemyEnum(JobStatus), nullable=False, default=JobStatus.PENDING
    )
    result = Column(JSONB)
    version = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
