# Project Mayhem

Real-time video interaction agent (LiveKit + TTS + chat).
Inspired by Tavus Griffin. Built to stay simple so a human developer can own it.

## Live

| Piece | URL |
|-------|-----|
| Web | https://mayhemm.vercel.app |
| API health | https://project-mayhem-ulmi.onrender.com/health |
| Code | https://github.com/Aryan418-dev/project-mayhem |

## What runs today (Phase 1 · Week 4)

- Join a LiveKit room from the browser
- Type or Mic → agent replies and **speaks** (Gnani Timbre or edge-tts)
- Optional still-face video track (no GPU lip-sync yet)

## Repo layout (keep it this simple)

```
apps/
  server/           # ONE Python service
    speak_agent.py  # entrypoint: /health /token /speak /chat /voices
    tts.py          # Gnani Timbre + edge-tts fallback
    replies.py      # rule-based English / Hinglish replies
    requirements.txt
    .env.example
  web/              # Next.js frontend
    app/page.tsx    # Join room, chat, Mic, demo chips
docs/
  phase-1-mvp.md
  gnani-contest.md
AGENTS.md           # instructions for AI agents
```

**One server process:** `python speak_agent.py` (or uvicorn on Render).
Do not add parallel token servers or second TTS packages.

## Run locally

```bash
# Terminal 1 – LiveKit (optional if using LiveKit Cloud)
docker compose up livekit

# Terminal 2 – API
cd apps/server
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill LiveKit + optional GNANI_API_KEY
python speak_agent.py

# Terminal 3 – Web
cd apps/web && npm install && npm run dev
```

Open http://localhost:3000 → Join Room.

## Render env (production)

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

Start command should run `speak_agent.py` (root dir `apps/server`).

## Docs

- [AGENTS.md](AGENTS.md) – how agents should work on this repo
- [docs/phase-1-mvp.md](docs/phase-1-mvp.md) – phase checklist
- [docs/gnani-contest.md](docs/gnani-contest.md) – internship demo notes
- [ARCHITECTURE.md](ARCHITECTURE.md) · [ROADMAP.md](ROADMAP.md) · [CONVENTIONS.md](CONVENTIONS.md)

## License

TBD
