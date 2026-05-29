"""
Local Embedding Provider

PURPOSE:
Generate semantic embeddings locally using
Sentence Transformers.

WHY THIS EXISTS:
Replaces Azure OpenAI Embeddings.

ARCHITECTURE BENEFITS:
- zero API cost
- local execution
- provider independence
- reusable embedding layer
"""

import logging

from typing import List

from sentence_transformers import SentenceTransformer


logger = logging.getLogger("local-embeddings")


class LocalEmbeddingService:
    """
    Local embedding provider.

    Uses:
        all-MiniLM-L6-v2

    This model is:
    - lightweight
    - fast
    - widely used for RAG
    """

    def __init__(self):

        logger.info(
            "[Embeddings] Loading local model..."
        )

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        logger.info(
            "[Embeddings] Model ready"
        )

    def embed_query(
        self,
        text: str
    ) -> List[float]:
        """
        Generate embedding for a search query.
        """

        return self.model.encode(
            text,
            normalize_embeddings=True
        ).tolist()

    def embed_documents(
        self,
        texts: List[str]
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple chunks.
        """

        return self.model.encode(
            texts,
            normalize_embeddings=True
        ).tolist()