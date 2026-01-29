import re

def extract_intelligence(message: str):
    if not isinstance(message, str):
        return {"bank_accounts": [], "upi_ids": [], "phishing_links": []}

    return {
        "bank_accounts": re.findall(r"\b\d{9,18}\b", message),
        "upi_ids": re.findall(r"[a-zA-Z0-9.\-_]+@[a-zA-Z]+", message),
        "phishing_links": re.findall(r"https?://\S+", message),
    }
