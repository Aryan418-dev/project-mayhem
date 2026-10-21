# Week 3: Video Generation

**Goal**: Lip-synced talking video from a single reference image + audio, published as a LiveKit video track.

## Status
Scaffolding complete. Placeholder backend works without GPU (still image as video). MuseTalk path is stubbed for GPU hosts.

## Architecture

```
Text → TTS (Week 2) → PCM audio
                         ↓
              VideoBackend.frames_from_audio(pcm)
                         ↓
              JPEG/RGB frames @ 15–25 fps
                         ↓
              LiveKit LocalVideoTrack → room
```

## Backends

| Backend | GPU | Quality | When |
|---------|-----|---------|------|
| placeholder | No | Still image | Default on Render / free tier |
| musetalk | Yes | Real lip-sync | Local GPU or GPU cloud |

Env:
```bash
ENABLE_VIDEO=true
VIDEO_BACKEND=placeholder
REFERENCE_IMAGE_PATH=/path/to/face.jpg
```

## Local GPU setup (MuseTalk)

1. Machine with NVIDIA GPU (8GB+ VRAM recommended)
2. Install MuseTalk (follow upstream repo)
3. Download weights into `models/musetalk/`
4. Set `VIDEO_BACKEND=musetalk`
5. Wire inference in `packages/video/generator.py`

Primary model: **MuseTalk** (real-time lip-sync)
Optional motion: **EchoMimic V3-Flash**

## Exit criteria
Video track appears when system speaks (placeholder OK for pipeline; MuseTalk for quality).

## Constraint
Render free tier has **no GPU**. Production lip-sync needs a GPU host (local, RunPod, Vast, etc.).
