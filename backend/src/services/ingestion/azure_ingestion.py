import logging
import os

from typing import Dict, Any

from backend.src.services.ingestion.base import BaseIngestionService
from backend.src.services.video_indexer import VideoIndexerService


logger = logging.getLogger("azure-ingestion")


class AzureIngestionService(BaseIngestionService):
    """
    Azure Video Indexer implementation of the ingestion contract.

    This adapter isolates Azure-specific ingestion logic from
    LangGraph orchestration nodes.
    """

    def __init__(self):
        self.video_indexer = VideoIndexerService()

    def process_video(
        self,
        video_url: str,
        video_id: str
    ) -> Dict[str, Any]:

        logger.info(f"[Azure Ingestion] Processing: {video_url}")

        local_filename = "temp_audit_video.mp4"

        try:
            # 1. DOWNLOAD VIDEO
            if "youtube.com" in video_url or "youtu.be" in video_url:
                local_path = self.video_indexer.download_youtube_video(
                    video_url,
                    output_path=local_filename
                )
            else:
                raise Exception("Only YouTube URLs are currently supported.")

            # 2. UPLOAD TO AZURE VIDEO INDEXER
            azure_video_id = self.video_indexer.upload_video(
                local_path,
                video_name=video_id
            )

            logger.info(f"Azure Upload Success: {azure_video_id}")

            # 3. CLEANUP LOCAL FILE
            if os.path.exists(local_path):
                os.remove(local_path)

            # 4. WAIT FOR PROCESSING
            raw_insights = self.video_indexer.wait_for_processing(
                azure_video_id
            )

            # 5. NORMALIZE OUTPUT
            clean_data = self.video_indexer.extract_data(raw_insights)

            logger.info("[Azure Ingestion] Extraction Complete")

            return clean_data

        except Exception as e:
            logger.error(f"Azure Ingestion Failed: {e}")

            return {
                "errors": [str(e)],
                "final_status": "FAIL",
                "transcript": "",
                "ocr_text": [],
                "video_metadata": {}
            }