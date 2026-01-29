from fastapi import FastAPI, Header, HTTPException, Request
from typing import Optional

from app.schemas import ScamResponse, Intelligence
from app.detector import is_scam_message
from app.agent import generate_agent_reply
from app.extractor import extract_intelligence

API_KEY = "N!m!$#@3reddy"

app = FastAPI()


# =========================
# ROOT — NO AUTH, EVER
# =========================
@app.api_route("/", methods=["GET", "POST", "HEAD"])
def root():
    # Debug marker to confirm new code is live
    return {"status": "honeypot running", "root_auth": "disabled"}


# =========================
# AUTH CHECK
# =========================
def check_api_key(x_api_key: Optional[str]):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")


# =========================
# HEALTH (AUTH REQUIRED)
# =========================
@app.get("/health")
def health(x_api_key: Optional[str] = Header(None)):
    check_api_key(x_api_key)
    return {"status": "ok"}


# =========================
# MESSAGE (AUTH REQUIRED)
# =========================
@app.api_route("/message", methods=["GET", "POST", "HEAD"])
async def message_endpoint(
    request: Request,
    x_api_key: Optional[str] = Header(None)
):
    check_api_key(x_api_key)

    try:
        body = await request.json()
        if not isinstance(body, dict):
            body = {}
    except Exception:
        body = {}

    message = body.get("message", "")
    history = body.get("history", [])

    if not isinstance(message, str):
        message = ""
    if not isinstance(history, list):
        history = []

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
            bank_accounts=intel["bank_accounts"],
            upi_ids=intel["upi_ids"],
            phishing_links=intel["phishing_links"],
        )
    )
