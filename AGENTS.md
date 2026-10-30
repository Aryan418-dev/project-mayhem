# Agent Instructions for Project Mayhem

This file is the primary source of truth for any AI agent working on Project Mayhem.

## Project Context
- **Name**: Project Mayhem
- **Goal**: Griffin-like full-duplex real-time video-to-video Human Interaction Model
- **Current focus**: Phase 1 Week 4 — chat + Mic + TTS (Gnani Timbre preferred, edge-tts fallback)
- **Repo**: https://github.com/Aryan418-dev/project-mayhem
- **Live web**: https://mayhemm.vercel.app
- **Live API**: https://project-mayhem-ulmi.onrender.com

## Coding rule (required)
Write **simple, human-readable code** only. Clear names, short functions, comments only when needed. A hired developer must own this without reverse-engineering AI patterns.

## Tool priority for agents
1. **GitHub** (native `github___*` tools) — source of truth for all code and docs
2. **mcpgram** — only if GitHub tools fail and mcpgram has a working GitHub/server connection
3. **Composio** — fallback for Vercel / Render deploy and env when those tools are available
4. Public HTTP (`/health`, site URL) — always OK for verification

If Render/Vercel tools are missing in the session, push to GitHub and ask the user to redeploy from the dashboard.

## Core principles
1. Modular, working pipelines over premature unification
2. Latency and natural turn-taking are first-class
3. Start simple (rule-based replies); replace with LLM later
4. Document major decisions in this file or phase docs
5. No large model weights in git

## Phase 1 stack
- Media: LiveKit
- TTS: Gnani Timbre (`GNANI_API_KEY`) with edge-tts fallback
- Video: still-face placeholder on free Render; MuseTalk/EchoMimic needs GPU later
- VAD: browser STT for now; Silero later on GPU host
- Frontend: Next.js + LiveKit React
- Backend: Python FastAPI (`apps/server/speak_agent.py`)

## Decision log
- 2026-10-20: Started as ProjectX → renamed Project Mayhem
- 2026-10-20: LiveKit preferred for media layer
- 2026-10-21: Human-readable code rule locked in
- 2026-10-21: Deployed Vercel (web) + Render (API)
- 2026-10-28: Gnani Timbre path for internship contest; edge-tts fallback
- 2026-10-28: Hinglish/Hindi rule-based replies + contest doc
- 2026-10-29: Frontend demo chips + mic language selector
- 2026-10-30: Docs refreshed to Week 4 live status

## Week status (Phase 1)
| Week | Goal | Status |
|------|------|--------|
| 1 | Media loop LiveKit | Done (cloud) |
| 2 | Speech / TTS into room | Done (edge + Gnani path) |
| 3 | Video track placeholder | Done (CPU face; no real lip-sync) |
| 4 | Chat + Mic + contest UX | Done (needs GNANI_API_KEY for Timbre) |
| 5+ | VAD interruption, GPU lip-sync | Next |

## How agents should work
1. Read this file and `docs/gnani-contest.md` before large changes
2. Push code with GitHub tools; small commits
3. Prefer editing `speak_agent.py`, `tts.py`, `replies.py`, `apps/web/app/page.tsx`
4. Never paste secrets into chat or commit them
5. After deploy, verify `GET /health`

## Next immediate actions
1. Confirm Render has `GNANI_API_KEY` → health `tts: gnani`
2. Optional: Hindi demo env (`GNANI_VOICE=Nalini`, `GNANI_LANGUAGE=hi-IN`, `REPLY_LANGUAGE=hi`)
3. Next code: server-side STT (Prisma) or GPU MuseTalk path on AWS
