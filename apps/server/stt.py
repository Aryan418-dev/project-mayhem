"""
Speech-to-text via Gnani Prisma (REST).

POST https://api.vachana.ai/stt/v3
Uses the same GNANI_API_KEY as Timbre TTS.
"""

from __future__ import annotations

import logging
import os
from typing import Optional

import httpx

logger = logging.getLogger("mayhem.stt")

STT_URL = os.getenv("GNANI_STT_URL", "https://api.vachana.ai/stt/v3")
STT_MODEL = os.getenv("GNANI_STT_MODEL", "prisma-v3.0")
STT_LANGUAGE = os.getenv("GNANI_STT_LANGUAGE", "indic-auto")


def _clean(value: Optional[str]) -> str:
    if not value:
        return ""
    return value.strip().strip('"').strip("'")


def get_api_key() -> str:
    for name in ("GNANI_API_KEY", "X_API_KEY_ID", "GNANI_KEY"):
        val = _clean(os.getenv(name))
        if val:
            return val
    return ""


def stt_ready() -> bool:
    return bool(get_api_key())


async def transcribe_audio(
    audio_bytes: bytes,
    filename: str = "audio.wav",
    content_type: str = "audio/wav",
    language_code: Optional[str] = None,
) -> dict:
    """
    Send short audio (≤30s) to Prisma. Returns:
      { "ok": True, "transcript": "...", "model": "...", "language": "..." }
    or
      { "ok": False, "error": "..." }
    """
    key = get_api_key()
    if not key:
        return {"ok": False, "error": "GNANI_API_KEY not set"}

    if not audio_bytes:
        return {"ok": False, "error": "empty audio"}

    lang = language_code or STT_LANGUAGE
    headers = {"X-API-Key-ID": key}
    files = {"audio_file": (filename, audio_bytes, content_type)}
    data = {
        "model": STT_MODEL,
        "language_code": lang,
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            res = await client.post(STT_URL, headers=headers, files=files, data=data)
    except Exception as e:
        logger.warning("Prisma STT request failed: %s", e)
        return {"ok": False, "error": str(e)}

    if res.status_code >= 400:
        snippet = res.text[:300]
        logger.warning("Prisma STT HTTP %s: %s", res.status_code, snippet)
        return {"ok": False, "error": f"HTTP {res.status_code}: {snippet}"}

    try:
        body = res.json()
    except Exception:
        return {"ok": False, "error": "invalid JSON from Prisma"}

    transcript = body.get("transcript") or ""
    if isinstance(transcript, dict):
        # older shapes sometimes nested text
        transcript = transcript.get("text") or str(transcript)

    return {
        "ok": True,
        "transcript": (transcript or "").strip(),
        "model": body.get("model") or STT_MODEL,
        "language": body.get("detected_language_code") or lang,
        "request_id": body.get("request_id"),
    }
