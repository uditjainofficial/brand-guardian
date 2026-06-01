"""
Startup Health Checks

PURPOSE:
Validate critical dependencies before
the application accepts audit requests.
"""

import os
from pathlib import Path

from backend.src.services.retrieval.qdrant_store import (
    QdrantStore
)


def run_health_checks():
    """
    Validate runtime requirements.
    Raises RuntimeError on failure.
    """

    # ============================================
    # GROQ KEY
    # ============================================

    if not os.getenv("GROQ_API_KEY"):
        raise RuntimeError(
            "GROQ_API_KEY is missing."
        )

    # ============================================
    # PDF DATA
    # ============================================

    data_dir = (
        Path(__file__)
        .resolve()
        .parents[2]
        / "data"
    )

    pdfs = list(
        data_dir.glob("*.pdf")
    )

    if not pdfs:
        raise RuntimeError(
            "No policy PDFs found in backend/data."
        )

    # ============================================
    # QDRANT DATABASE
    # ============================================

    store = QdrantStore()

    collections = (
        store.client
        .get_collections()
    )

    names = [
        c.name
        for c in collections.collections
    ]

    if (
        store.COLLECTION_NAME
        not in names
    ):
        raise RuntimeError(
            "Qdrant collection "
            "'compliance_rules' not found."
        )

    print(
        "✅ Startup Health Checks Passed"
    )