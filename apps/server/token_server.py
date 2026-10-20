"""
Simple token server for Project Mayhem frontend.
Generates LiveKit access tokens so the browser can join rooms.
Run this alongside the main agent (or combine later).
"""

import os
from datetime import timedelta

from dotenv import load_dotenv
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from livekit.api import AccessToken, VideoGrants

load_dotenv()

app = FastAPI(title="Project Mayhem Token Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY", "devkey")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET", "secret")
LIVEKIT_URL = os.getenv("LIVEKIT_URL", "ws://localhost:7880")


@app.get("/token")
async def get_token(
    room: str = Query(default="project-mayhem-room"),
    identity: str = Query(default="user"),
    name: str = Query(default="User"),
):
    """Issue a LiveKit access token for the given room and identity."""
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

    return {
        "token": token.to_jwt(),
        "url": LIVEKIT_URL,
        "room": room,
    }


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
