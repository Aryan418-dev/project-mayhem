# Project Mayhem

**Real-time full-duplex video-to-video Human Interaction Model**  
Inspired by Tavus Griffin. Goal: build a system that sees, hears, decides, speaks, and generates video concurrently with natural conversational timing.

## Current Status
- **Phase**: Phase 1 Week 1 (Foundation & Media Loop) — ready for local test
- **Target**: Usable real-time avatar with lip-sync, voice cloning, basic interruption handling, end-to-end latency < 1.2s
- **Last updated**: 2026-10-20

### Quick Start (local) — 4 terminals
```bash
# 1. LiveKit
docker compose up livekit

# 2. Token server
cd apps/server
python -m venv .venv && source .venv/bin/activate   # first time
pip install -r requirements.txt                     # first time
cp .env.example .env                                # first time
python token_server.py

# 3. Frontend
cd apps/web && npm install && npm run dev           # npm install first time only

# 4. Simple agent (plays a short test tone after ~3s)
cd apps/server && source .venv/bin/activate
python simple_agent.py
```
Open http://localhost:3000 → Join Room.  
You should see your camera and hear a short test beep from the agent.

## Quick Links
- [Architecture](ARCHITECTURE.md)
- [Roadmap](ROADMAP.md)
- [Phase 1 Detailed Plan](docs/phase-1-mvp.md)
- [Agent Instructions](AGENTS.md)
- [Tech Stack & Conventions](CONVENTIONS.md)

## High-Level Goal
Create a system where:
1. User joins via browser (camera + mic)
2. System continuously perceives audio + video
3. Makes sub-second conversational decisions (speak / wait / interrupt / backchannel)
4. Generates streaming speech (with voice cloning) + streaming video (from single reference image)
5. Everything runs full-duplex (listens while speaking)

## Success Levels
- **MVP (Phase 1)**: Natural real-time talking avatar with decent lip-sync and basic responsiveness
- **V1 (Phase 2–3)**: Strong interruption handling, emotion/gesture control, better naturalness
- **V2+**: Closer to Griffin quality (full-scene consistency, highly natural timing)

## Getting Started (for humans & agents)
1. Read `AGENTS.md` first
2. Read `docs/phase-1-mvp.md` for current work
3. Follow the Week 1 tasks in Phase 1

## License
TBD (likely Apache 2.0 or MIT once decided)
