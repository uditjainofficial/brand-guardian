from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseIngestionService(ABC):
    """
    Abstract base class for all video ingestion providers.

    Every ingestion provider must return data in the normalized
    VideoAuditState-compatible schema.
    """

    @abstractmethod
    def process_video(
        self,
        video_url: str,
        video_id: str
    ) -> Dict[str, Any]:
        """
        Process a video and return normalized ingestion output.

        Required return schema:
        {
            "transcript": str,
            "ocr_text": list[str],
            "video_metadata": dict
        }
        """
        pass