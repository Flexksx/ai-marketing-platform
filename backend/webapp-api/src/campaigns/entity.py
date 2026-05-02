from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Index,
    String,
    func,
)
from sqlalchemy import (
    Enum as SQLAlchemyEnum,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from lib.db.database import Base
from webapp_api_contract.campaigns import CampaignState


class CampaignRecord(Base):
    __tablename__ = "campaigns"
    __table_args__ = (
        Index("campaigns_brand_id_idx", "brand_id"),
        Index("campaigns_state_idx", "state"),
    )

    id = Column(String, primary_key=True)
    brand_id = Column(String, ForeignKey("brands.id", ondelete="CASCADE"))
    state = Column(SQLAlchemyEnum(CampaignState))
    data = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    brand = relationship("BrandRecord", back_populates="campaigns")
    contents = relationship("ContentRecord", back_populates="campaign")
