from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Optional

from app.detector import is_scam_message
from app.agent import generate_agent_reply
from app.extractor import extract_intelligence

API_KEY = "N!m!$#@3reddy"

app = FastAPI()


# ======================================================
# ROOT ENDPOINT — NO AUTH (CONNECTIVITY CHECK)
# ======================================================
@app.api_route("/", methods=["GET", "POST", "HEAD"])
def root():
    return JSONResponse(
        status_code=200,
        content={"status": "honeypot running"}
    )


# ======================================================
# API KEY CHECK
# ======================================================
def check_api_key(x_api_key: Optional[str]):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )


# ======================================================
# MAIN HONEYPOT ENDPOINT
# ======================================================
@app.api_route("/message", methods=["GET", "POST", "HEAD"])
async def message_endpoint(
    request: Request,
    x_api_key: Optional[str] = Header(None)
):
    # 🔐 Enforce API key
    check_api_key(x_api_key)

    # --------------------------------------------------
    # SAFE BODY PARSING (NO VALIDATION FAILURES)
    # --------------------------------------------------
    try:
        body = await request.json()
        if not isinstance(body, dict):
            body = {}
    except Exception:
        body = {}

    # --------------------------------------------------
    # HISTORY EXTRACTION
    # --------------------------------------------------
    history = body.get("history", [])
    if not isinstance(history, list):
        history = []

    # --------------------------------------------------
    # MESSAGE EXTRACTION (HISTORY-FIRST)
    # --------------------------------------------------
    message = body.get("message")

    last_scammer_msg = ""
    for item in reversed(history):
        if isinstance(item, dict) and item.get("role") == "scammer":
            last_scammer_msg = item.get("content", "")
            break

    if not isinstance(message, str) or not message.strip():
        message = last_scammer_msg

    if not isinstance(message, str):
        message = ""

    # --------------------------------------------------
    # FINAL SCAM DECISION
    # --------------------------------------------------
    # If scammer has ever spoken → THIS IS A SCAM
    is_scam = bool(last_scammer_msg) or is_scam_message(message)

    # --------------------------------------------------
    # AGENT RESPONSE
    # --------------------------------------------------
    if is_scam:
        reply = generate_agent_reply(message, history)
    else:
        reply = "Hello, how can I help you?"

    # --------------------------------------------------
    # INTELLIGENCE EXTRACTION
    # --------------------------------------------------
    intel = extract_intelligence(message)

    # --------------------------------------------------
    # FORCE JSON RESPONSE (TESTER-SAFE)
    # --------------------------------------------------
    return JSONResponse(
        status_code=200,
        content={
            "is_scam": is_scam,
            "agent_active": is_scam,
            "reply": reply,
            "metrics": {
                "turns": len(history) + 1
            },
            "extracted_intelligence": {
                "bank_accounts": intel.get("bank_accounts", []),
                "upi_ids": intel.get("upi_ids", []),
                "phishing_links": intel.get("phishing_links", []),
            }
        }
    )
