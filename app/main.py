from fastapi import FastAPI, Header, HTTPException, Request
from typing import Optional

from app.detector import is_scam_message
from app.agent import generate_agent_reply

API_KEY = "N!m!$#@3redd"

app = FastAPI()

def verify_api_key(key: Optional[str]):
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

@app.post("/")
async def honeypot_entrypoint(
    request: Request,
    x_api_key: Optional[str] = Header(None),
):
    verify_api_key(x_api_key)

    # NEVER FAIL ON BODY
    try:
        body = await request.json()
        if not isinstance(body, dict):
            body = {}
    except Exception:
        body = {}

    text = ""

    # Handle tester payload
    msg = body.get("message")
    if isinstance(msg, dict):
        text = msg.get("text", "")

    if not isinstance(text, str):
        text = ""

    # Honeypot reasoning (internal only)
    if is_scam_message(text):
        reply = generate_agent_reply(text, [])
    else:
        reply = "Hello, how can I help you?"

    # 🔒 ALWAYS SAME RESPONSE SHAPE
    return {
        "status": "success",
        "reply": reply
    }
