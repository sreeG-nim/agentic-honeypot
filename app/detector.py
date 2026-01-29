def is_scam_message(message: str) -> bool:
    if not isinstance(message, str):
        return False

    keywords = [
        "otp", "upi", "bank", "urgent", "verify",
        "account", "transfer", "refund", "click",
        "police", "loan", "crypto", "job"
    ]

    msg = message.lower()
    return any(k in msg for k in keywords)
