from fastapi import FastAPI, Header, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from app.detector import is_scam_message
from app.agent import generate_agent_reply
from app.extractor import extract_intelligence

# =========================
# CONFIG
# =========================
API_KEY = "N!m!$#@3reddy"

app = FastAPI(title="Agentic Honeypot API")

# =========================
# CORS (browser + tester safe)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# In-memory conversation store
# =========================
CONVERSATIONS = {}

# =========================
# AUTH
# =========================
def verify_api_key(key: Optional[str]):
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

# =========================
# ROOT — REQUIRED FOR TESTER
# =========================
@app.api_route("/", methods=["GET", "HEAD"])
def root():
    return {"status": "honeypot running"}

# Tester sends POST with EMPTY BODY to root
@app.api_route("/", methods=["POST"])
async def tester_root(
    request: Request,
    x_api_key: Optional[str] = Header(None),
):
    verify_api_key(x_api_key)

    return {
        "is_scam": False,
        "agent_active": False,
        "reply": "Honeypot active and listening.",
        "confidence_score": 0,
        "metrics": {"turns": 0},
        "memory": [],
        "extracted_intelligence": {
            "bank_accounts": [],
            "upi_ids": [],
            "phishing_links": []
        }
    }

# =========================
# CONFIDENCE SCORE
# =========================
def confidence_score(message: str) -> int:
    keywords = ["otp", "urgent", "blocked", "verify", "kyc", "transfer", "account", "upi"]
    hits = sum(1 for k in keywords if k in message.lower())
    return min(95, 30 + hits * 15)

# =========================
# MAIN HONEYPOT ENDPOINT
# =========================
@app.api_route("/message", methods=["POST", "OPTIONS"])
async def message_endpoint(
    request: Request,
    x_api_key: Optional[str] = Header(None),
):
    if request.method == "OPTIONS":
        return Response(status_code=200)

    verify_api_key(x_api_key)

    # Parse body safely
    try:
        body = await request.json()
        if not isinstance(body, dict):
            body = {}
    except Exception:
        body = {}

    conversation_id = body.get("conversation_id", "default")
    history = body.get("history", [])
    message = body.get("message")

    # 🔥 CRITICAL FIX: infer message from history
    if not message and isinstance(history, list):
        for h in reversed(history):
            if (
                isinstance(h, dict)
                and h.get("role") == "scammer"
                and h.get("content")
            ):
                message = h["content"]
                break

    if not message:
        message = ""

    # Init memory
    if conversation_id not in CONVERSATIONS:
        CONVERSATIONS[conversation_id] = []

    # Append scammer message ONLY if valid
    if message:
        CONVERSATIONS[conversation_id].append({
            "role": "scammer",
            "content": message
        })

    # Scam detection
    is_scam = bool(message) and is_scam_message(message)

    # Agent reply
    reply = (
        generate_agent_reply(message, CONVERSATIONS[conversation_id])
        if is_scam
        else "Hello, how can I help you?"
    )

    # Append honeypot reply
    CONVERSATIONS[conversation_id].append({
        "role": "honeypot",
        "content": reply
    })

    # Extract intelligence
    intel = extract_intelligence(message)

    return JSONResponse(
        status_code=200,
        content={
            "is_scam": is_scam,
            "agent_active": is_scam,
            "reply": reply,
            "confidence_score": confidence_score(message),
            "metrics": {
                "turns": len(CONVERSATIONS[conversation_id])
            },
            "memory": CONVERSATIONS[conversation_id],
            "extracted_intelligence": intel,
        }
    )
