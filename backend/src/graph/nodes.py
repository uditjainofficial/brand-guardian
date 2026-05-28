import os
import logging
from typing import Dict, Any, List

from backend.src.services.retrieval.azure_retrieval import (
    AzureRetrievalService
)
from backend.src.services.llm.azure_llm import (
    AzureLLMService
)
# Import the State schema
from backend.src.graph.state import VideoAuditState, ComplianceIssue

# NEW: Import ingestion abstraction layer
from backend.src.services.ingestion.azure_ingestion import AzureIngestionService

# Configure Logger
logger = logging.getLogger("brand-guardian")
logging.basicConfig(level=logging.INFO)


# =========================================================
# NODE 1 — VIDEO INGESTION
# =========================================================
def index_video_node(state: VideoAuditState) -> Dict[str, Any]:
    """
    Executes the video ingestion pipeline.

    Current Provider:
    - Azure Video Indexer

    Future Providers:
    - Whisper + OCR
    - Local multimodal ingestion
    """

    video_url = state.get("video_url")
    video_id_input = state.get("video_id", "vid_demo")

    logger.info(f"--- [Node: Indexer] Processing: {video_url} ---")

    try:
        # NEW: Node now depends on abstraction layer
        ingestion_service = AzureIngestionService()

        clean_data = ingestion_service.process_video(
            video_url=video_url,
            video_id=video_id_input
        )

        logger.info("--- [Node: Indexer] Extraction Complete ---")

        return clean_data

    except Exception as e:
        logger.error(f"Video Ingestion Failed: {e}")

        return {
            "errors": [str(e)],
            "final_status": "FAIL",
            "transcript": "",
            "ocr_text": [],
            "video_metadata": {}
        }


# =========================================================
# NODE 2 — COMPLIANCE AUDITOR
# =========================================================
def audit_content_node(state: VideoAuditState) -> Dict[str, Any]:
    """
    Performs Retrieval-Augmented Generation (RAG)
    to audit video content against compliance policies.
    """

    logger.info("--- [Node: Auditor] querying Knowledge Base & LLM ---")

    transcript = state.get("transcript", "")

    if not transcript:
        logger.warning("No transcript available. Skipping Audit.")

        return {
            "final_status": "FAIL",
            "final_report": "Audit skipped because video processing failed (No Transcript)."
        }

    # =====================================================
    # LLM INITIALIZATION
    # =====================================================
    llm = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"),
        openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        temperature=0.0
    )

    """
    Initialize retrieval provider.

    IMPORTANT:
    The Auditor Node no longer directly depends on:
    - AzureSearch
    - embeddings
    - vector database infrastructure

    It now depends on an abstract retrieval service.
    """

    retrieval_service = AzureRetrievalService()

    # =====================================================
    # RAG RETRIEVAL
    # =====================================================

    """
    Combine:
    - transcript
    - OCR text

    into a unified semantic retrieval query.
    """
    ocr_text = state.get("ocr_text", [])

    query_text = f"{transcript} {' '.join(ocr_text)}"

    """
    Retrieve the most relevant policy chunks.

    Future retrieval providers may include:
    - Qdrant
    - FAISS
    - Hybrid Retrieval
    - BM25 + Vector Search
    """
    retrieved_docs = retrieval_service.retrieve_rules(
        query=query_text,
        k=3
    )

    """
    Merge retrieved rules into prompt context.
    """
    retrieved_rules = "\n\n".join(
        retrieved_docs
    )






    """
    Initialize LLM provider.

    IMPORTANT:
    The Auditor Node no longer directly depends on:
    - AzureChatOpenAI
    - prompt execution
    - JSON parsing
    - response formatting

    It now depends on an abstract LLM service.
    """

    llm_service = AzureLLMService()

    """
    Execute compliance reasoning workflow.

    The provider is responsible for:
    - prompt construction
    - reasoning execution
    - structured parsing
    - normalization
    """
    return llm_service.audit_content(
        transcript=transcript,
        ocr_text=ocr_text,
        video_metadata=state.get(
            "video_metadata",
            {}
        ),
        retrieved_rules=retrieved_rules
    )