from fastapi import FastAPI, Header, HTTPException, Depends
from typing import Optional

from .schemas import ScamRequest, ScamResponse, Intelligence
from .detector import is_scam_message
from .agent import generate_agent_reply
from .extractor import extract_intelligence


# =========================
# API KEY CONFIG
# =========================
API_KEY = "N!m!$#@3reddy"


def verify_api_key(x_api_key: Optional[str] = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )


# =========================
# FASTAPI APP
# =========================
app = FastAPI()


# =========================
# HEALTH CHECK
# =========================
@app.get("/health")
def health(_: None = Depends(verify_api_key)):
    return {"status": "ok"}


# =========================
# MAIN HONEYPOT ENDPOINT
# =========================
@app.post("/message", response_model=ScamResponse)
def handle_message(
    req: ScamRequest,
    _: None = Depends(verify_api_key)
):
    # Detect scam intent
    is_scam = is_scam_message(req.message)

    # Agent handoff
    if is_scam:
        reply = generate_agent_reply(req.message, req.history)
    else:
        reply = "Hello, how can I help you?"

    # Extract scam intelligence
    intel = extract_intelligence(req.message)

    return ScamResponse(
        is_scam=is_scam,
        agent_active=is_scam,
        reply=reply,
        metrics={"turns": len(req.history) + 1},
        extracted_intelligence=Intelligence(
            bank_accounts=intel["bank_accounts"],
            upi_ids=intel["upi_ids"],
            phishing_links=intel["phishing_links"],
        )
    )
