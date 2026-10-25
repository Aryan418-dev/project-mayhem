"""
Simple reply logic for Phase 1 Week 4.
No LLM yet — clear rules a human can read and change.
"""


def make_reply(user_text: str) -> str:
    """Return a short spoken reply for the given user message."""
    text = (user_text or "").strip().lower()

    if not text:
        return "I did not catch that. Please say something again."

    if any(word in text for word in ("hello", "hi", "hey")):
        return "Hello. I am Project Mayhem. How can I help you today?"

    if "name" in text:
        return "I am Project Mayhem, a real-time video interaction agent."

    if any(word in text for word in ("how are you", "how's it going")):
        return "I am running well. Thanks for asking."

    if any(word in text for word in ("bye", "goodbye", "see you")):
        return "Goodbye. Talk to you soon."

    if "help" in text:
        return (
            "You can greet me, ask my name, or type any message. "
            "I will speak a short reply. Real lip-sync video needs a GPU host."
        )

    # Default: acknowledge what they said
    short = user_text.strip()
    if len(short) > 80:
        short = short[:80] + "..."
    return f"You said: {short}. Week four turn-taking is online."
