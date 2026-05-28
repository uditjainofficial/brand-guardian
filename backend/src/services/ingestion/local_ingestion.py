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

        """
        Reuse existing stable YouTube downloader.
        """
        self.video_downloader = VideoIndexerService()

        """
        Local AI inference engines.
        """
        self.transcriber = WhisperTranscriber()

        self.frame_extractor = FrameExtractor()

        self.ocr_engine = OCREngine()

    def process_video(
        self,
        video_url: str,
        video_id: str
    ) -> Dict[str, Any]:
        """
        Execute local ingestion workflow.
        """

        logger.info(
            f"[Local Ingestion] Processing: {video_url}"
        )

        local_video_path = "temp_audit_video.mp4"

        frame_dir = "temp_frames"

        try:

            # =================================================
            # STEP 1 — DOWNLOAD VIDEO
            # =================================================

            if (
                "youtube.com" in video_url
                or "youtu.be" in video_url
            ):

                local_path = (
                    self.video_downloader
                    .download_youtube_video(
                        video_url,
                        output_path=local_video_path
                    )
                )

            else:
                raise Exception(
                    "Only YouTube URLs are supported."
                )

            # =================================================
            # STEP 2 — TRANSCRIPTION
            # =================================================

            transcript = self.transcriber.transcribe(
                local_path
            )

            # =================================================
            # STEP 3 — FRAME EXTRACTION
            # =================================================

            frame_paths = (
                self.frame_extractor.extract_frames(
                    local_path,
                    output_dir=frame_dir,
                    frame_interval=90
                )
            )

            # =================================================
            # STEP 4 — OCR PROCESSING
            # =================================================

            ocr_text = self.ocr_engine.extract_text(
                frame_paths
            )

            # =================================================
            # STEP 5 — CLEANUP
            # =================================================

            if os.path.exists(local_path):
                os.remove(local_path)

            if os.path.exists(frame_dir):
                shutil.rmtree(frame_dir)

            # =================================================
            # STEP 6 — NORMALIZED OUTPUT
            # =================================================

            logger.info(
                "[Local Ingestion] Complete"
            )

            return {
                "transcript": transcript,

                "ocr_text": ocr_text,

                "video_metadata": {
                    "platform": "youtube",
                    "ingestion_mode": "local"
                }
            }

        except Exception as e:

            logger.error(
                f"Local Ingestion Failed: {e}"
            )

            """
            Prevent temp artifact accumulation.
            """
            if os.path.exists(local_video_path):
                os.remove(local_video_path)

            if os.path.exists(frame_dir):
                shutil.rmtree(
                    frame_dir,
                    ignore_errors=True
                )

            return {
                "errors": [str(e)],
                "final_status": "FAIL",
                "transcript": "",
                "ocr_text": [],
                "video_metadata": {}
            }