import re

UPI_REGEX = r"[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}"
URL_REGEX = r"https?://[^\s]+"
BANK_REGEX = r"\b\d{9,18}\b"

def extract_intelligence(message: str):
    return {
        "bank_accounts": re.findall(BANK_REGEX, message),
        "upi_ids": re.findall(UPI_REGEX, message),
        "phishing_links": re.findall(URL_REGEX, message),
    }
