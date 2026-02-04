from fastapi import FastAPI, Header, HTTPException, Request
from typing import Optional

API_KEY = "N!m!$#@3reddy"

app = FastAPI()

def verify_api_key(key: Optional[str]):
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

# 🔒 HANDLE *ALL* METHODS ON ROOT
@app.api_route("/", methods=["GET", "POST", "HEAD", "OPTIONS"])
async def root_handler(
    request: Request,
    x_api_key: Optional[str] = Header(None),
):
    verify_api_key(x_api_key)

    text = ""

    # Try to extract text ONLY IF BODY EXISTS
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
            pass  # absolutely never fail

    # Very simple bait logic
    if text and any(k in text.lower() for k in ["blocked", "verify", "urgent", "otp", "account"]):
        reply = "Why is my account being suspended?"
    else:
        reply = "Hello, how can I help you?"

    # 🔑 ALWAYS SAME RESPONSE SHAPE
    return {
        "status": "success",
        "reply": reply
    }
