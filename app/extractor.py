import re

UPI_REGEX = r"[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}"
BANK_REGEX = r"\b\d{9,18}\b"
URL_REGEX = r"https?://[^\s]+"


def extract_intelligence(message):
    # Defensive: extractor never crashes
    if not isinstance(message, str):
        return {
            "bank_accounts": [],
            "upi_ids": [],
            "phishing_links": []
        }

    return {
        "bank_accounts": re.findall(BANK_REGEX, message),
        "upi_ids": re.findall(UPI_REGEX, message),
        "phishing_links": re.findall(URL_REGEX, message)
    }
