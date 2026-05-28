"""
Video Frame Extraction Service

PURPOSE:
Extracts video frames for OCR analysis.

WHY THIS EXISTS:
Azure Video Indexer previously handled OCR internally.

Now:
we must manually:
- sample frames
- extract images
- pass frames into OCR pipeline

ARCHITECTURE BENEFITS:
- provider independence
- reusable OCR pipeline
- controllable frame sampling strategy
"""

import os
import cv2
import logging

from typing import List


logger = logging.getLogger("frame-extractor")


class FrameExtractor:
    """
    Extracts frames from videos at fixed intervals.
    """

    def extract_frames(
        self,
        video_path: str,
        output_dir: str = "temp_frames",
        frame_interval: int = 30
    ) -> List[str]:
        """
        Extract frames from a video.

        PARAMETERS:
        - frame_interval:
            Extract one frame every N frames.

        RETURNS:
        List[str]
            Paths to extracted frame images.
        """

        logger.info(
            f"[Frame Extractor] Processing: {video_path}"
        )

        """
        Create temp frame directory if missing.
        """
        os.makedirs(
            output_dir,
            exist_ok=True
        )

        capture = cv2.VideoCapture(video_path)

        frame_paths = []

        frame_count = 0
        saved_count = 0

        while True:

            success, frame = capture.read()

            if not success:
                break

            """
            Sample frames at intervals.

            This prevents:
            - excessive OCR cost
            - redundant frames
            - unnecessary processing
            """
            if frame_count % frame_interval == 0:

                frame_path = os.path.join(
                    output_dir,
                    f"frame_{saved_count}.jpg"
                )

                cv2.imwrite(
                    frame_path,
                    frame
                )

                frame_paths.append(
                    frame_path
                )

                saved_count += 1

            frame_count += 1

        capture.release()

        logger.info(
            f"[Frame Extractor] Extracted "
            f"{len(frame_paths)} frames"
        )

        return frame_paths