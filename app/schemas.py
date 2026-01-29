from pydantic import BaseModel
from typing import List, Optional, Dict


# =========================
# MESSAGE MODEL
# =========================
class Message(BaseModel):
    role: Optional[str] = "user"
    content: Optional[str] = ""


# =========================
# REQUEST MODEL (TESTER-FRIENDLY)
# =========================
class ScamRequest(BaseModel):
    conversation_id: Optional[str] = "unknown"
    message: Optional[str] = ""
    history: Optional[List[Message]] = []


# =========================
# EXTRACTED INTELLIGENCE
# =========================
class Intelligence(BaseModel):
    bank_accounts: List[str] = []
    upi_ids: List[str] = []
    phishing_links: List[str] = []


# =========================
# RESPONSE MODEL
# =========================
class ScamResponse(BaseModel):
    is_scam: bool
    agent_active: bool
    reply: str
    metrics: Dict
    extracted_intelligence: Intelligence
