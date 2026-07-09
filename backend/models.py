from sqlalchemy import Column, Integer, String, Text, Date, Time, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class HCP(Base):
    __tablename__ = "hcps"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False, index=True)
    specialty = Column(String(120))
    hospital = Column(String(200))
    interactions = relationship("Interaction", back_populates="hcp")

class Interaction(Base):
    __tablename__ = "interactions"
    id = Column(Integer, primary_key=True, index=True)
    hcp_id = Column(Integer, ForeignKey("hcps.id"), nullable=True)
    hcp_name = Column(String(120), nullable=False)
    interaction_type = Column(String(50), default="Meeting")
    date = Column(String(20))
    time = Column(String(20))
    attendees = Column(Text, default="")
    topics_discussed = Column(Text, default="")
    materials_shared = Column(Text, default="")
    samples_distributed = Column(Text, default="")
    sentiment = Column(String(20), default="Neutral")
    outcomes = Column(Text, default="")
    follow_up_actions = Column(Text, default="")
    ai_summary = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    hcp = relationship("HCP", back_populates="interactions")

class FollowUp(Base):
    __tablename__ = "follow_ups"
    id = Column(Integer, primary_key=True, index=True)
    interaction_id = Column(Integer, ForeignKey("interactions.id"), nullable=True)
    hcp_name = Column(String(120))
    task = Column(Text)
    due_date = Column(String(20))
    status = Column(String(20), default="Pending")
    created_at = Column(DateTime, default=datetime.utcnow)
