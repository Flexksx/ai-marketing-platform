from sqlalchemy import Column, ForeignKey, String, func
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import DateTime

from db import Base
from webapp_api_contract.shared import ContentFormat
from webapp_api_contract.shared import JobStatus


class ContentGenerationJobRecord(Base):
    __tablename__ = "content_generation_jobs"

    id = Column(String, primary_key=True)
    brand_id = Column(String, ForeignKey("brands.id", ondelete="CASCADE"))
    user_input = Column(JSONB, nullable=False)
    content_format = Column(SQLAlchemyEnum(ContentFormat), nullable=False)
    status = Column(
        SQLAlchemyEnum(JobStatus), nullable=False, default=JobStatus.PENDING
    )
    result = Column(JSONB)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
