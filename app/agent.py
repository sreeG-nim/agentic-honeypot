import random


def generate_agent_reply(message, history):
    try:
        turns = len(history)
        text = " ".join(
            h.get("content", "").lower()
            for h in history
            if isinstance(h, dict)
        )

        # ==========================
        # MEMORY LAYER
        # ==========================
        mem = {
            "upi": "@" in text,
            "link": "http" in text,
            "otp": "otp" in text,
            "bank": any(b in text for b in ["bank", "sbi", "hdfc", "icici"]),
            "job": "job" in text,
            "crypto": "crypto" in text or "bitcoin" in text,
            "refund": "refund" in text,
            "police": "police" in text or "legal" in text,
            "repetition": (
                len(history) >= 2
                and history[-1].get("content") == history[-2].get("content")
            ),
        }

        # ==========================
        # SCENARIO LAYER
        # ==========================
        if mem["police"]:
            scenario = "authority"
        elif mem["otp"] or mem["bank"]:
            scenario = "bank"
        elif mem["upi"]:
            scenario = "payment"
        elif mem["link"]:
            scenario = "phishing"
        elif mem["job"]:
            scenario = "job"
        elif mem["crypto"]:
            scenario = "investment"
        elif mem["refund"]:
            scenario = "refund"
        else:
            scenario = "generic"

        # ==========================
        # STAGE LAYER
        # ==========================
        if turns <= 2:
            stage = "confusion"
        elif turns <= 5:
            stage = "anxiety"
        elif turns <= 8:
            stage = "cooperation"
        elif turns <= 12:
            stage = "hesitation"
        else:
            stage = "dependency"

        def pick(x):
            return random.choice(x)

        # ==========================
        # BEHAVIOR LAYER
        # ==========================
        if mem["repetition"]:
            return "You already mentioned this earlier… I’m trying to understand."

        if stage == "confusion":
            return pick([
                "Sorry… I wasn’t expecting this. What is this about?",
                "I’m a bit confused. Who exactly am I speaking with?",
                "This sounds serious… can you explain slowly?",
            ])

        if scenario == "bank":
            if mem["otp"]:
                return pick([
                    "The message says not to share OTP… why is it required?",
                    "I received two OTPs. Which one should I look at?",
                ])
            return pick([
                "Which bank account is this related to?",
                "Is this my main account or another one?",
            ])

        if scenario == "payment":
            if not mem["upi"]:
                return pick([
                    "You mean I need to send money? Or will I receive it?",
                    "I’m not good with UPI. Can you repeat the ID slowly?",
                ])
            return pick([
                "It says processing… should I wait?",
                "My app is loading very slowly.",
            ])

        if scenario == "phishing":
            return pick([
                "What exactly will open when I click the link?",
                "It looks different from my bank’s site. Is it safe?",
            ])

        if scenario == "job":
            return pick([
                "Is there any registration or joining fee?",
                "Where did you get my number from?",
            ])

        if scenario == "investment":
            return pick([
                "I don’t understand crypto much. Can I withdraw anytime?",
                "Why is this offer only valid today?",
            ])

        if scenario == "refund":
            return pick([
                "Which order is this refund for?",
                "I didn’t request a refund. Why was it initiated?",
            ])

        if scenario == "authority":
            return pick([
                "I didn’t receive any official notice. Will there be legal trouble?",
                "Can this be resolved today itself?",
            ])

        if stage == "hesitation":
            return pick([
                "My husband is asking what this is about.",
                "I’m feeling uneasy… are you sure this is safe?",
            ])

        if stage == "dependency":
            return pick([
                "Please don’t disconnect, I really need help.",
                "Sorry if I keep asking… I’m just scared to lose money.",
                "My phone battery is low, can we continue in a moment?",
            ])

        return "Can you explain that once more?"

    except Exception:
        return "Sorry… my phone is acting weird. Can you explain again?"
