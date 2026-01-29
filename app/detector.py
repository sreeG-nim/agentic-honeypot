def is_scam_message(message: str) -> bool:
    if not isinstance(message, str):
        return False

    keywords = [
        "otp", "upi", "bank", "urgent", "verify",
        "account", "transfer", "refund", "click",
        "police", "job", "crypto", "loan"
    ]

    return any(k in message.lower() for k in keywords)
