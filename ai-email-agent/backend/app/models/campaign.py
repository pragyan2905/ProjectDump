from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class Campaign(Base):
    """
    Represents a bulk email campaign.
    """
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    prompt_template = Column(Text)
    status = Column(String, default="pending") # States: pending, processing, completed
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class EmailRecord(Base):
    """
    Represents an individual email being generated and sent to a specific recipient.
    """
    __tablename__ = "email_records"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    recipient_email = Column(String, index=True)
    recipient_name = Column(String)
    generated_content = Column(Text, nullable=True)
    status = Column(String, default="pending") # States: pending, generated, sent, failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
