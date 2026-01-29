SCAM_KEYWORDS = [
    "account",
    "blocked",
    "verify",
    "click",
    "otp",
    "kyc",
    "upi",
    "bank",
    "refund",
    "urgent"
]

def is_scam_message(message: str) -> bool:
    msg = message.lower()
    return any(word in msg for word in SCAM_KEYWORDS)
