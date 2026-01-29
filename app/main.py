from fastapi import FastAPI, Header, HTTPException, Request
from typing import Optional

from .schemas import ScamResponse, Intelligence
from .detector import is_scam_message
from .agent import generate_agent_reply
from .extractor import extract_intelligence


API_KEY = "N!m!$#@3reddy"

app = FastAPI()


# =========================
# AUTH CHECK (MANUAL)
# =========================
def check_api_key(x_api_key: Optional[str]):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")


# =========================
# ROOT (TESTER CONNECTIVITY)
# =========================
@app.api_route("/", methods=["GET", "POST", "HEAD"])
def root(x_api_key: Optional[str] = Header(None)):
    check_api_key(x_api_key)
    return {"status": "honeypot running"}


# =========================
# MAIN ENDPOINT
# =========================
@app.api_route("/message", methods=["GET", "POST", "HEAD"])
async def message_endpoint(
    request: Request,
    x_api_key: Optional[str] = Header(None)
):
    check_api_key(x_api_key)

    # Safely read body
    try:
        body = await request.json()
        if not isinstance(body, dict):
            body = {}
    except Exception:
        body = {}

    message = body.get("message", "")
    history = body.get("history", [])

    # Defensive type handling
    if not isinstance(message, str):
        message = ""

    is_scam = is_scam_message(message)

    if is_scam:
        reply = generate_agent_reply(message, history)
    else:
        reply = "Hello, how can I help you?"

    intel = extract_intelligence(message)

    return ScamResponse(
        is_scam=is_scam,
        agent_active=is_scam,
        reply=reply,
        metrics={"turns": 1},
        extracted_intelligence=Intelligence(
            bank_accounts=intel.get("bank_accounts", []),
            upi_ids=intel.get("upi_ids", []),
            phishing_links=intel.get("phishing_links", []),
        )
    )
