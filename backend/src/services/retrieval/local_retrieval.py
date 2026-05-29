"""
Local Retrieval Provider

PURPOSE:
Provides local Retrieval-Augmented Generation (RAG)
using:

- Local Embeddings
- Qdrant

This replaces:

Azure OpenAI Embeddings
        +
Azure AI Search

with a fully local retrieval stack.

CONTRACT:

retrieve_rules(...)
        ↓
List[str]

This matches BaseRetrievalService and allows
LangGraph orchestration to remain unchanged.
"""

import logging

from typing import List

from backend.src.services.retrieval.base import (
    BaseRetrievalService
)

from backend.src.services.retrieval.local_embeddings import (
    LocalEmbeddingService
)

from backend.src.services.retrieval.qdrant_store import (
    QdrantStore
)


logger = logging.getLogger(
    "local-retrieval"
)


class LocalRetrievalService(
    BaseRetrievalService
):
    """
    Local Qdrant implementation of the
    retrieval contract.

    Flow:

    query
        ↓
    embedding
        ↓
    Qdrant search
        ↓
    policy chunks
    """

    def __init__(self):
        """
        Initialize local retrieval stack.
        """

        self.embeddings = (
            LocalEmbeddingService()
        )

        self.vector_store = (
            QdrantStore()
        )

    def retrieve_rules(
        self,
        query: str,
        k: int = 3
    ) -> List[str]:
        """
        Retrieve relevant policy chunks.

        Parameters:
            query:
                User content requiring
                compliance grounding.

            k:
                Number of chunks to retrieve.

        Returns:
            List[str]
        """

        logger.info(
            "[Local Retrieval] "
            "Running semantic search"
        )

        # =====================================
        # EMBED QUERY
        # =====================================

        query_vector = (
            self.embeddings.embed_query(
                query
            )
        )

        # =====================================
        # SEARCH QDRANT
        # =====================================

        results = (
            self.vector_store.search(
                query_vector=query_vector,
                limit=k
            )
        )

        # =====================================
        # NORMALIZE OUTPUT
        # =====================================

        documents = []

        for result in results:

            payload = (
                result.payload
                or {}
            )

            text = payload.get(
                "text"
            )

            if text:
                documents.append(
                    text
                )

        logger.info(
            f"[Local Retrieval] "
            f"Retrieved "
            f"{len(documents)} chunks"
        )

        return documents