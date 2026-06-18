import logging

logger = logging.getLogger("brand-guardian-telemetry")


def setup_telemetry():
    """
    Telemetry bootstrap.

    Azure Monitor has been removed from the
    open-source deployment.

    LangSmith tracing remains active through
    environment variables and LangChain.
    """

    logger.info(
        "Telemetry initialized (LangSmith enabled)"
    )