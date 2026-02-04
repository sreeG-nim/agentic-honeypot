def is_scam_message(message) -> bool:
    """
    Defensive scam detection.
    Accepts ANY input type safely.
    """

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

    return any(keyword in msg for keyword in keywords)
