# Agent instructions — Project Mayhem

## Goal
Griffin-like real-time video interaction agent. Prefer simple, human-readable code.

## Live
- Web: https://mayhemm.vercel.app
- API: https://project-mayhem-ulmi.onrender.com
- Repo: https://github.com/Aryan418-dev/project-mayhem

## Single source of truth for code
| Path | Role |
|------|------|
| `apps/server/speak_agent.py` | **Only** server entry (token, speak, chat, health) |
| `apps/server/tts.py` | TTS (Gnani + edge fallback) |
| `apps/server/replies.py` | Rule-based replies |
| `apps/web/app/page.tsx` | Frontend |

**Do not recreate** `main.py`, `token_server.py`, or `packages/speech/tts.py`. Those were removed as duplicates.

## Coding rules
1. Short functions, clear names, no clever abstractions
2. A hired developer must understand the code without reverse-engineering AI patterns
3. Never commit secrets
4. Push with GitHub tools first; Composio only if needed for deploy

## Tool priority
1. GitHub (`github___*`)
2. mcpgram only if GitHub fails and a server is linked
3. Composio for Vercel/Render when available
4. Public HTTP for health checks

## Phase status
| Week | Status |
|------|--------|
| 1 Media loop | Done |
| 2 TTS into room | Done |
| 3 Video placeholder | Done (CPU face) |
| 4 Chat + Mic + Gnani | Done |
| 5+ VAD / GPU lip-sync | Next |

## Decision log
- 2026-10-20: LiveKit media; renamed Project Mayhem
- 2026-10-21: Human-readable code rule; Vercel + Render deploy
- 2026-10-28: Gnani Timbre path + Hinglish replies
- 2026-10-30: Gnani live on Render; removed duplicate server/TTS files
