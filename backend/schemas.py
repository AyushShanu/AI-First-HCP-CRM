from pydantic import BaseModel
from typing import Optional

class InteractionBase(BaseModel):
    hcp_name: str
    interaction_type: str = "Meeting"
    date: Optional[str] = None
    time: Optional[str] = None
    attendees: str = ""
    topics_discussed: str = ""
    materials_shared: str = ""
    samples_distributed: str = ""
    sentiment: str = "Neutral"
    outcomes: str = ""
    follow_up_actions: str = ""

class InteractionCreate(InteractionBase):
    pass

class InteractionOut(InteractionBase):
    id: int
    ai_summary: str = ""
    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"
