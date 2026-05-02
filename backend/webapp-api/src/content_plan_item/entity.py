from sqlalchemy import Column, Enum, ForeignKey, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, TIMESTAMP

from lib.db import Base
from webapp_api_contract.shared import ContentChannelName, ContentFormat, JobStatus


class ContentPlanItemRecord(Base):
    __tablename__ = "content_plan_items"

    id = Column(Text, primary_key=True)
    job_id = Column(
        Text, ForeignKey("campaign_generation_jobs.id", ondelete="CASCADE"), index=True
    )
    description = Column(Text, nullable=False)
    channel = Column(Enum(ContentChannelName), nullable=False)
    content_type = Column(Text, nullable=False)
    content_format = Column(Enum(ContentFormat), nullable=False)
    image_urls = Column(ARRAY(Text), nullable=True)
    status = Column(Enum(JobStatus), nullable=False, default=JobStatus.PENDING)
    scheduled_at = Column(TIMESTAMP(timezone=True), nullable=True)
    content_data = Column(JSONB, nullable=True)
