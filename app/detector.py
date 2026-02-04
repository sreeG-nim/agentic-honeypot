def is_scam_message(message) -> bool:
    if not isinstance(message, str):
        return False

    msg = message.lower()

    keywords = [
        "otp",
        "urgent",
        "blocked",
        "verify",
        "kyc",
        "transfer",
        "account",
        "upi",
        "suspended",
        "security",
        "fraud"
    ]

    return any(k in msg for k in keywords)
