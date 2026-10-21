"""
TTS backend for Project Mayhem Phase 1 Week 2.

Default: edge-tts (free, CPU, no API key) – works on Render free tier.
Later: swap in CosyVoice / fish-speech when GPU is available.
"""

from __future__ import annotations

import asyncio
import io
import logging
import os
from typing import Optional

logger = logging.getLogger("project-mayhem.speech")

DEFAULT_VOICE = os.getenv("TTS_VOICE", "en-US-JennyNeural")


async def synthesize_to_wav_bytes(
    text: str,
    voice: Optional[str] = None,
) -> bytes:
    text = (text or "").strip()
    if not text:
        raise ValueError("text must be non-empty")

    voice = voice or DEFAULT_VOICE

    try:
        import edge_tts
    except ImportError as e:
        raise RuntimeError(
            "edge-tts is not installed. Run: pip install edge-tts"
        ) from e

    communicate = edge_tts.Communicate(text, voice)
    mp3_buf = io.BytesIO()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            mp3_buf.write(chunk["data"])

    mp3_data = mp3_buf.getvalue()
    if not mp3_data:
        raise RuntimeError("TTS produced empty audio")

    logger.info(
        "TTS synthesized %d bytes for text_len=%d voice=%s",
        len(mp3_data),
        len(text),
        voice,
    )
    return mp3_data


def list_voices() -> list[str]:
    return [
        "en-US-JennyNeural",
        "en-US-GuyNeural",
        "en-GB-SoniaNeural",
        "en-IN-NeerjaNeural",
        "en-US-AriaNeural",
    ]


def synthesize_sync(text: str, voice: Optional[str] = None) -> bytes:
    return asyncio.run(synthesize_to_wav_bytes(text, voice=voice))
