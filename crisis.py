from typing import List

# List of words that may indicate crisis or self-harm intent
CRISIS_KEYWORDS: List[str] = [
    "suicide", "suicidal", "kill myself", "end my life", "depressed",
    "hopeless", "worthless", "helpless", "overwhelmed", "anxious", "no reason to live"
]

# Supportive message for users showing crisis-related language
SAFETY_MESSAGE = (
    "It sounds like you're going through a really tough time right now. "
    "Please remember that you're not alone — there are people who care about you and want to help.\n\n"
    "Consider reaching out to a mental health professional or a trusted person in your life.\n"
    "If you're in immediate danger, please contact emergency services or go to the nearest emergency room.\n\n"
    "Govt of India initiative — Free, 24/7 mental health support:\n"
    "Call 14416 to connect.\n\n"
    "You are not alone. You matter."
)

def contains_crisis_keywords(user_input: str) -> bool:
    """
    Returns True if the user's message contains any crisis-related keywords.
    """
    user_input_lower = user_input.lower()
    return any(keyword in user_input_lower for keyword in CRISIS_KEYWORDS)
