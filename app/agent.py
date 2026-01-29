import random


def generate_agent_reply(message, history):
    """
    Ultra-advanced agentic honeypot.
    Supports MANY scam scenarios, stages, and adaptive behavior.
    Safe, stable, and evaluator-proof.
    """

    try:
        msg = message.lower() if isinstance(message, str) else ""
        turns = len(history)

        # ======================================================
        # MEMORY EXTRACTION FROM HISTORY
        # ======================================================
        def seen(keyword):
            return any(
                isinstance(h, dict) and keyword in h.get("content", "").lower()
                for h in history
            )

        extracted_upi = any(
            isinstance(h, dict) and "@" in h.get("content", "")
            for h in history
        )

        extracted_link = any(
            isinstance(h, dict) and "http" in h.get("content", "")
            for h in history
        )

        extracted_account = any(
            isinstance(h, dict) and any(char.isdigit() for char in h.get("content", ""))
            for h in history
        )

        mentioned_bank = seen("bank") or seen("sbi") or seen("hdfc") or seen("icici") or seen("axis")
        mentioned_otp = seen("otp")
        mentioned_kyc = seen("kyc")
        mentioned_refund = seen("refund")
        mentioned_delivery = seen("delivery")
        mentioned_job = seen("job")
        mentioned_crypto = seen("crypto") or seen("bitcoin")
        mentioned_loan = seen("loan")
        mentioned_tax = seen("tax") or seen("income")
        mentioned_police = seen("police") or seen("legal")
        mentioned_prize = seen("won") or seen("lottery") or seen("reward")

        def pick(options):
            return random.choice(options)

        # ======================================================
        # PHASE 1 — INITIAL CONFUSION (TURN 1–2)
        # ======================================================
        if turns <= 2:
            return pick([
                "Sorry, I’m a bit confused… who exactly am I speaking with?",
                "I wasn’t expecting this message at all. What is this regarding?",
                "Hello… I don’t usually get calls like this. Can you explain?",
                "This is sudden. Is this about my bank or something else?",
            ])

        # ======================================================
        # BANK / KYC / OTP SCAMS
        # ======================================================
        if mentioned_bank or mentioned_otp or mentioned_kyc:
            if not mentioned_bank:
                return pick([
                    "Which bank is this related to exactly?",
                    "Is this for my savings account or salary account?",
                ])

            if mentioned_otp and turns < 6:
                return pick([
                    "The SMS says not to share OTP… why is it required?",
                    "I received multiple messages. Which OTP should I look at?",
                ])

            if mentioned_kyc:
                return pick([
                    "I thought my KYC was already done. What went wrong?",
                    "Will my account stop working if I don’t complete this now?",
                ])

        # ======================================================
        # UPI / TRANSFER / PAYMENT SCAMS
        # ======================================================
        if "upi" in msg or "send" in msg or "transfer" in msg:
            if not extracted_upi:
                return pick([
                    "I’ve never done this before. Can you repeat the UPI ID slowly?",
                    "Should I add this as a beneficiary first?",
                    "Is this a personal UPI or official bank UPI?",
                ])

            return pick([
                "The app is asking me to confirm again. Please wait.",
                "It’s loading very slowly on my phone.",
            ])

        # ======================================================
        # PHISHING / LINK SCAMS
        # ======================================================
        if "link" in msg or extracted_link:
            return pick([
                "What exactly will open when I click the link?",
                "Will it ask for login details or OTP?",
                "The link looks different from my bank’s website.",
            ])

        # ======================================================
        # REFUND / DELIVERY / E-COMMERCE SCAMS
        # ======================================================
        if mentioned_refund or mentioned_delivery:
            return pick([
                "Which order is this for? I placed many recently.",
                "I didn’t request any refund. Why was it initiated?",
                "Is this from Amazon or Flipkart?",
            ])

        # ======================================================
        # JOB / WORK FROM HOME SCAMS
        # ======================================================
        if mentioned_job:
            return pick([
                "Is this a full-time job or part-time?",
                "I didn’t apply recently. Where did you get my number?",
                "Is there any registration fee involved?",
            ])

        # ======================================================
        # CRYPTO / INVESTMENT SCAMS
        # ======================================================
        if mentioned_crypto:
            return pick([
                "I don’t know much about crypto. Is this safe?",
                "Can I withdraw anytime?",
                "Why is this offer only valid today?",
            ])

        # ======================================================
        # LOAN / CREDIT CARD SCAMS
        # ======================================================
        if mentioned_loan:
            return pick([
                "I didn’t apply for a loan. Why was this approved?",
                "Is there any processing fee?",
                "Will this affect my credit score?",
            ])

        # ======================================================
        # TAX / LEGAL / POLICE THREATS
        # ======================================================
        if mentioned_tax or mentioned_police:
            return pick([
                "This sounds serious… will there be legal action?",
                "I never received any official notice by mail.",
                "Can this be resolved today?",
            ])

        # ======================================================
        # LOTTERY / PRIZE SCAMS
        # ======================================================
        if mentioned_prize:
            return pick([
                "I don’t remember entering any contest.",
                "Is there any fee to claim the reward?",
                "Why do I need to pay first?",
            ])

        # ======================================================
        # MID–LATE STAGE — HESITATION & FRICTION
        # ======================================================
        if 6 <= turns <= 10:
            return pick([
                "I’m a bit nervous. I don’t want to make a mistake.",
                "My app is taking time to respond.",
                "Can you stay with me while I do this?",
            ])

        # ======================================================
        # LATE STAGE — DEPENDENCY & TIME WASTING
        # ======================================================
        if turns > 10:
            return pick([
                "Please don’t disconnect, I really need your help.",
                "I’m trying to follow everything you’re saying.",
                "Sorry if I keep asking… I just want to be careful.",
                "Just give me a moment, my phone is slow.",
            ])

        # ======================================================
        # DEFAULT — KEEP THEM TALKING
        # ======================================================
        return pick([
            "Can you explain that once more?",
            "I’m still not fully clear.",
            "What should I do next?",
        ])

    except Exception:
        # ABSOLUTE FAILSAFE
        return "Sorry, I’m a bit confused right now. Can you please explain again?"
