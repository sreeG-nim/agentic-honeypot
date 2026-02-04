from fastapi import FastAPI, Header, HTTPException, Request
from typing import Optional
import random

app = FastAPI()

API_KEY = "N!m!$#@3reddy"

SCAM_REPLIES = [
    "Why is my account being suspended?",
    "This sounds serious. What happened?",
    "I didn’t receive any notice earlier. Can you explain?",
    "Is my account already blocked?",
]

NORMAL_REPLIES = [
    "Hello, how can I help you?",
    "Can you please clarify?",
]

def looks_like_scam(text: str) -> bool:
    triggers = ["blocked", "verify", "urgent", "otp", "account", "kyc", "suspended"]
    return any(t in text.lower() for t in triggers)

# -----------------------------
# OPEN PROBE (NO AUTH)
# -----------------------------
@app.api_route("/", methods=["GET", "HEAD", "OPTIONS"])
async def open_probe():
    return {
        "status": "success",
        "reply": "Honeypot active"
    }

# -----------------------------
# REAL HANDLER (AUTH REQUIRED)
# -----------------------------
@app.post("/")
async def main_handler(
    request: Request,
    x_api_key: Optional[str] = Header(None),
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

    text = ""

    try:
        body = await request.json()
        if isinstance(body, dict):
            msg = body.get("message")
            if isinstance(msg, dict):
                t = msg.get("text")
                if isinstance(t, str):
                    text = t
    except Exception:
        pass

    if text and looks_like_scam(text):
        reply = random.choice(SCAM_REPLIES)
    else:
        reply = random.choice(NORMAL_REPLIES)

    return {
        "status": "success",
        "reply": reply
    }
