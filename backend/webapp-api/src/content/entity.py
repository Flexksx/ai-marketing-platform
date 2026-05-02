import public
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey, Index
from sqlalchemy.sql.functions import func
from sqlalchemy.types import DateTime, String
from sqlalchemy.types import Enum as SQLAlchemyEnum

from lib.db.database import Base
from webapp_api_contract.shared import ContentFormat
from webapp_api_contract.shared import ContentChannelName


@public.add
class ContentRecord(Base):
    __tablename__ = "contents"
    __table_args__ = (Index("idx_content_channel", "channel"),)

    id = Column(Text, primary_key=True)
    brand_id = Column(String, ForeignKey("brands.id", ondelete="CASCADE"))
    campaign_id = Column(
        String, ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=True
    )

    channel = Column(
        SQLAlchemyEnum(ContentChannelName, name="content_channel_name"),
    )
    content_format = Column(SQLAlchemyEnum(ContentFormat))

    data = Column(JSONB)

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    scheduled_at = Column(DateTime(timezone=True))

    campaign = relationship("CampaignRecord", back_populates="contents")
