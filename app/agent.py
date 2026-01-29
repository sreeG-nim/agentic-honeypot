def generate_agent_reply(message, history):
    msg = message.lower() if isinstance(message, str) else ""

    # First engagement after detection
    if not history:
        return (
            "That sounds serious… I wasn’t aware of any issue. "
            "Which bank is this regarding?"
        )

    # If scammer asks for OTP
    if "otp" in msg:
        return (
            "I received a few messages just now and I’m a bit confused. "
            "Can you tell me which message or sender name I should look for?"
        )

    # If scammer asks for account / transfer
    if "account" in msg or "send" in msg or "transfer" in msg or "upi" in msg:
        return (
            "I want to fix this quickly but I’m not sure where to send anything. "
            "Can you share the account number or UPI ID again?"
        )

    # If scammer mentions link
    if "link" in msg or "click" in msg:
        return (
            "I’m not very comfortable clicking links. "
            "Can you explain what will happen after I open it?"
        )

    # Keep the scammer engaged
    return (
        "I’m getting a bit worried now. "
        "Can you please guide me step by step?"
    )
