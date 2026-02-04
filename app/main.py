from fastapi import FastAPI, Header, HTTPException, Request
from typing import Optional
import random

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    body = await request.body()
    print("===== INCOMING REQUEST =====")
    print("METHOD:", request.method)
    print("PATH:", request.url.path)
    print("HEADERS:", dict(request.headers))
    print("BODY:", body)
    print("============================")
    response = await call_next(request)
    return response

API_KEY = "N!m!$#@3reddy"

def verify_api_key(key: Optional[str]):
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

SCAM_REPLIES = [
    "Why is my account being suspended?",
    "This is the first time I’m hearing about this. What happened?",
    "I’m really worried. What do I need to do?",
    "Can you explain why my account will be blocked?",
    "Is this urgent? I didn’t receive any notification earlier."
]

NORMAL_REPLIES = [
    "Hello, how can I help you?",
    "Can you please explain what this is about?",
    "I’m not sure I understand. Could you clarify?",
]

def looks_like_scam(text: str) -> bool:
    triggers = ["blocked", "verify", "urgent", "otp", "account", "kyc", "suspended"]
    return any(t in text.lower() for t in triggers)

@app.api_route("/", methods=["GET", "POST", "HEAD", "OPTIONS"])
@app.api_route("/message", methods=["GET", "POST", "HEAD", "OPTIONS"])
async def universal_handler(
    request: Request,
    x_api_key: Optional[str] = Header(None),
):
    verify_api_key(x_api_key)

    text = ""

    # Try to read message text safely
    if request.method == "POST":
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

    # 🔒 Fixed response schema (tester-safe)
    return {
        "status": "success",
        "reply": reply
    }
