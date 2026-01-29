def is_scam_message(message) -> bool:
    # ✅ Handle non-string inputs safely
    if not isinstance(message, str):
        return False

    msg = message.lower()

    scam_keywords = [
        "send money",
        "upi",
        "bank",
        "account",
        "otp",
        "urgent",
        "transfer"
    ]

    return any(keyword in msg for keyword in scam_keywords)
