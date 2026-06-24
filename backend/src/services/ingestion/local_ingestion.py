"""
Local Multimodal Ingestion Service

PURPOSE:
Completely local replacement for Azure Video Indexer.

PIPELINE:
YouTube URL
    ↓
Video Download
    ↓
Whisper Transcription
    ↓
Frame Extraction
    ↓
OCR Processing
    ↓
Normalized Output

ARCHITECTURE BENEFITS:
- zero Azure dependency
- local multimodal processing
- reusable ingestion pipeline
- provider independence
"""

import logging
import os
import shutil

from typing import Dict, Any

from backend.src.services.ingestion.base import (
    BaseIngestionService
)

from backend.src.services.video_indexer import (
    VideoIndexerService
)

from backend.src.services.ingestion.whisper_transcriber import (
    WhisperTranscriber
)

from backend.src.services.ingestion.frame_extractor import (
    FrameExtractor
)

from backend.src.services.ingestion.ocr_engine import (
    OCREngine
)


logger = logging.getLogger("local-ingestion")


class LocalIngestionService(BaseIngestionService):
    """
    Local multimodal ingestion provider.
    """

    def __init__(self):
        """
        Initialize ingestion components.
        """

        # Reuse existing stable YouTube downloader.
        self.video_downloader = VideoIndexerService()

        # Local AI inference engines.
        self.transcriber = WhisperTranscriber()

        self.frame_extractor = FrameExtractor()

        self.ocr_engine = OCREngine()

    def process_video(
        self,
        video_url: str,
        video_id: str
    ) -> Dict[str, Any]:
        """
        TEMPORARY DEBUG VERSION

        Bypasses:
        - YouTube download
        - Whisper
        - Frame extraction
        - OCR

        Goal:
        Verify Retrieval + Qdrant + Groq
        work correctly on Render.
        """

        logger.info(
            f"[Local Ingestion] MOCK MODE: {video_url}"
        )

        return {
            "transcript": """
            This video is sponsored by BrandX.

            Use my affiliate link below.

            Guaranteed results in 30 days.

            Click the link in the description
            to purchase now.
            """,

            "ocr_text": [
                "Sponsored",
                "Affiliate Link",
                "Guaranteed Results",
                "Limited Time Offer"
            ],

            "video_metadata": {
                "platform": "youtube",
                "ingestion_mode": "mock"
            }
        }