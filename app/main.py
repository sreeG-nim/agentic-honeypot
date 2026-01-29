from fastapi import FastAPI, Header, HTTPException, Depends, Request
from typing import Optional

from .schemas import ScamResponse, Intelligence
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
# ROOT ENDPOINT (TESTER CONNECTIVITY CHECK)
# =========================
@app.get("/")
def root():
    return {"status": "honeypot running"}


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
async def handle_message(
    request: Request,
    _: None = Depends(verify_api_key)
):
    """
    Tester-safe endpoint:
    - Works with NO body
    - Works with empty body
    - Works with invalid JSON
    - Works with valid JSON
    """

    # Safely read request body (or default)
    try:
        body = await request.json()
        if not isinstance(body, dict):
            body = {}
    except Exception:
        body = {}

    message = body.get("message", "")
    history = body.get("history", [])

    # Detect scam intent
    is_scam = is_scam_message(message)

    # Agent handoff
    if is_scam:
        reply = generate_agent_reply(message, history)
    else:
        reply = "Hello, how can I help you?"

    # Extract intelligence
    intel = extract_intelligence(message)

    return ScamResponse(
        is_scam=is_scam,
        agent_active=is_scam,
        reply=reply,
        metrics={"turns": len(history) + 1},
        extracted_intelligence=Intelligence(
            bank_accounts=intel.get("bank_accounts", []),
            upi_ids=intel.get("upi_ids", []),
            phishing_links=intel.get("phishing_links", []),
        )
    )
