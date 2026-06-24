"""
Local Whisper Transcription Service

PURPOSE:
Provides local speech-to-text transcription using Faster-Whisper.

WHY THIS EXISTS:
Replaces Azure Video Indexer transcription functionality
with local inference.

ARCHITECTURE BENEFITS:
- zero cloud transcription cost
- provider independence
- local execution
- CPU-friendly inference
- modular ingestion pipeline

PERFORMANCE:
The Whisper model is loaded once and reused
across all requests using a singleton pattern.
"""

import logging

from faster_whisper import WhisperModel


logger = logging.getLogger("whisper-transcriber")


"""
Global singleton model instance.

This prevents the model from being loaded
on every audit request.
"""
_whisper_model = None


def get_whisper_model():
    """
    Load Whisper model once.

    Subsequent calls return the same instance.
    """

    global _whisper_model

    if _whisper_model is None:

        logger.info("[Whisper] BEFORE MODEL LOAD")

        _whisper_model = WhisperModel(
            model_size_or_path="tiny",
            device="cpu",
            compute_type="int8"
        )

        logger.info("[Whisper] AFTER MODEL LOAD")
    return _whisper_model


class WhisperTranscriber:
    """
    Local Faster-Whisper transcription engine.
    """

    def __init__(self):
        """
        Reuse existing model instance.
        """

        self.model = get_whisper_model()

    def transcribe(
        self,
        video_path: str
    ) -> str:
        """
        Transcribe video/audio into text.

        FLOW:
        video file
            ↓
        Faster-Whisper inference
            ↓
        segmented transcription
            ↓
        normalized transcript
        """

        logger.info(
            f"[Whisper] Transcribing: {video_path}"
        )

        segments, info = self.model.transcribe(
            video_path,
            beam_size=5
        )

        logger.info(
            f"[Whisper] Detected language: "
            f"{info.language}"
        )

        transcript_parts = []

        for segment in segments:
            transcript_parts.append(
                segment.text.strip()
            )

        final_transcript = " ".join(
            transcript_parts
        )

        logger.info(
            "[Whisper] Transcription complete"
        )

        return final_transcript