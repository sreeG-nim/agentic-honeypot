def generate_agent_reply(message, history):
    msg = message.lower() if isinstance(message, str) else ""

    # First response after detection
    if not history:
        return (
            "Oh no, that sounds serious. I wasn’t aware of any issue. "
            "Which bank is this regarding?"
        )

    # If scammer mentions OTP
    if "otp" in msg:
        return (
            "I did receive some message but I’m not sure which one you mean. "
            "Can you tell me what sender name I should look for?"
        )

    # If scammer mentions account / transfer
    if "account" in msg or "send" in msg or "transfer" in msg:
        return (
            "I’m a bit confused — where exactly am I supposed to send this? "
            "Is there an account number or UPI ID I should use?"
        )

    # Fallback to keep engagement going
    return (
        "I’m trying to understand, but I’m not very technical. "
        "Can you please explain the steps slowly?"
    )
