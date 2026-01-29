from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Optional

from app.detector import is_scam_message
from app.agent import generate_agent_reply
from app.extractor import extract_intelligence

API_KEY = "N!m!$#@3reddy"

app = FastAPI()


@app.api_route("/", methods=["GET", "POST", "HEAD"])
def root():
    return JSONResponse(status_code=200, content={"status": "honeypot running"})


def check_api_key(x_api_key: Optional[str]):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")


@app.api_route("/message", methods=["GET", "POST", "HEAD"])
async def message_endpoint(request: Request, x_api_key: Optional[str] = Header(None)):
    check_api_key(x_api_key)

    try:
        body = await request.json()
        if not isinstance(body, dict):
            body = {}
    except Exception:
        body = {}

    history = body.get("history", [])
    if not isinstance(history, list):
        history = []

    message = body.get("message", "")

    last_scammer_msg = ""
    for h in reversed(history):
        if isinstance(h, dict) and h.get("role") == "scammer":
            last_scammer_msg = h.get("content", "")
            break

    if not message:
        message = last_scammer_msg

    is_scam = bool(last_scammer_msg) or is_scam_message(message)

    if is_scam:
        try:
            reply = generate_agent_reply(message, history)
        except Exception:
            reply = "Sorry… my phone is acting weird. Can you explain again?"
    else:
        reply = "Hello, how can I help you?"

    try:
        intel = extract_intelligence(message)
    except Exception:
        intel = {"bank_accounts": [], "upi_ids": [], "phishing_links": []}

    return JSONResponse(
        status_code=200,
        content={
            "is_scam": is_scam,
            "agent_active": is_scam,
            "reply": reply,
            "metrics": {"turns": len(history) + 1},
            "extracted_intelligence": intel,
        },
    )
