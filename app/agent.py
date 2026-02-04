import random

RESPONSES = [
    "Why is my account being suspended?",
    "This sounds serious. What exactly do I need to do?",
    "I wasn’t aware of this issue. Can you explain?",
    "Is my account blocked already?",
    "Please tell me how to fix this immediately.",
    "I’m worried — what verification do you need?"
]

def generate_agent_reply(message, history):
    return random.choice(RESPONSES)
