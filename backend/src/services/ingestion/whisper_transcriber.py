import logging


logger = logging.getLogger("whisper-transcriber")


class WhisperTranscriber:
    """
    Temporary debug implementation.

    PURPOSE:
    Bypass Faster-Whisper entirely to determine
    whether Whisper model loading is causing
    Render crashes.
    """

    def __init__(self):
        logger.info(
            "[Whisper Debug] Using mock transcript"
        )

    def transcribe(
        self,
        video_path: str
    ) -> str:
        """
        Return a fake transcript.

        This allows us to test the rest of the
        Brand Guardian pipeline without loading
        any Whisper model.
        """

        logger.info(
            f"[Whisper Debug] Skipping transcription for: "
            f"{video_path}"
        )

        return """
        This video is sponsored by BrandX.

        Use my affiliate link below.

        Guaranteed results in 30 days.

        Click the link in the description
        to purchase now.
        """