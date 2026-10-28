"""
TTS for Project Mayhem.

Backends (env TTS_BACKEND):
  - gnani  → Gnani Timbre (needs GNANI_API_KEY)
  - edge   → edge-tts (free fallback)

Env is read at call time so Render restarts pick up new keys reliably.
"""

from __future__ import annotations

import io
import logging
import os
from typing import Optional

logger = logging.getLogger("mayhem.tts")

DEFAULT_EDGE_VOICE = os.getenv("TTS_VOICE", "en-US-JennyNeural")
GNANI_TTS_URL = os.getenv(
    "GNANI_TTS_URL",
    "https://api.vachana.ai/api/v1/tts/inference",
)


def _clean(value: Optional[str]) -> str:
    if not value:
        return ""
    return value.strip().strip('"').strip("'")


def get_tts_backend() -> str:
    return _clean(os.getenv("TTS_BACKEND", "gnani")).lower() or "gnani"


def get_gnani_api_key() -> str:
    """Try several common names people use in the Render dashboard."""
    candidates = [
        "GNANI_API_KEY",
        "X_API_KEY_ID",
        "GNANI_KEY",
        "GNANI_API_KEY_ID",
        "VACHANA_API_KEY",
        "API_KEY_ID",
    ]
    for name in candidates:
        val = _clean(os.getenv(name))
        if val:
            return val
    return ""


def get_gnani_voice() -> str:
    return _clean(os.getenv("GNANI_VOICE")) or "Kaveri"


def get_gnani_language() -> str:
    return _clean(os.getenv("GNANI_LANGUAGE")) or "en-IN"


def get_gnani_model() -> str:
    return _clean(os.getenv("GNANI_TTS_MODEL")) or "timbre-v2.5"


def active_backend() -> str:
    if get_tts_backend() == "gnani" and get_gnani_api_key():
        return "gnani"
    return "edge"


def debug_env() -> dict:
    """Safe diagnostics — never returns the secret itself."""
    key = get_gnani_api_key()
    found_name = None
    for name in (
        "GNANI_API_KEY",
        "X_API_KEY_ID",
        "GNANI_KEY",
        "GNANI_API_KEY_ID",
        "VACHANA_API_KEY",
        "API_KEY_ID",
    ):
        if _clean(os.getenv(name)):
            found_name = name
            break
    return {
        "tts_backend_setting": get_tts_backend(),
        "active_tts": active_backend(),
        "has_gnani_key": bool(key),
        "gnani_key_env_name": found_name,
        "gnani_key_length": len(key) if key else 0,
        "gnani_voice": get_gnani_voice(),
        "gnani_language": get_gnani_language(),
        "gnani_model": get_gnani_model(),
    }


async def synthesize_to_mp3_bytes(
    text: str,
    voice: Optional[str] = None,
) -> bytes:
    text = (text or "").strip()
    if not text:
        raise ValueError("text must be non-empty")

    backend = get_tts_backend()
    key = get_gnani_api_key()

    if backend == "gnani" and key:
        try:
            return await _gnani_tts(text, voice=voice, api_key=key)
        except Exception as e:
            logger.warning("Gnani TTS failed (%s); falling back to edge-tts", e)
    elif backend == "gnani" and not key:
        logger.warning(
            "TTS_BACKEND=gnani but no API key found; using edge-tts"
        )

    return await _edge_tts(text, voice=voice or DEFAULT_EDGE_VOICE)


async def _gnani_tts(
    text: str,
    voice: Optional[str] = None,
    api_key: str = "",
) -> bytes:
    import httpx

    payload = {
        "text": text,
        "voice": voice or get_gnani_voice(),
        "model": get_gnani_model(),
        "language": get_gnani_language(),
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
        "X-API-Key-ID": api_key,
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
        get_gnani_language(),
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
    if get_tts_backend() == "gnani":
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
