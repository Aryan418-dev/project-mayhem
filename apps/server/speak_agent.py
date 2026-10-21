"""
Project Mayhem – Week 2 Speak Agent
Token server + TTS publish into LiveKit room.

  GET  /health
  GET  /token
  POST /speak  { "text": "...", "room": "..." }
  GET  /voices
"""

from __future__ import annotations

import asyncio
import io
import logging
import os
import struct
from datetime import timedelta

from dotenv import load_dotenv
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("project-mayhem.speak-agent")

LIVEKIT_URL = os.getenv("LIVEKIT_URL", "ws://localhost:7880")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY", "devkey")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET", "secret")
ROOM_NAME = os.getenv("ROOM_NAME", "project-mayhem-room")
AGENT_IDENTITY = os.getenv("AGENT_NAME", "project-mayhem-agent")
PORT = int(os.environ.get("PORT", "8000"))


def generate_token(identity: str, room: str) -> str:
    from livekit import api

    token = (
        api.AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
        .with_identity(identity)
        .with_name(identity)
        .with_grants(
            api.VideoGrants(
                room_join=True,
                room=room,
                can_publish=True,
                can_subscribe=True,
            )
        )
    )
    return token.to_jwt()


def mp3_to_pcm16_mono(mp3_bytes: bytes, target_rate: int = 48000) -> tuple[bytes, int]:
    try:
        from pydub import AudioSegment
    except ImportError:
        logger.warning("pydub not available; cannot decode mp3")
        n = target_rate
        return struct.pack(f"<{n}h", *([0] * n)), target_rate

    seg = AudioSegment.from_file(io.BytesIO(mp3_bytes), format="mp3")
    seg = seg.set_frame_rate(target_rate).set_channels(1).set_sample_width(2)
    return seg.raw_data, target_rate


async def publish_pcm_audio(room, pcm: bytes, sample_rate: int = 48000) -> None:
    from livekit import rtc

    source = rtc.AudioSource(sample_rate, 1)
    track = rtc.LocalAudioTrack.create_audio_track("tts", source)
    options = rtc.TrackPublishOptions(source=rtc.TrackSource.SOURCE_MICROPHONE)
    publication = await room.local_participant.publish_track(track, options)
    logger.info("Published TTS track: %s", publication.sid)

    samples_per_channel = 480
    total_samples = len(pcm) // 2
    offset = 0

    while offset < total_samples:
        n = min(samples_per_channel, total_samples - offset)
        chunk = pcm[offset * 2 : (offset + n) * 2]
        if n < samples_per_channel:
            chunk = chunk + b"\x00" * ((samples_per_channel - n) * 2)
            n = samples_per_channel

        frame = rtc.AudioFrame(
            data=chunk,
            sample_rate=sample_rate,
            num_channels=1,
            samples_per_channel=n,
        )
        await source.capture_frame(frame)
        offset += samples_per_channel
        await asyncio.sleep(samples_per_channel / sample_rate)

    await asyncio.sleep(0.2)
    await room.local_participant.unpublish_track(publication.sid)
    logger.info("Unpublished TTS track")


async def speak_in_room(text: str, room_name: str | None = None) -> dict:
    from livekit import rtc
    from tts import synthesize_to_mp3_bytes

    room_name = room_name or ROOM_NAME
    room = rtc.Room()
    token = generate_token(AGENT_IDENTITY, room_name)

    logger.info("Connecting to %s room=%s", LIVEKIT_URL, room_name)
    await room.connect(LIVEKIT_URL, token)
    logger.info("Joined room as %s", room.local_participant.identity)

    try:
        mp3 = await synthesize_to_mp3_bytes(text)
        pcm, rate = mp3_to_pcm16_mono(mp3, target_rate=48000)
        await publish_pcm_audio(room, pcm, sample_rate=rate)
        return {"ok": True, "room": room_name, "text_len": len(text)}
    finally:
        await room.disconnect()
        logger.info("Disconnected")


app = FastAPI(title="Project Mayhem Speak + Token Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SpeakRequest(BaseModel):
    text: str
    room: str | None = None


@app.get("/health")
async def health():
    return {"status": "ok", "service": "speak-agent"}


@app.get("/token")
async def get_token(
    room: str = Query(default=ROOM_NAME),
    identity: str = Query(default="user"),
    name: str = Query(default="User"),
):
    from livekit.api import AccessToken, VideoGrants

    token = (
        AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
        .with_identity(identity)
        .with_name(name)
        .with_grants(
            VideoGrants(
                room_join=True,
                room=room,
                can_publish=True,
                can_subscribe=True,
            )
        )
        .with_ttl(timedelta(hours=2))
    )
    return {"token": token.to_jwt(), "url": LIVEKIT_URL, "room": room}


@app.post("/speak")
async def speak(req: SpeakRequest):
    if not req.text.strip():
        return {"ok": False, "error": "empty text"}
    try:
        result = await speak_in_room(req.text.strip(), room_name=req.room)
        return result
    except Exception as e:
        logger.exception("speak failed")
        return {"ok": False, "error": str(e)}


@app.get("/voices")
async def voices():
    from tts import list_voices

    return {"voices": list_voices()}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=PORT)
