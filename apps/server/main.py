"""
Project Mayhem Server - Phase 1 Week 1
Minimal LiveKit agent that joins a room and can receive/publish media tracks.
"""

import asyncio
import logging
import os
from dotenv import load_dotenv

from livekit import rtc, api
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant  # may evolve; keep simple for Week 1

load_dotenv()

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("project-mayhem-server")

LIVEKIT_URL = os.getenv("LIVEKIT_URL", "ws://localhost:7880")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY", "devkey")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET", "secret")
ROOM_NAME = os.getenv("ROOM_NAME", "project-mayhem-room")
AGENT_NAME = os.getenv("AGENT_NAME", "project-mayhem-agent")


async def entrypoint(ctx: JobContext):
    """Main entrypoint when the agent is dispatched to a room."""
    logger.info(f"Agent connecting to room: {ctx.room.name}")

    # Connect to the room, subscribe to all tracks for now
    await ctx.connect(auto_subscribe=AutoSubscribe.SUBSCRIBE_ALL)

    logger.info(f"Agent joined room: {ctx.room.name}")
    logger.info(f"Local participant: {ctx.room.local_participant.identity}")

    # Simple event handlers for Week 1 observability
    @ctx.room.on("participant_connected")
    def on_participant_connected(participant: rtc.RemoteParticipant):
        logger.info(f"Participant connected: {participant.identity}")

    @ctx.room.on("track_subscribed")
    def on_track_subscribed(
        track: rtc.Track,
        publication: rtc.RemoteTrackPublication,
        participant: rtc.RemoteParticipant,
    ):
        logger.info(
            f"Track subscribed: {track.kind} from {participant.identity} "
            f"(sid={publication.sid})"
        )

        if track.kind == rtc.TrackKind.KIND_AUDIO:
            logger.info("User audio track received — ready for VAD / processing in later weeks")

        if track.kind == rtc.TrackKind.KIND_VIDEO:
            logger.info("User video track received — ready for perception in later weeks")

    @ctx.room.on("track_unsubscribed")
    def on_track_unsubscribed(
        track: rtc.Track,
        publication: rtc.RemoteTrackPublication,
        participant: rtc.RemoteParticipant,
    ):
        logger.info(f"Track unsubscribed: {track.kind} from {participant.identity}")

    # Keep the agent alive
    # In later weeks we will add speech + video publishing here
    logger.info("Agent is running. Waiting for participants and tracks...")
    await asyncio.Future()  # run forever


if __name__ == "__main__":
    # For local development you can also connect manually.
    # The LiveKit Agents worker pattern is preferred going forward.
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            # For Week 1 we can run in "dev" mode against local LiveKit
        )
    )
