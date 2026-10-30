# Phase 1: MVP – Real-time Talking Avatar

**Status**: Active · Week 4  
**Last Updated**: 2026-10-30  
**Latency goal**: < 1.2 s end-to-end (not yet measured under load)

## Goal
Usable real-time talking avatar that hears the user, speaks back, and shows a video presence.

## Success criteria
- [x] Camera + microphone work in browser
- [x] Join LiveKit room via token server
- [x] Agent speaks (TTS into room)
- [x] Chat text + Mic (browser STT) → reply
- [x] Placeholder video track (still face on CPU)
- [ ] Real lip-sync from reference image (needs GPU)
- [ ] Learned / Silero VAD interruption
- [ ] Measured e2e latency < 1.2 s

## Stack in use
- LiveKit Cloud + Render API + Vercel web
- TTS: Gnani Timbre (preferred) / edge-tts (fallback)
- Replies: rule-based English + Hinglish (`replies.py`)
- Video: Pillow still-face publish (no GPU)

## Week-by-week

### Week 1 — Media loop · Done
LiveKit room, token, camera in browser.

### Week 2 — Speech · Done
`/speak` publishes TTS audio into the room.

### Week 3 — Video placeholder · Done
Still face video track on free Render (avatar unreliable without GPU).

### Week 4 — Chat + Mic + Gnani · Done (key pending)
- `/chat` + frontend chips + Mic language
- Gnani Timbre integration; falls back to edge if key missing
- Contest notes: `docs/gnani-contest.md`

### Week 5+ — Next
1. Confirm Timbre live (`has_gnani_key`)
2. Optional Prisma STT
3. AWS GPU for MuseTalk / EchoMimic
4. Silero VAD + barge-in

## Deploy map
| Piece | Where |
|-------|--------|
| Web | Vercel, root `apps/web` |
| API | Render, root `apps/server`, entry `speak_agent.py` |
| Code | GitHub `Aryan418-dev/project-mayhem` |
