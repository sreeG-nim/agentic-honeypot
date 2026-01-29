import random

def generate_agent_reply(message, history):
    msg = message.lower() if isinstance(message, str) else ""
    turns = len(history)

    def pick(x): return random.choice(x)

    def seen(word):
        return any(word in h.get("content","").lower() for h in history if isinstance(h, dict))

    extracted_upi = seen("@")
    extracted_link = seen("http")
    mentioned_bank = seen("bank") or seen("sbi") or seen("hdfc") or seen("icici")
    mentioned_otp = seen("otp")
    mentioned_job = seen("job")
    mentioned_crypto = seen("crypto") or seen("bitcoin")
    mentioned_refund = seen("refund")
    mentioned_police = seen("police") or seen("legal")

    # PHASE 1 – CONFUSION
    if turns <= 2:
        return pick([
            "Sorry… I wasn’t expecting this. What is this about?",
            "Hello? I’m a bit confused, who is this?",
            "This sounds serious… can you explain slowly?",
        ])

    # BANK / OTP / KYC
    if mentioned_bank or mentioned_otp:
        if not mentioned_bank:
            return pick([
                "Which bank is this related to?",
                "Is this my savings account or salary account?",
            ])
        if mentioned_otp:
            return pick([
                "The SMS says not to share OTP… why is it needed?",
                "I got two OTPs, which one do you want?",
            ])

    # PAYMENT / UPI
    if "send" in msg or "transfer" in msg or "upi" in msg:
        if not extracted_upi:
            return pick([
                "I’m not very good with UPI. Can you repeat the ID?",
                "Is this a personal UPI or official bank UPI?",
            ])
        return pick([
            "It’s loading… please wait.",
            "My app is asking to confirm again.",
        ])

    # PHISHING LINKS
    if "link" in msg or extracted_link:
        return pick([
            "What will open when I click the link?",
            "Is it safe? My phone shows a warning.",
        ])

    # JOB SCAMS
    if mentioned_job:
        return pick([
            "Is this part-time or full-time?",
            "Is there any registration fee?",
        ])

    # CRYPTO / INVESTMENT
    if mentioned_crypto:
        return pick([
            "I don’t understand crypto much. Is this guaranteed?",
            "Can I withdraw anytime?",
        ])

    # REFUND SCAMS
    if mentioned_refund:
        return pick([
            "Which order is this refund for?",
            "I didn’t request a refund… why was it initiated?",
        ])

    # POLICE / LEGAL
    if mentioned_police:
        return pick([
            "Will there be legal trouble?",
            "I didn’t get any official notice.",
        ])

    # LATE STAGE – DEPENDENCY
    if turns > 8:
        return pick([
            "Please don’t disconnect, I’m really worried.",
            "I trust you, just guide me step by step.",
            "Sorry for asking again… I just want to be careful.",
        ])

    return pick([
        "Can you explain again?",
        "What should I do next?",
    ])
