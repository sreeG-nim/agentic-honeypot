import random

RESPONSES = [
    "Sorry… I wasn’t expecting this. What is this about?",
    "This sounds serious. What exactly do I need to do?",
    "I’m a bit confused — why is this urgent?",
    "I’ve never had this happen before. Can you explain?",
    "Is my account really at risk right now?",
    "Please tell me clearly what you need from me."
]

def generate_agent_reply(message, history):
    return random.choice(RESPONSES)
