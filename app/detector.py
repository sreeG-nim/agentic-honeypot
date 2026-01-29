def is_scam_message(message) -> bool:
    if not isinstance(message, str):
        return False

    msg = message.lower()

    scam_keywords = [
        "otp",
        "one time password",
        "account number",
        "bank security",
        "verify your account",
        "urgent",
        "suspended",
        "send money",
        "transfer",
        "upi",
        "click link",
        "secure your account",
    ]

    return any(keyword in msg for keyword in scam_keywords)
