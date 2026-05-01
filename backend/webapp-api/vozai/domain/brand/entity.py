import public
from sqlalchemy import Column, DateTime, Index, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from db.database import Base


@public.add
class BrandRecord(Base):
    __tablename__ = "brands"
    __table_args__ = (Index("brands_supabaseUserId_idx", "user_id"),)

    id = Column(String, primary_key=True)
    user_id = Column(Text, nullable=False, default="")
    name = Column(Text, nullable=False)
    data = Column(JSONB, nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    campaigns = relationship(
        "CampaignRecord",
        back_populates="brand",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
