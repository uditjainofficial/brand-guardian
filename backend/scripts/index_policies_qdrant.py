"""
Qdrant Policy Indexer

PURPOSE:
Loads compliance PDFs from backend/data,
chunks them, generates embeddings,
and stores them in Qdrant.

This replaces:

Azure OpenAI Embeddings
        +
Azure AI Search

with:

Sentence Transformers
        +
Qdrant
"""

import os
import glob
import logging
import uuid
import sys
from pathlib import Path

"""
Allow standalone script execution.

Adds project root to Python path so imports like:

    from backend.src...

work correctly when running:

    python backend/scripts/index_policies_qdrant.py
"""

project_root = Path(__file__).resolve().parents[2]

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from langchain_community.document_loaders import (
    PyPDFLoader
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from qdrant_client.models import (
    PointStruct
)

from backend.src.services.retrieval.local_embeddings import (
    LocalEmbeddingService
)

from backend.src.services.retrieval.qdrant_store import (
    QdrantStore
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(
    "qdrant-policy-indexer"
)


def index_documents():
    """
    Build local compliance knowledge base.
    """

    logger.info(
        "=" * 60
    )

    logger.info(
        "Starting Qdrant Policy Indexing"
    )

    logger.info(
        "=" * 60
    )

    # =====================================================
    # DATA LOCATION
    # =====================================================

    current_dir = os.path.dirname(
        os.path.abspath(__file__)
    )

    data_folder = os.path.join(
        current_dir,
        "../data"
    )

    pdf_files = glob.glob(
        os.path.join(
            data_folder,
            "*.pdf"
        )
    )

    if not pdf_files:

        logger.warning(
            f"No PDFs found in {data_folder}"
        )

        return

    logger.info(
        f"Found {len(pdf_files)} PDFs"
    )

    # =====================================================
    # EMBEDDINGS + QDRANT
    # =====================================================

    embedding_service = (
        LocalEmbeddingService()
    )

    qdrant_store = (
        QdrantStore()
    )

    all_chunks = []

    # =====================================================
    # LOAD + CHUNK
    # =====================================================

    for pdf_path in pdf_files:

        logger.info(
            f"Loading: "
            f"{os.path.basename(pdf_path)}"
        )

        loader = PyPDFLoader(
            pdf_path
        )

        documents = loader.load()

        splitter = (
            RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
        )

        chunks = splitter.split_documents(
            documents
        )

        for chunk in chunks:

            chunk.metadata[
                "source"
            ] = os.path.basename(
                pdf_path
            )

        all_chunks.extend(
            chunks
        )

        logger.info(
            f"Created {len(chunks)} chunks"
        )

    logger.info(
        f"Total Chunks: {len(all_chunks)}"
    )

    # =====================================================
    # EMBEDDINGS
    # =====================================================

    texts = [
        doc.page_content
        for doc in all_chunks
    ]

    embeddings = (
        embedding_service.embed_documents(
            texts
        )
    )

    vector_size = len(
        embeddings[0]
    )

    qdrant_store.create_collection(
        vector_size=vector_size
    )

    # =====================================================
    # BUILD POINTS
    # =====================================================

    points = []

    for doc, vector in zip(
        all_chunks,
        embeddings
    ):

        points.append(

            PointStruct(
                id=str(
                    uuid.uuid4()
                ),

                vector=vector,

                payload={
                    "text":
                    doc.page_content,

                    "source":
                    doc.metadata.get(
                        "source",
                        "unknown"
                    )
                }
            )
        )

    # =====================================================
    # UPSERT
    # =====================================================

    logger.info(
        f"Uploading "
        f"{len(points)} vectors..."
    )

    qdrant_store.upsert_points(
        points
    )

    logger.info(
        "=" * 60
    )

    logger.info(
        "Knowledge Base Ready"
    )

    logger.info(
        "=" * 60
    )


if __name__ == "__main__":
    index_documents()