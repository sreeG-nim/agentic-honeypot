def is_scam_message(message: str) -> bool:
    keywords = [
        "otp", "urgent", "verify", "blocked",
        "kyc", "transfer", "account", "payment"
    ]
    msg = message.lower()
    return any(k in msg for k in keywords)
