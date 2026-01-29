def generate_agent_reply(message: str, history: list) -> str:
    """
    Simple rule-based agent to engage scammers.
    """

    msg = message.lower()

    if "link" in msg:
        return "I tried opening the link but it didn’t work properly. Can you send it again?"

    if "upi" in msg:
        return "I’m not very familiar with UPI. Which UPI ID should I send it to?"

    if "bank" in msg or "account" in msg:
        return "Okay… which bank account is this? Can you share the details so I don’t make a mistake?"

    if "otp" in msg:
        return "I received an OTP but I’m not sure if I should share it. Is there another way?"

    return "I’m really worried. Please guide me step by step."
