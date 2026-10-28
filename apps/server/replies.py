"""
Simple reply logic for Phase 1 Week 4.
No LLM yet — clear rules a human can read and change.

Supports English and light Hinglish/Hindi for the Gnani contest demo.
"""

from __future__ import annotations

import os
import re


def _lang() -> str:
    return (os.getenv("REPLY_LANGUAGE") or "auto").strip().lower()


def _looks_hindi(text: str) -> bool:
    if re.search(r"[\u0900-\u097F]", text):
        return True
    hinglish = (
        "namaste",
        "namaskar",
        "kaise",
        "kaisa",
        "kya",
        "haan",
        "nahi",
        "theek",
        "shukriya",
        "dhanyavad",
        "bhai",
        "yaar",
    )
    lower = text.lower()
    return any(w in lower for w in hinglish)


def make_reply(user_text: str) -> str:
    """Return a short spoken reply for the given user message."""
    raw = (user_text or "").strip()
    text = raw.lower()

    use_hi = _lang() == "hi" or (_lang() == "auto" and _looks_hindi(raw))

    if not text:
        if use_hi:
            return "Main sun nahi paya. Kripya dobara boliye."
        return "I did not catch that. Please say something again."

    if any(w in text for w in ("hello", "hi", "hey", "namaste", "namaskar")):
        if use_hi or "namaste" in text or "namaskar" in text:
            return (
                "Namaste. Main Project Mayhem hoon, "
                "ek real-time video interaction agent. Aap kaise hain?"
            )
        return "Hello. I am Project Mayhem. How can I help you today?"

    if "name" in text or "naam" in text or "who are you" in text:
        if use_hi or "naam" in text:
            return (
                "Mera naam Project Mayhem hai. "
                "Main LiveKit par real-time baat karne wala agent hoon."
            )
        return "I am Project Mayhem, a real-time video interaction agent."

    if any(
        w in text
        for w in (
            "how are you",
            "how's it going",
            "kaise ho",
            "kaisa hai",
            "kya haal",
        )
    ):
        if use_hi or "kaise" in text or "kaisa" in text or "haal" in text:
            return "Main theek hoon, shukriya. Aap bataiye, kaise madad karun?"
        return "I am running well. Thanks for asking."

    if "help" in text or "madad" in text:
        if use_hi or "madad" in text:
            return (
                "Aap mujhe hello, apna naam, ya koi bhi sandesh bhej sakte hain. "
                "Main short reply bolunga. Gnani Timbre se awaaz aati hai jab key set ho."
            )
        return (
            "You can greet me, ask my name, or type any message. "
            "I will speak a short reply. Voice uses Gnani Timbre when the API key is set."
        )

    if "gnani" in text or "timbre" in text:
        return (
            "Yes. Project Mayhem can use Gnani Timbre for text to speech "
            "and is built for real-time video calls on LiveKit."
        )

    if any(
        w in text
        for w in ("bye", "goodbye", "see you", "alvida", "chalta", "phir milte")
    ):
        if use_hi or "alvida" in text or "milte" in text:
            return "Alvida. Phir milte hain."
        return "Goodbye. Talk to you soon."

    short = raw
    if len(short) > 80:
        short = short[:80] + "..."
    if use_hi:
        return f"Aapne kaha: {short}. Main sun raha hoon."
    return f"You said: {short}. Week four turn-taking is online."
