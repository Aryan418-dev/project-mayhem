"""
Project Mayhem server – one process for token, TTS, chat, STT, video.

Endpoints:
  GET  /health
  GET  /token
  POST /speak       JSON { text, room? }
  POST /chat        JSON { message, room? }
  POST /transcribe  multipart audio_file
  POST /voice-chat  multipart audio_file + optional room
  GET  /voices
"""

from __future__ import annotations

import asyncio
import io
import logging
import os
from datetime import timedelta

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger("mayhem")

LIVEKIT_URL = os.getenv("LIVEKIT_URL", "ws://localhost:7880")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY", "devkey")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET", "secret")
ROOM_NAME = os.getenv("ROOM_NAME", "project-mayhem-room")
AGENT_NAME = os.getenv("AGENT_NAME", "project-mayhem-agent")
PORT = int(os.environ.get("PORT", "8000"))
ENABLE_VIDEO = os.getenv("ENABLE_VIDEO", "true").lower() in ("1", "true", "yes")


def make_livekit_token(identity: str, room: str) -> str:
    from livekit import api

    return (
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
        .to_jwt()
    )


def audio_bytes_to_pcm(audio_bytes: bytes, sample_rate: int = 48000) -> bytes:
    """Decode TTS wav/mp3 to 16-bit mono PCM."""
    from pydub import AudioSegment

    audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
    audio = audio.set_frame_rate(sample_rate).set_channels(1).set_sample_width(2)
    return audio.raw_data


def make_face_jpeg(size: int = 512) -> bytes:
    from PIL import Image, ImageDraw

    img = Image.new("RGB", (size, size), color=(40, 40, 60))
    draw = ImageDraw.Draw(img)
    draw.ellipse([size * 0.3, size * 0.22, size * 0.7, size * 0.62], fill=(220, 190, 170))
    draw.ellipse([size * 0.38, size * 0.35, size * 0.45, size * 0.42], fill=(30, 30, 30))
    draw.ellipse([size * 0.55, size * 0.35, size * 0.62, size * 0.42], fill=(30, 30, 30))
    draw.arc(
        [size * 0.42, size * 0.45, size * 0.58, size * 0.55],
        0,
        180,
        fill=(120, 60, 60),
        width=3,
    )
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return buf.getvalue()


def load_face_image() -> bytes:
    path = os.getenv("REFERENCE_IMAGE_PATH", "")
    if path and os.path.isfile(path):
        with open(path, "rb") as f:
            return f.read()
    return make_face_jpeg()


async def publish_audio(room, pcm: bytes, sample_rate: int = 48000) -> None:
    from livekit import rtc

    source = rtc.AudioSource(sample_rate, 1)
    track = rtc.LocalAudioTrack.create_audio_track("tts", source)
    pub = await room.local_participant.publish_track(
        track,
        rtc.TrackPublishOptions(source=rtc.TrackSource.SOURCE_MICROPHONE),
    )
    log.info("audio track published %s", pub.sid)

    samples_per_chunk = sample_rate // 100
    total_samples = len(pcm) // 2
    offset = 0
    while offset < total_samples:
        n = min(samples_per_chunk, total_samples - offset)
        chunk = pcm[offset * 2 : (offset + n) * 2]
        if n < samples_per_chunk:
            chunk = chunk + b"\x00" * ((samples_per_chunk - n) * 2)
            n = samples_per_chunk
        frame = rtc.AudioFrame(
            data=chunk,
            sample_rate=sample_rate,
            num_channels=1,
            samples_per_channel=n,
        )
        await source.capture_frame(frame)
        offset += samples_per_chunk
        await asyncio.sleep(n / sample_rate)

    await asyncio.sleep(0.15)
    await room.local_participant.unpublish_track(pub.sid)


async def publish_face_video(room, duration_sec: float, fps: int = 15) -> None:
    from livekit import rtc
    from PIL import Image
    import numpy as np

    jpeg = load_face_image()
    img = Image.open(io.BytesIO(jpeg)).convert("RGB")
    width, height = img.size
    width, height = width - (width % 2), height - (height % 2)
    img = img.resize((width, height))
    rgba_bytes = np.array(img.convert("RGBA")).tobytes()

    source = rtc.VideoSource(width, height)
    track = rtc.LocalVideoTrack.create_video_track("avatar", source)
    pub = await room.local_participant.publish_track(
        track,
        rtc.TrackPublishOptions(source=rtc.TrackSource.SOURCE_CAMERA),
    )
    log.info("video track published %s (%dx%d)", pub.sid, width, height)

    frame_count = max(1, int(duration_sec * fps))
    for _ in range(frame_count):
        frame = rtc.VideoFrame(width, height, rtc.VideoBufferType.RGBA, rgba_bytes)
        source.capture_frame(frame)
        await asyncio.sleep(1.0 / fps)

    await room.local_participant.unpublish_track(pub.sid)


async def speak_in_room(text: str, room_name: str | None = None) -> dict:
    from livekit import rtc
    from tts import synthesize_to_mp3_bytes

    room_name = room_name or ROOM_NAME
    room = rtc.Room()
    token = make_livekit_token(AGENT_NAME, room_name)

    log.info("connecting to %s room=%s", LIVEKIT_URL, room_name)
    await room.connect(LIVEKIT_URL, token)

    try:
        audio = await synthesize_to_mp3_bytes(text)
        pcm = audio_bytes_to_pcm(audio, sample_rate=48000)
        duration = (len(pcm) // 2) / 48000.0

        jobs = [publish_audio(room, pcm)]
        if ENABLE_VIDEO:
            jobs.append(publish_face_video(room, duration_sec=duration + 0.3))

        await asyncio.gather(*jobs)
        return {
            "ok": True,
            "room": room_name,
            "duration_sec": round(duration, 2),
            "video": ENABLE_VIDEO,
        }
    finally:
        await room.disconnect()


app = FastAPI(title="Project Mayhem")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SpeakBody(BaseModel):
    text: str
    room: str | None = None


class ChatBody(BaseModel):
    message: str
    room: str | None = None


@app.get("/health")
async def health():
    from tts import active_backend, debug_env
    from stt import stt_ready

    info = debug_env()
    return {
        "status": "ok",
        "service": "speak-agent",
        "video": ENABLE_VIDEO,
        "week": 5,
        "tts": active_backend(),
        "stt": "prisma" if stt_ready() else "none",
        "tts_debug": info,
        "features": ["token", "speak", "chat", "gnani-tts", "prisma-stt"],
    }


@app.get("/token")
async def token(
    room: str = Query(default=ROOM_NAME),
    identity: str = Query(default="user"),
    name: str = Query(default="User"),
):
    from livekit.api import AccessToken, VideoGrants

    t = (
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
    return {"token": t.to_jwt(), "url": LIVEKIT_URL, "room": room}


@app.post("/speak")
async def speak(body: SpeakBody):
    if not body.text.strip():
        return {"ok": False, "error": "text is empty"}
    try:
        return await speak_in_room(body.text.strip(), room_name=body.room)
    except Exception as e:
        log.exception("speak failed")
        return {"ok": False, "error": str(e)}


@app.post("/chat")
async def chat(body: ChatBody):
    from replies import make_reply

    if not body.message.strip():
        return {"ok": False, "error": "message is empty"}

    reply = make_reply(body.message)
    try:
        result = await speak_in_room(reply, room_name=body.room)
        result["reply"] = reply
        result["user_message"] = body.message.strip()
        return result
    except Exception as e:
        log.exception("chat failed")
        return {"ok": False, "error": str(e), "reply": reply}


@app.post("/transcribe")
async def transcribe(
    audio_file: UploadFile = File(...),
    language_code: str | None = Form(default=None),
):
    """Upload short audio → Prisma transcript (no speak)."""
    from stt import transcribe_audio

    data = await audio_file.read()
    filename = audio_file.filename or "audio.wav"
    content_type = audio_file.content_type or "audio/wav"
    result = await transcribe_audio(
        data,
        filename=filename,
        content_type=content_type,
        language_code=language_code,
    )
    return result


@app.post("/voice-chat")
async def voice_chat(
    audio_file: UploadFile = File(...),
    room: str | None = Form(default=None),
    language_code: str | None = Form(default=None),
):
    """Upload short audio → Prisma STT → reply → speak in room."""
    from replies import make_reply
    from stt import transcribe_audio

    data = await audio_file.read()
    filename = audio_file.filename or "audio.wav"
    content_type = audio_file.content_type or "audio/wav"

    stt = await transcribe_audio(
        data,
        filename=filename,
        content_type=content_type,
        language_code=language_code,
    )
    if not stt.get("ok"):
        return {"ok": False, "error": stt.get("error", "stt failed"), "stage": "stt"}

    user_text = stt.get("transcript") or ""
    if not user_text:
        return {
            "ok": False,
            "error": "empty transcript",
            "stage": "stt",
            "stt": stt,
        }

    reply = make_reply(user_text)
    try:
        result = await speak_in_room(reply, room_name=room)
        result["user_message"] = user_text
        result["reply"] = reply
        result["stt"] = {
            "model": stt.get("model"),
            "language": stt.get("language"),
        }
        return result
    except Exception as e:
        log.exception("voice-chat speak failed")
        return {
            "ok": False,
            "error": str(e),
            "stage": "speak",
            "user_message": user_text,
            "reply": reply,
        }


@app.get("/voices")
async def voices():
    from tts import list_voices

    return {"voices": list_voices()}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=PORT)
