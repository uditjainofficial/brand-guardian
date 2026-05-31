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

PERFORMANCE:
The embedding model is loaded once and
reused across all requests.
"""

import logging

from typing import List

from sentence_transformers import (
    SentenceTransformer
)


logger = logging.getLogger(
    "local-embeddings"
)


"""
Global singleton embedding model.

This prevents loading the model
on every audit request.
"""
_embedding_model = None


def get_embedding_model():
    """
    Load embedding model once.

    Subsequent calls reuse the
    same model instance.
    """

    global _embedding_model

    if _embedding_model is None:

        logger.info(
            "[Embeddings] Loading local model..."
        )

        _embedding_model = (
            SentenceTransformer(
                "all-MiniLM-L6-v2"
            )
        )

        logger.info(
            "[Embeddings] Model ready"
        )

    return _embedding_model


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

        self.model = (
            get_embedding_model()
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