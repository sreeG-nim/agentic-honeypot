from pydantic import BaseModel
from typing import List, Dict

class ScamResponse(BaseModel):
    is_scam: bool
    agent_active: bool
    reply: str
    metrics: Dict
    extracted_intelligence: Dict
