from fastapi import FastAPI, Header, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from app.detector import is_scam_message
from app.agent import generate_agent_reply
from app.extractor import extract_intelligence

API_KEY = "N!m!$#@3reddy"

app = FastAPI(title="Agentic Honeypot API")

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# MEMORY
# =========================
CONVERSATIONS = {}

# =========================
# AUTH
# =========================
def verify_api_key(key: Optional[str]):
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

# =========================
# ROOT ENDPOINT (OFFICIAL TESTER)
# =========================
@app.post("/")
async def tester_entrypoint(
    request: Request,
    x_api_key: Optional[str] = Header(None),
):
    verify_api_key(x_api_key)

    try:
        body = await request.json()
        if not isinstance(body, dict):
            body = {}
    except Exception:
        body = {}

    # Extract tester message safely
    text = ""
    try:
        msg_obj = body.get("message", {})
        if isinstance(msg_obj, dict):
            text = msg_obj.get("text", "")
        if not isinstance(text, str):
            text = ""
    except Exception:
        text = ""

    is_scam = is_scam_message(text)

    reply = (
        generate_agent_reply(text, [])
        if is_scam
        else "Hello, how can I help you?"
    )

    # ✅ EXACT FORMAT REQUIRED BY ORGANIZER
    return {
        "status": "success",
        "reply": reply
    }

# =========================
# FULL HONEYPOT ENDPOINT
# =========================
@app.api_route("/message", methods=["POST", "OPTIONS"])
async def message_endpoint(
    request: Request,
    x_api_key: Optional[str] = Header(None),
):
    if request.method == "OPTIONS":
        return Response(status_code=200)

    verify_api_key(x_api_key)

    try:
        body = await request.json()
        if not isinstance(body, dict):
            body = {}
    except Exception:
        body = {}

    conversation_id = body.get("conversation_id", "default")
    history = body.get("history", [])
    message = body.get("message")

    # Infer message from history if needed
    if not isinstance(message, str) and isinstance(history, list):
        for h in reversed(history):
            if isinstance(h, dict) and h.get("role") == "scammer":
                message = h.get("content", "")
                break

    if not isinstance(message, str):
        message = ""

    if conversation_id not in CONVERSATIONS:
        CONVERSATIONS[conversation_id] = []

    if message:
        CONVERSATIONS[conversation_id].append({
            "role": "scammer",
            "content": message
        })

    is_scam = is_scam_message(message)

    reply = (
        generate_agent_reply(message, CONVERSATIONS[conversation_id])
        if is_scam
        else "Hello, how can I help you?"
    )

    CONVERSATIONS[conversation_id].append({
        "role": "honeypot",
        "content": reply
    })

    intel = extract_intelligence(message)

    return {
        "is_scam": is_scam,
        "agent_active": is_scam,
        "reply": reply,
        "metrics": {
            "turns": len(CONVERSATIONS[conversation_id])
        },
        "memory": CONVERSATIONS[conversation_id],
        "extracted_intelligence": intel
    }
