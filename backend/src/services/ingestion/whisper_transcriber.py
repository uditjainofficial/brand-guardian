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
"""

import logging

from faster_whisper import WhisperModel


logger = logging.getLogger("whisper-transcriber")


class WhisperTranscriber:
    """
    Local Faster-Whisper transcription engine.
    """

    def __init__(self):
        """
        Initialize Whisper model.

        MODEL CHOICE:
        - 'base' gives good balance between:
            accuracy
            speed
            memory usage

        CPU EXECUTION:
        - compute_type='int8'
        reduces memory usage significantly.
        """

        logger.info(
            "[Whisper] Loading Faster-Whisper model..."
        )

        self.model = WhisperModel(
            model_size_or_path="base",

            device="cpu",

            compute_type="int8"
        )

        logger.info(
            "[Whisper] Model loaded successfully"
        )

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