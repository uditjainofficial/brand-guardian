"""
OCR Processing Engine

PURPOSE:
Extract on-screen text from video frames.

WHY THIS EXISTS:
Azure Video Indexer previously handled OCR automatically.

Now:
we perform OCR locally using:
- RapidOCR
- ONNX Runtime

ARCHITECTURE BENEFITS:
- local inference
- provider independence
- reusable OCR pipeline
- controllable preprocessing

PERFORMANCE:
The OCR engine is loaded once and reused
across all requests.
"""

import logging

from typing import List

from rapidocr_onnxruntime import RapidOCR


logger = logging.getLogger("ocr-engine")


"""
Global singleton OCR instance.

This prevents ONNX models from being
reloaded on every audit request.
"""
_ocr_engine = None


def get_ocr_engine():
    """
    Load OCR engine once.

    Subsequent calls reuse the same instance.
    """

    global _ocr_engine

    if _ocr_engine is None:

        logger.info(
            "[OCR] Initializing RapidOCR engine..."
        )

        _ocr_engine = RapidOCR()

        logger.info(
            "[OCR] OCR engine ready"
        )

    return _ocr_engine


class OCREngine:
    """
    Local OCR engine for extracting text from frames.
    """

    def __init__(self):
        """
        Reuse existing OCR instance.
        """

        self.ocr = get_ocr_engine()

    def extract_text(
        self,
        frame_paths: List[str]
    ) -> List[str]:
        """
        Run OCR across extracted frames.

        FLOW:
        frame image
            ↓
        OCR inference
            ↓
        extracted text
            ↓
        normalized OCR results
        """

        logger.info(
            f"[OCR] Processing {len(frame_paths)} frames"
        )

        detected_text = []

        for frame_path in frame_paths:

            try:

                result, _ = self.ocr(
                    frame_path
                )

                if result:

                    for item in result:

                        text = item[1]

                        if text.strip():

                            detected_text.append(
                                text.strip()
                            )

            except Exception as e:

                logger.warning(
                    f"[OCR] Failed on "
                    f"{frame_path}: {e}"
                )

        logger.info(
            f"[OCR] Extracted "
            f"{len(detected_text)} text segments"
        )

        return detected_text