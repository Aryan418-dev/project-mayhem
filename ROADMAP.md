# Project Mayhem Roadmap

## Overview
Build a Griffin-inspired full-duplex real-time video-to-video Human Interaction Model in progressive phases.

## Phase 0: Foundation (Optional / Parallel)
- Basic repo structure
- Development environment
- Simple WebRTC media loop
**Status**: Can be folded into Phase 1 Week 1

## Phase 1: MVP – Real-time Talking Avatar (Current)
**Target Duration**: 6–10 weeks  
**Goal**: Usable real-time avatar with lip-sync, voice cloning, basic interruption handling. End-to-end latency < 1.2s.

### Key Deliverables
- Browser-based camera + mic
- Streaming TTS with voice cloning
- Real-time audio-driven video generation from single reference image
- Continuous VAD + rule-based turn-taking
- Basic interruption support
- Working continuous conversation loop

**Detailed plan**: See `docs/phase-1-mvp.md`

## Phase 2: Strong Conversational Control
**Target Duration**: 8–12 weeks  
**Goal**: Sub-second decision making for speak/wait/interrupt/backchannel + emotion/gesture control signals.

- Train or fine-tune continuous control model
- Feed rich control signals into speech and video generators
- Improve natural timing and nonverbal behavior
- Collect conversational data

## Phase 3: Quality & Latency Push
**Target Duration**: 10–16 weeks  
**Goal**: Significantly better quality and lower latency.

- Aggressive distillation and optimization of video model
- Better full-scene or upper-body consistency
- Memory / long-context support
- Systematic human evaluation

## Phase 4: Unification & Production
**Ongoing**
- Tighter end-to-end training
- Advanced techniques (distillation methods, Self-Forcing style, etc.)
- Multi-avatar, robustness, safety features
- Production hardening

## Success Metrics (Across Phases)
- End-to-end latency
- Lip-sync quality
- Interruption success rate
- Human preference / naturalness scores
- Ability to sustain multi-minute conversations without breaking

## Notes
- Always prefer working modular systems over incomplete unified ones.
- Latency budget is sacred.
- Document major architectural decisions in `AGENTS.md` Decision Log.
