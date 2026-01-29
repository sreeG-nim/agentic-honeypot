import re

UPI_REGEX = r"\b[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}\b"
BANK_ACCOUNT_REGEX = r"\b\d{9,18}\b"
URL_REGEX = r"https?://[^\s]+"


def extract_intelligence(message: str) -> dict:
    return {
        "upi_ids": re.findall(UPI_REGEX, message),
        "bank_accounts": re.findall(BANK_ACCOUNT_REGEX, message),
        "phishing_links": re.findall(URL_REGEX, message),
    }
