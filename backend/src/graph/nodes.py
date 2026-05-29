import os
import logging

from typing import Dict, Any

from backend.src.services.retrieval.local_retrieval import (
    LocalRetrievalService
)

# =========================================================
# STATE SCHEMA
# =========================================================
from backend.src.graph.state import (
    VideoAuditState,
    ComplianceIssue
)

# =========================================================
# INGESTION PROVIDERS
# =========================================================
from backend.src.services.ingestion.azure_ingestion import (
    AzureIngestionService
)

from backend.src.services.ingestion.local_ingestion import (
    LocalIngestionService
)

# =========================================================
# RETRIEVAL PROVIDERS
# =========================================================
from backend.src.services.retrieval.azure_retrieval import (
    AzureRetrievalService
)

# =========================================================
# LLM PROVIDERS
# =========================================================
from backend.src.services.llm.azure_llm import (
    AzureLLMService
)

# =========================================================
# LOGGER CONFIGURATION
# =========================================================
logger = logging.getLogger("brand-guardian")

logging.basicConfig(level=logging.INFO)


# =========================================================
# NODE 1 — VIDEO INGESTION
# =========================================================
def index_video_node(
    state: VideoAuditState
) -> Dict[str, Any]:
    """
    Executes the video ingestion workflow.

    ARCHITECTURE:
    LangGraph orchestration node
        ↓
    Provider routing layer
        ↓
    Ingestion provider
        ↓
    Infrastructure implementation

    SUPPORTED PROVIDERS:
    - Azure Video Indexer
    - Local Whisper + OCR pipeline
    """

    video_url = state.get("video_url")

    video_id_input = state.get(
        "video_id",
        "vid_demo"
    )

    logger.info(
        f"--- [Node: Indexer] "
        f"Processing: {video_url} ---"
    )

    try:

        # =================================================
        # PROVIDER ROUTING
        # =================================================
        """
        Infrastructure provider selection.

        IMPORTANT:
        Orchestration logic should NOT directly
        hardcode infrastructure dependencies.

        Provider routing allows:
        - local execution
        - Azure execution
        - future GPU providers
        - future cloud providers

        WITHOUT changing orchestration.
        """

        ingestion_provider = os.getenv(
            "INGESTION_PROVIDER",
            "local"
        )

        # =============================================
        # LOCAL MULTIMODAL INGESTION
        # =============================================
        if ingestion_provider == "local":

            logger.info(
                "[Indexer] Using Local "
                "Ingestion Provider"
            )

            ingestion_service = (
                LocalIngestionService()
            )

        # =============================================
        # AZURE VIDEO INDEXER
        # =============================================
        elif ingestion_provider == "azure":

            logger.info(
                "[Indexer] Using Azure "
                "Ingestion Provider"
            )

            ingestion_service = (
                AzureIngestionService()
            )

        # =============================================
        # UNSUPPORTED PROVIDER
        # =============================================
        else:

            raise ValueError(
                f"Unsupported ingestion provider: "
                f"{ingestion_provider}"
            )

        # =================================================
        # EXECUTE INGESTION PIPELINE
        # =================================================
        clean_data = ingestion_service.process_video(
            video_url=video_url,
            video_id=video_id_input
        )

        logger.info(
            "--- [Node: Indexer] "
            "Extraction Complete ---"
        )

        return clean_data

    except Exception as e:

        logger.error(
            f"Video Ingestion Failed: {e}"
        )

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
def audit_content_node(
    state: VideoAuditState
) -> Dict[str, Any]:
    """
    Performs Retrieval-Augmented Generation (RAG)
    to audit video content against compliance rules.

    ARCHITECTURE:
    transcript + OCR
        ↓
    semantic retrieval
        ↓
    policy grounding
        ↓
    LLM reasoning
        ↓
    structured compliance output
    """

    logger.info(
        "--- [Node: Auditor] "
        "querying Knowledge Base & LLM ---"
    )

    transcript = state.get(
        "transcript",
        ""
    )

    # =====================================================
    # VALIDATE TRANSCRIPT EXISTS
    # =====================================================
    if not transcript:

        logger.warning(
            "No transcript available. "
            "Skipping Audit."
        )

        return {
            "final_status": "FAIL",

            "final_report":
            "Audit skipped because video "
            "processing failed (No Transcript)."
        }

    # =====================================================
    # RETRIEVAL PROVIDER
    # =====================================================
    """
    Initialize retrieval provider.

    IMPORTANT:
    The Auditor Node no longer directly depends on:
    - AzureSearch
    - embeddings
    - vector database infrastructure

    It now depends on an abstract retrieval service.
    """

    """
    Select retrieval provider.

    Supported Providers:

    azure:
        Azure AI Search
        + Azure Embeddings

    local:
        Qdrant
        + Sentence Transformers
    """

    retrieval_provider = os.getenv(
        "RETRIEVAL_PROVIDER",
        "local"
    ).lower()

    if retrieval_provider == "azure":

        logger.info(
            "[Retrieval] Using Azure Provider"
        )

        retrieval_service = (
            AzureRetrievalService()
        )

    else:

        logger.info(
            "[Retrieval] Using Local Provider"
        )

        retrieval_service = (
            LocalRetrievalService()
        )

    # =====================================================
    # BUILD RETRIEVAL QUERY
    # =====================================================
    """
    Combine:
    - transcript
    - OCR text

    into a unified semantic query.
    """

    ocr_text = state.get(
        "ocr_text",
        []
    )

    query_text = (
        f"{transcript} "
        f"{' '.join(ocr_text)}"
    )

    # =====================================================
    # RETRIEVE POLICY DOCUMENTS
    # =====================================================
    """
    Retrieve the most relevant policy chunks.

    FUTURE PROVIDERS:
    - Qdrant
    - FAISS
    - Hybrid Retrieval
    - BM25 + Vector Search
    """

    retrieved_docs = (
        retrieval_service.retrieve_rules(
            query=query_text,
            k=3
        )
    )

    # =====================================================
    # NORMALIZE RETRIEVED CONTEXT
    # =====================================================
    retrieved_rules = "\n\n".join(
        retrieved_docs
    )

    # =====================================================
    # LLM PROVIDER
    # =====================================================
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

    # =====================================================
    # EXECUTE COMPLIANCE REASONING
    # =====================================================
    """
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