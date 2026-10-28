# Gnani Great Indian AI Internship Challenge

**Deadline:** 10 Nov 2026, 11:59 PM IST  
**Project:** Project Mayhem (real-time video interaction agent)

## What we use from Gnani

| Model | Role in Mayhem |
|-------|----------------|
| **Timbre** (TTS) | Agent speaks replies into the LiveKit room |
| **Prisma** (STT) | Optional later — server-side speech-to-text |
| **Evon** | Optional later — better replies than rule-based |

## Env vars (Render)

```
TTS_BACKEND=gnani
GNANI_API_KEY=<your key from Gnani dashboard>
GNANI_VOICE=Kaveri
GNANI_LANGUAGE=en-IN
REPLY_LANGUAGE=auto
```

For Hindi/Hinglish demo:
```
GNANI_VOICE=Nalini
GNANI_LANGUAGE=hi-IN
REPLY_LANGUAGE=hi
```

Check: `GET /health` → `"tts":"gnani"` and `tts_debug.has_gnani_key: true`.

## Demo flow for submission video

1. Open https://mayhemm.vercel.app  
2. Join Room  
3. Type or Mic: **Namaste** → agent replies in Hinglish/Hindi if language set  
4. Type: **What is your name?** → spoken reply  
5. Mention Gnani Timbre in the voiceover  

## Submission checklist

- [ ] Register at https://www.gnani.ai/internship  
- [ ] Working app uses Gnani API (Timbre at minimum)  
- [ ] 60-second demo video  
- [ ] Post on LinkedIn and/or X with `#GreatIndianAIInternshipChallenge` and `#GnaniAI`  
- [ ] Nominate post links in final submit form  

## Award angles

- **Mixed Vibes** — Hinglish replies + Timbre  
- **Jugaad Genius** — real-time LiveKit avatar + Indic TTS  
- **Demo Day Drop** — short clean join → speak → hear loop  

## Honest status

- LiveKit room + chat + mic: working  
- Timbre: code ready; needs `GNANI_API_KEY` visible on Render  
- Real lip-sync video: still placeholder without GPU  
