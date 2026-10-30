# Project Mayhem

**Real-time full-duplex video-to-video Human Interaction Model**  
Inspired by Tavus Griffin. Goal: build a system that sees, hears, decides, speaks, and generates video concurrently with natural conversational timing.

## Live demo
- **Frontend (Vercel):** https://mayhemm.vercel.app  
- **API (Render):** https://project-mayhem-ulmi.onrender.com/health  
- **GitHub:** https://github.com/Aryan418-dev/project-mayhem  

## Current Status (2026-10-30)
- **Phase**: Phase 1 · **Week 4** (Voice + Chat + Gnani Timbre path)
- **Working**: LiveKit room, Join, chat text, Mic (browser STT), spoken replies, placeholder face video
- **TTS**: edge-tts fallback; Gnani Timbre when `GNANI_API_KEY` is set on Render
- **Not yet**: real lip-sync GPU video, server-side Prisma STT, learned VAD interruption

### Cloud quick test
1. Open https://mayhemm.vercel.app → **Join Room**
2. Tap a demo chip (**Namaste**) or type a message → agent speaks a reply
3. Optional: Mic (Chrome/Edge), language en-IN / hi-IN

### Env on Render (service or linked group)
```
LIVEKIT_URL=
LIVEKIT_API_KEY=
LIVEKIT_API_SECRET=
TTS_BACKEND=gnani
GNANI_API_KEY=
GNANI_VOICE=Kaveri
GNANI_LANGUAGE=en-IN
REPLY_LANGUAGE=auto
```

Health should show `"tts":"gnani"` and `tts_debug.has_gnani_key: true` when the key is live.

### Local quick start (optional)
```bash
# 1. LiveKit
docker compose up livekit

# 2. Server
cd apps/server
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill LiveKit + optional GNANI_API_KEY
python speak_agent.py

# 3. Frontend
cd apps/web && npm install && npm run dev
```
Open http://localhost:3000 → Join Room.

## Quick Links
- [Agent Instructions](AGENTS.md)
- [Architecture](ARCHITECTURE.md)
- [Roadmap](ROADMAP.md)
- [Gnani contest notes](docs/gnani-contest.md)
- [Conventions](CONVENTIONS.md)

## High-Level Goal
1. User joins via browser (camera + mic)
2. System continuously perceives audio + video
3. Sub-second conversational decisions (speak / wait / interrupt)
4. Streaming speech + streaming video from a reference image
5. Full-duplex (listens while speaking)

## Success Levels
- **MVP (Phase 1)**: Natural real-time talking avatar with decent lip-sync and basic responsiveness
- **V1 (Phase 2–3)**: Strong interruption handling, emotion/gesture control
- **V2+**: Closer to Griffin quality

## License
TBD (likely Apache 2.0 or MIT once decided)
