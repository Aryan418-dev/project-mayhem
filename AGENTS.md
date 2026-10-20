# Agent Instructions for Project Mayhem

This file is the primary source of truth for any AI agent (Grok, Claude, Cursor, Codex, etc.) working on Project Mayhem.

## Project Context
- **Name**: Project Mayhem
- **Goal**: Build a Griffin-like full-duplex real-time video-to-video Human Interaction Model
- **Current Focus**: Phase 1 – MVP Real-time Talking Avatar
- **Key Inspiration**: Tavus Griffin architecture (Continuous Conversational Modeling + Streaming Speech + Streaming Video)

## Core Principles
1. Prefer modular, working pipelines over premature unification.
2. Latency and natural conversational timing are first-class concerns.
3. Start simple (rule-based turn-taking) and replace with learned models later.
4. Document every major decision in this file or in the relevant phase doc.
5. Keep the monorepo clean. Put temporary scripts in `/tmp` if needed; final code under `apps/` and `packages/`.

## Current Phase Priority (Phase 1)
Follow the detailed plan in `docs/phase-1-mvp.md`.

Order of work:
1. Media loop (LiveKit or Pipecat) – camera/mic ↔ server
2. Streaming TTS + voice cloning
3. Real-time video generation (MuseTalk / EchoMimic primary)
4. Continuous VAD + basic rule-based control
5. Polish latency and sync

## Recommended Stack (Phase 1)
- **Media**: LiveKit (preferred for speed) or Pipecat
- **TTS + Clone**: fish-speech or CosyVoice
- **Video**: MuseTalk (lip-sync) + EchoMimic V3-Flash (motion)
- **VAD**: Silero VAD
- **Backend**: Python 3.11+
- **Frontend**: Next.js + LiveKit client
- **GPU**: At least one modern NVIDIA GPU (4090 / A6000 class minimum for comfortable development)

## Decision Log
- 2026-10-20: Project originally named ProjectX. Starting with Phase 1 MVP.
- 2026-10-20: Architecture follows two-engine pattern (Continuous Conversational Modeling + Audio-Visual Generation) but implemented modularly at first.
- 2026-10-20: Prefer LiveKit for initial media layer.
- 2026-10-20: Scaffolded monorepo (apps/web, apps/server, packages/*, docker-compose, token server, agent skeleton, Next.js frontend). Week 1 media loop scaffolding complete.
- 2026-10-20: Project renamed from ProjectX to **Project Mayhem**. Folder is now `project-mayhem`.

## How Agents Should Work
1. Always read `README.md`, `AGENTS.md`, and the current phase doc before making changes.
2. When implementing a feature, update the relevant markdown if the plan changes.
3. Prefer small, testable increments.
4. Measure latency early and often.
5. When stuck on model choice, prefer the options listed in `docs/phase-1-mvp.md` and `CONVENTIONS.md`.
6. Record important new decisions in the Decision Log above.

## File Ownership
- Agents may freely edit code under `apps/` and `packages/`
- Update markdown documentation when architecture or plan changes
- Do not commit large model weights

## Next Immediate Action
User should run the 4-terminal local setup and verify:
1. Camera appears in the browser
2. Agent joins the room (check simple_agent.py logs)
3. Test tone is heard after ~3 seconds

After successful verification, next code task is user-audio echo (or start Week 2 speech pipeline).
