# Phase 1: MVP – Real-time Talking Avatar

**Status**: Active · Week 5  
**Last Updated**: 2026-10-30

## Goal
Usable real-time talking avatar that hears the user, speaks back, and shows a video presence.

## Success criteria
- [x] Camera + microphone work in browser
- [x] Join LiveKit room via token server
- [x] Agent speaks (TTS into room)
- [x] Chat text + Mic (browser STT) → reply
- [x] Placeholder video track (still face on CPU)
- [x] Gnani Timbre TTS live
- [x] Gnani Prisma STT (`/transcribe`, `/voice-chat`)
- [ ] Real lip-sync from reference image (needs GPU)
- [ ] Silero VAD interruption
- [ ] Measured e2e latency < 1.2 s

## Stack
- LiveKit Cloud + Render API + Vercel web
- TTS: Gnani Timbre / edge-tts fallback
- STT: Gnani Prisma v3.0 REST (same API key)
- Replies: rule-based English + Hinglish
- Video: still-face on CPU

## API (speak_agent.py)
| Method | Path | Purpose |
|--------|------|--------|
| GET | /health | status, tts, stt |
| GET | /token | LiveKit join token |
| POST | /speak | text → speak in room |
| POST | /chat | message → reply → speak |
| POST | /transcribe | audio file → transcript |
| POST | /voice-chat | audio → STT → reply → speak |
| GET | /voices | Timbre voice list |

## Week status
1–4 Done · 5 Prisma STT added · Next: GPU lip-sync / VAD

## Deploy
| Piece | Where |
|-------|--------|
| Web | Vercel, `apps/web` |
| API | Render, `apps/server`, `speak_agent.py` |
| Code | GitHub `Aryan418-dev/project-mayhem` |
