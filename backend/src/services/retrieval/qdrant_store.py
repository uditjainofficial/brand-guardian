"""
Qdrant Vector Store

PURPOSE:
Centralizes all Qdrant interactions.

WHY THIS EXISTS:
Both:
- indexing pipeline
- retrieval provider

need access to the same vector database.

Keeping Qdrant logic isolated prevents
database-specific code from leaking into
business logic.

ARCHITECTURE:

PDFs
 ↓
Indexing Script
 ↓
QdrantStore
 ↓
Qdrant Database

and

User Query
 ↓
Local Retrieval Provider
 ↓
QdrantStore
 ↓
Qdrant Database
"""

import logging

from pathlib import Path
from typing import List

from qdrant_client import QdrantClient

from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)


logger = logging.getLogger("qdrant-store")


class QdrantStore:
    """
    Wrapper around Qdrant operations.

    Responsibilities:
    - collection creation
    - vector insertion
    - semantic search

    This class hides all Qdrant-specific
    implementation details from the rest
    of the application.
    """

    COLLECTION_NAME = "compliance_rules"

    def __init__(self):
        """
        Initialize local persistent Qdrant database.

        IMPORTANT:
        Use an absolute project-root path instead of
        a relative path.

        This prevents issues when running:

        - FastAPI
        - scripts
        - tests

        from different working directories.

        Resulting location:

        ComplianceQAPipeline/
        └── qdrant_db/
        """

        project_root = (
            Path(__file__)
            .resolve()
            .parents[4]
        )

        qdrant_path = (
            project_root / "qdrant_db"
        )

        logger.info(
            f"[Qdrant] Database Path: "
            f"{qdrant_path}"
        )

        self.client = QdrantClient(
            path=str(qdrant_path)
        )

    def create_collection(
        self,
        vector_size: int
    ):
        """
        Create collection if it does not exist.

        Parameters:
            vector_size:
                Embedding dimension size.

        Example:
            all-MiniLM-L6-v2
            → 384 dimensions
        """

        collections = (
            self.client.get_collections()
        )

        existing_collections = [
            collection.name
            for collection in collections.collections
        ]

        if self.COLLECTION_NAME in existing_collections:

            logger.info(
                "[Qdrant] Collection already exists"
            )

            return

        logger.info(
            "[Qdrant] Creating collection..."
        )

        self.client.create_collection(
            collection_name=self.COLLECTION_NAME,

            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            )
        )

        logger.info(
            "[Qdrant] Collection created"
        )

    def upsert_points(
        self,
        points: List[PointStruct]
    ):
        """
        Insert vectors into Qdrant.

        Parameters:
            points:
                List of vectorized policy chunks.
        """

        logger.info(
            f"[Qdrant] Upserting "
            f"{len(points)} vectors"
        )

        self.client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=points
        )

    def search(
        self,
        query_vector: List[float],
        limit: int = 3
    ):
        """
        Perform semantic similarity search.

        Parameters:
            query_vector:
                Embedded query vector.

            limit:
                Number of results to return.

        Returns:
            List of Qdrant search results.
        """

        logger.info(
            f"[Qdrant] Searching "
            f"top {limit} matches"
        )

        results = self.client.query_points(
            collection_name=self.COLLECTION_NAME,
            query=query_vector,
            limit=limit
        )

        return results.points