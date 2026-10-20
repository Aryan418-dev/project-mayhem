# Project Mayhem Architecture

## High-Level Design
Project Mayhem follows a Griffin-inspired architecture with two concurrent engines, implemented modularly in early phases.

```
User (Browser)
  Camera + Mic
       ↕ WebRTC (LiveKit / Pipecat)
Server
  ├── Orchestration Layer
  ├── Continuous Perception (Vision + Audio features)
  ├── Conversational Control Engine (decisions at high frequency)
  ├── Streaming Speech Generation + Voice Cloning
  └── Streaming Video Generation (conditioned on audio + controls + reference image)
       ↕
  Combined A/V stream back to user
```

## Core Components

### 1. Orchestration Layer
- Handles WebRTC sessions, media tracks, state
- Recommended: LiveKit or Pipecat
- Responsibilities: routing, latency monitoring, session management

### 2. Continuous Perception
- Ingests user audio and video continuously
- Extracts features (VAD, basic face/pose, later richer multimodal embeddings)
- Runs at high frequency (every 100–200 ms)

### 3. Conversational Control Engine
- Makes decisions at sub-second intervals
- Outputs:
  - Whether to speak / wait / interrupt / backchannel
  - What to say (or triggers LLM)
  - Emotion, gaze, gesture, head-pose control signals
- Phase 1: Rule-based (VAD + silence timers)
- Later phases: Learned model

### 4. Streaming Speech Generation
- Voice cloning from short reference audio (~10s)
- Streaming / chunked output
- Conditioned on control signals when available

### 5. Streaming Video Generation
- Input: single reference image + streaming audio + control signals
- Output: real-time video frames (lip-sync + head/upper-body motion)
- Phase 1 primary: MuseTalk + EchoMimic hybrid
- Goal: Move toward full-scene consistency over time

## Data Flow (Phase 1 Simplified)
1. User audio → VAD + feature extraction
2. Control logic decides when to respond
3. Text response → Streaming TTS (cloned voice)
4. Generated audio → Video model (conditioned on reference image)
5. Video frames + audio → LiveKit tracks → User

## Latency Targets
- Phase 1 MVP: < 1.2 s end-to-end
- Later phases: < 0.5–0.8 s

## Design Principles
- Full-duplex from the start (system can listen while speaking)
- Control signals drive both speech style and video behavior
- Modular first, unify later
- Measure everything related to latency and naturalness

## Evolution Path
- Phase 1: Modular pipeline with rule-based control
- Phase 2+: Richer continuous control model
- Phase 3+: Distilled / optimized generators + better scene consistency
- Phase 4: Tighter joint modeling
