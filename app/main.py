from fastapi import FastAPI, Header, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from app.detector import is_scam_message
from app.agent import generate_agent_reply
from app.extractor import extract_intelligence

API_KEY = "N!m!$#@3reddy"

app = FastAPI(title="Agentic Honeypot API")

# ===== CORS =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== In-memory conversation store =====
CONVERSATIONS = {}

@app.api_route("/", methods=["GET", "HEAD"])
def root():
    return {"status": "honeypot running"}

def verify_api_key(key: Optional[str]):
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

def confidence_score(message: str) -> int:
    keywords = ["otp", "urgent", "blocked", "verify", "kyc", "transfer", "account"]
    score = 30 + sum(15 for k in keywords if k in message.lower())
    return min(score, 95)

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
    except Exception:
        body = {}

    conv_id = body.get("conversation_id", "default")
    message = body.get("message", "")
    history = body.get("history", [])

    if conv_id not in CONVERSATIONS:
        CONVERSATIONS[conv_id] = []

    CONVERSATIONS[conv_id].append({
        "role": "scammer",
        "content": message
    })

    is_scam = is_scam_message(message)

    reply = (
        generate_agent_reply(message, CONVERSATIONS[conv_id])
        if is_scam
        else "Hello, how can I help you?"
    )

    CONVERSATIONS[conv_id].append({
        "role": "honeypot",
        "content": reply
    })

    intel = extract_intelligence(message)

    return JSONResponse(
        content={
            "is_scam": is_scam,
            "agent_active": is_scam,
            "reply": reply,
            "confidence_score": confidence_score(message),
            "metrics": {"turns": len(CONVERSATIONS[conv_id])},
            "memory": CONVERSATIONS[conv_id],
            "extracted_intelligence": intel,
        }
    )
