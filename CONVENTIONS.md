# Project Mayhem Conventions & Tech Stack

## Language & Runtime
- Backend: Python 3.11+
- Frontend: TypeScript / Next.js (App Router preferred)
- Package management: uv or poetry for Python; pnpm for JS

## Code Style
- Python: Ruff + Black (or Ruff format)
- TypeScript: ESLint + Prettier
- Prefer explicit types
- Keep functions focused and testable
- Comment non-obvious latency or concurrency decisions

## Repository Structure
```
project-mayhem/
├── apps/
│   ├── web/                 # Next.js frontend
│   └── server/              # Main Python backend / agent
├── packages/
│   ├── media/               # LiveKit / WebRTC helpers
│   ├── speech/              # TTS + cloning wrappers
│   ├── video/               # MuseTalk / EchoMimic / future models
│   ├── perception/          # VAD, vision features
│   └── control/             # Turn-taking and decision logic
├── models/                  # Local model weights (git-ignored)
├── scripts/                 # Setup, download, eval scripts
├── docs/                    # Phase plans and detailed docs
├── AGENTS.md
├── ARCHITECTURE.md
├── ROADMAP.md
├── CONVENTIONS.md
└── README.md
```

## Model Preferences (Phase 1)
- **Media**: LiveKit (first choice) or Pipecat
- **VAD**: Silero VAD
- **TTS + Voice Clone**: fish-speech or CosyVoice
- **Video**: MuseTalk (lip-sync primary) + EchoMimic V3-Flash
- Prefer models with existing streaming or low-latency paths

## Git & Collaboration
- Conventional commits preferred
- Feature branches for significant work
- Update relevant markdown when architecture or plan changes
- Never commit large model weights or secrets

## Latency Discipline
- Every new component must report its contribution to end-to-end latency
- Prefer streaming / chunked APIs over full-utterance generation
- Profile early

## Testing
- Unit tests for control logic and utilities
- Integration tests for media pipeline where feasible
- Manual human evaluation for naturalness (record short clips)

## Documentation Rules for Agents
- When changing the plan or architecture, update the corresponding `.md` file
- Add major decisions to the Decision Log in `AGENTS.md`
- Keep `docs/phase-1-mvp.md` as the living task list for current work
