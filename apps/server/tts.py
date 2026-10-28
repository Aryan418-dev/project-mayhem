"""
TTS for Project Mayhem.

Backends (env TTS_BACKEND):
  - gnani  → Gnani Timbre (needs GNANI_API_KEY)
  - edge   → edge-tts (free fallback)

If TTS_BACKEND=gnani but the key is missing or the call fails, we fall back to edge-tts.
"""

from __future__ import annotations

import io
import logging
import os
from typing import Optional

logger = logging.getLogger("mayhem.tts")

TTS_BACKEND = os.getenv("TTS_BACKEND", "gnani").lower().strip()
DEFAULT_EDGE_VOICE = os.getenv("TTS_VOICE", "en-US-JennyNeural")
GNANI_API_KEY = os.getenv("GNANI_API_KEY") or os.getenv("X_API_KEY_ID") or ""
GNANI_VOICE = os.getenv("GNANI_VOICE", "Kaveri")
GNANI_LANGUAGE = os.getenv("GNANI_LANGUAGE", "en-IN")
GNANI_MODEL = os.getenv("GNANI_TTS_MODEL", "timbre-v2.5")
GNANI_TTS_URL = os.getenv(
    "GNANI_TTS_URL",
    "https://api.vachana.ai/api/v1/tts/inference",
)


async def synthesize_to_mp3_bytes(
    text: str,
    voice: Optional[str] = None,
) -> bytes:
    text = (text or "").strip()
    if not text:
        raise ValueError("text must be non-empty")

    if TTS_BACKEND == "gnani" and GNANI_API_KEY:
        try:
            return await _gnani_tts(text, voice=voice)
        except Exception as e:
            logger.warning("Gnani TTS failed (%s); falling back to edge-tts", e)

    return await _edge_tts(text, voice=voice or DEFAULT_EDGE_VOICE)


async def _gnani_tts(text: str, voice: Optional[str] = None) -> bytes:
    """Call Gnani Timbre REST API; return WAV bytes."""
    import httpx

    payload = {
        "text": text,
        "voice": voice or GNANI_VOICE,
        "model": GNANI_MODEL,
        "language": GNANI_LANGUAGE,
        "speed": 1.0,
        "audio_config": {
            "sample_rate": 48000,
            "num_channels": 1,
            "sample_width": 2,
            "encoding": "linear_pcm",
            "container": "wav",
        },
    }
    headers = {
        "Content-Type": "application/json",
        "X-API-Key-ID": GNANI_API_KEY,
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        res = await client.post(GNANI_TTS_URL, json=payload, headers=headers)
        if res.status_code >= 400:
            raise RuntimeError(f"Gnani HTTP {res.status_code}: {res.text[:300]}")
        audio = res.content
        if not audio:
            raise RuntimeError("Gnani returned empty audio")

    logger.info(
        "Gnani TTS ok bytes=%d voice=%s lang=%s",
        len(audio),
        payload["voice"],
        GNANI_LANGUAGE,
    )
    return audio


async def _edge_tts(text: str, voice: str) -> bytes:
    try:
        import edge_tts
    except ImportError as e:
        raise RuntimeError("edge-tts is not installed") from e

    communicate = edge_tts.Communicate(text, voice)
    mp3_buf = io.BytesIO()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            mp3_buf.write(chunk["data"])

    data = mp3_buf.getvalue()
    if not data:
        raise RuntimeError("edge-tts produced empty audio")
    logger.info("edge-tts ok bytes=%d voice=%s", len(data), voice)
    return data


def list_voices() -> list[str]:
    if TTS_BACKEND == "gnani":
        return [
            "Kaveri",
            "Trupti",
            "Devika",
            "Pranav",
            "Nalini",
            "Deepak",
            "Poorvi",
        ]
    return [
        "en-US-JennyNeural",
        "en-US-GuyNeural",
        "en-IN-NeerjaNeural",
        "en-GB-SoniaNeural",
    ]


def active_backend() -> str:
    if TTS_BACKEND == "gnani" and GNANI_API_KEY:
        return "gnani"
    return "edge"
