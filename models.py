from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    user_id: Optional[str] = "guest_default"
    session_id: Optional[str] = None
    conversation_id: Optional[str] = None
    query: str

class CreateConversationRequest(BaseModel):
    user_id: str
    title: Optional[str] = "New Conversation"