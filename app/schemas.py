from pydantic import BaseModel
from typing import List, Dict


class Intelligence(BaseModel):
    bank_accounts: List[str] = []
    upi_ids: List[str] = []
    phishing_links: List[str] = []


class ScamResponse(BaseModel):
    is_scam: bool
    agent_active: bool
    reply: str
    metrics: Dict
    extracted_intelligence: Intelligence
