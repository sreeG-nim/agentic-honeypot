from fastapi import FastAPI, Header, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from app.detector import is_scam_message
from app.agent import generate_agent_reply
from app.extractor import extract_intelligence

API_KEY = "N!m!$#@3reddy"

app = FastAPI(title="Agentic Honeypot API")

# 🔥 EXPLICIT CORS (INCLUDING PREFLIGHT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],      # includes OPTIONS
    allow_headers=["*"],      # includes x-api-key
)

@app.api_route("/", methods=["GET", "HEAD", "OPTIONS"])
def root():
    return {"status": "honeypot running"}

def verify_api_key(x_api_key: Optional[str]):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

@app.api_route("/message", methods=["POST", "GET", "HEAD", "OPTIONS"])
async def message_endpoint(
    request: Request,
    x_api_key: Optional[str] = Header(None),
):
    # OPTIONS preflight must return 200
    if request.method == "OPTIONS":
        return Response(status_code=200)

    verify_api_key(x_api_key)

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
    if not message:
        for h in reversed(history):
            if isinstance(h, dict) and h.get("role") == "scammer":
                message = h.get("content", "")
                break

    is_scam = bool(message) and is_scam_message(message)

    reply = (
        generate_agent_reply(message, history)
        if is_scam
        else "Hello, how can I help you?"
    )

    intel = extract_intelligence(message)

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
