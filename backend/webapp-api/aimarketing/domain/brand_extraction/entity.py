import public
from sqlalchemy import Column, String, func
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import ARRAY, DateTime

from db import Base
from aimarketing.lib.job.model import JobStatus


@public.add
class BrandGenerationJobRecord(Base):
    __tablename__ = "brand_generation_jobs"

    id = Column(String, primary_key=True)
    status = Column(
        SQLAlchemyEnum(JobStatus), nullable=False, default=JobStatus.PENDING
    )
    website_url = Column(String, nullable=False)
    extra_routes = Column(ARRAY(String), nullable=False, default=["/about", "/help"])
    result = Column(JSONB, nullable=True)
    user_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
