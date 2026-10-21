"""Speech package – TTS and voice cloning interfaces."""

from .tts import synthesize_to_wav_bytes, list_voices

__all__ = ["synthesize_to_wav_bytes", "list_voices"]
