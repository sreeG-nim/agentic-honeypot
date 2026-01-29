from fastapi import FastAPI, Header, HTTPException, Request
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

# =========================
# APP INIT
# =========================
app = FastAPI(title="Agentic Honeypot API")

# =========================
# CORS (REQUIRED FOR BROWSER FRONTEND)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # frontend can be anywhere
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# ROOT (KEEP SIMPLE FOR RENDER)
# =========================
@app.api_route("/", methods=["GET", "HEAD"])
def root():
    return {"status": "honeypot running"}

# =========================
# API KEY CHECK
# =========================
def verify_api_key(x_api_key: Optional[str]):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )

# =========================
# MAIN HONEYPOT ENDPOINT
# =========================
@app.api_route("/message", methods=["POST", "GET", "HEAD"])
async def message_endpoint(
    request: Request,
    x_api_key: Optional[str] = Header(None),
):
    # Auth
    verify_api_key(x_api_key)

    # Safely parse body (tester may send empty body)
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

    # If message missing, infer from last scammer message
    if not message:
        for h in reversed(history):
            if isinstance(h, dict) and h.get("role") == "scammer":
                message = h.get("content", "")
                break

    # Scam detection
    is_scam = bool(message) and is_scam_message(message)

    # Agent reply
    if is_scam:
        reply = generate_agent_reply(message, history)
    else:
        reply = "Hello, how can I help you?"

    # Intelligence extraction
    intel = extract_intelligence(message)

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
                "phishing_links": intel.get("phishing_links", [])
            }
        }
    )
