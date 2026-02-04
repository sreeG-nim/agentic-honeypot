from fastapi import FastAPI, Header, HTTPException, Request
from typing import Optional

API_KEY = "N!m!$#@3reddy"

app = FastAPI()

def verify_api_key(key: Optional[str]):
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

def build_reply(text: str) -> str:
    triggers = ["blocked", "verify", "urgent", "otp", "account", "kyc"]
    if any(t in text.lower() for t in triggers):
        return "Why is my account being suspended?"
    return "Hello, how can I help you?"

# 🔒 HANDLE EVERYTHING ON BOTH PATHS
@app.api_route("/", methods=["GET", "POST", "HEAD", "OPTIONS"])
@app.api_route("/message", methods=["GET", "POST", "HEAD", "OPTIONS"])
async def universal_handler(
    request: Request,
    x_api_key: Optional[str] = Header(None),
):
    verify_api_key(x_api_key)

    text = ""

    # Try reading body ONLY if present
    try:
        body = await request.json()
        if isinstance(body, dict):
            msg = body.get("message")
            if isinstance(msg, dict):
                t = msg.get("text")
                if isinstance(t, str):
                    text = t
    except Exception:
        pass  # never fail

    return {
        "status": "success",
        "reply": build_reply(text)
    }
