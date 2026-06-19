from __future__ import annotations


class SpeechError(Exception):
    """Base class for speech module errors."""


class TTSError(SpeechError):
    """Raised when TTS synthesis fails."""


class STTError(SpeechError):
    """Raised when STT transcription fails."""


class PlaybackError(SpeechError):
    """Raised when audio playback fails."""


class VoiceInputError(SpeechError):
    """Raised when voice input cannot be processed."""
