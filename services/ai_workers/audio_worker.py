"""Audio Worker for Keyword Spotting (Salam, Paket, Darurat) and Acoustic Anomaly Detection."""

import os
import re
from typing import Any, Dict, List, Optional


class AudioWorker:
    """Modular audio analyzer with feature flag and keyword spotting."""

    GREETING_KEYWORDS = ["assalamualaikum", "permisi", "punteun", "halo", "selamat"]
    COURIER_KEYWORDS = ["paket", "ekspedisi", "kurir", "antar"]
    EMERGENCY_KEYWORDS = ["tolong", "maling", "kebakaran", "rampok", "bantu"]

    def __init__(self, enabled: Optional[bool] = None):
        """Initialize AudioWorker with environment variable or explicit flag.

        Args:
            enabled: If True, worker will process audio. If None, reads from ENABLE_AUDIO_MODULE.
        """
        if enabled is not None:
            self._enabled = enabled
        else:
            env_val = os.getenv("ENABLE_AUDIO_MODULE", "false").lower()
            self._enabled = env_val in ("true", "1", "yes")

    def is_enabled(self) -> bool:
        """Return True if audio processing is enabled."""
        return self._enabled

    def process_audio_sample(self, raw_audio_bytes: bytes) -> Dict[str, Any]:
        """Process incoming raw audio PCM bytes from camera stream.

        Args:
            raw_audio_bytes: Audio chunk bytes from RTSP sub-stream.

        Returns:
            Analysis result dictionary.
        """
        if not self._enabled:
            return {
                "status": "disabled",
                "detected_intent": None,
                "keyword": None,
            }

        # If audio is enabled, in production this forwards to Faster-Whisper tiny / YamNet
        return {
            "status": "processed",
            "detected_intent": None,
            "keyword": None,
        }

    def process_transcript(self, transcript_text: str) -> Dict[str, Any]:
        """Analyze transcription text for defined safety keywords.

        Args:
            transcript_text: Text string returned by local STT model.

        Returns:
            Keyword match dictionary.
        """
        if not self._enabled:
            return {
                "status": "disabled",
                "detected_intent": None,
                "keyword": None,
            }

        cleaned = transcript_text.lower()

        # Check emergency keywords first (highest priority)
        for kw in self.EMERGENCY_KEYWORDS:
            if re.search(rf"\b{kw}\b", cleaned):
                return {
                    "status": "detected",
                    "detected_intent": "emergency_alert",
                    "keyword": kw,
                    "confidence": 0.95,
                }

        # Check courier keywords
        for kw in self.COURIER_KEYWORDS:
            if re.search(rf"\b{kw}\b", cleaned):
                return {
                    "status": "detected",
                    "detected_intent": "courier_arrival",
                    "keyword": kw,
                    "confidence": 0.90,
                }

        # Check greeting keywords
        for kw in self.GREETING_KEYWORDS:
            if re.search(rf"\b{kw}\b", cleaned):
                return {
                    "status": "detected",
                    "detected_intent": "guest_greeting",
                    "keyword": kw,
                    "confidence": 0.90,
                }

        return {
            "status": "no_keyword_match",
            "detected_intent": None,
            "keyword": None,
        }
