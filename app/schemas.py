from pydantic import BaseModel
from typing import List, Optional

class Message(BaseModel):
    role: str
    content: str

class ScamRequest(BaseModel):
    conversation_id: str
    message: str
    history: Optional[List[Message]] = []

class Intelligence(BaseModel):
    bank_accounts: List[str] = []
    upi_ids: List[str] = []
    phishing_links: List[str] = []

class ScamResponse(BaseModel):
    is_scam: bool
    agent_active: bool
    reply: str
    metrics: dict
    extracted_intelligence: Intelligence
