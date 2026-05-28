"""
Azure Retrieval Provider

PURPOSE:
This service isolates Azure AI Search + Azure OpenAI Embeddings
behind a retrieval abstraction layer.

WHY THIS EXISTS:
Previously, LangGraph nodes directly instantiated:
- AzureSearch
- AzureOpenAIEmbeddings

That tightly coupled orchestration logic to Azure infrastructure.

Now:
Nodes only interact with:

    retrieve_rules(...)

This allows future migrations to:
- Qdrant
- FAISS
- ChromaDB
- Hybrid Retrieval

WITHOUT changing orchestration logic.
"""

import os
import logging

from typing import List

from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import AzureSearch

from backend.src.services.retrieval.base import BaseRetrievalService


"""
Dedicated retrieval logger.

Useful later for:
- retrieval latency monitoring
- debugging bad RAG results
- provider-level observability
"""
logger = logging.getLogger("azure-retrieval")


class AzureRetrievalService(BaseRetrievalService):
    """
    Azure AI Search implementation of the retrieval contract.

    Responsibilities:
    - generate embeddings for queries
    - perform vector similarity search
    - return relevant policy chunks
    """

    def __init__(self):
        """
        Initialize:
        1. Embedding model
        2. Azure AI Search vector store
        """

        """
        Embedding model used for semantic similarity search.

        Converts text like:
            "missing sponsorship disclosure"

        into high-dimensional vectors.
        """
        self.embeddings = AzureOpenAIEmbeddings(
            azure_deployment="text-embedding-3-small",
            openai_api_version=os.getenv(
                "AZURE_OPENAI_API_VERSION"
            ),
        )

        """
        Azure AI Search vector database connection.

        This index already contains:
        - FTC Influencer Guidelines
        - YouTube Ad Policies

        Those documents were:
        - chunked
        - embedded
        - indexed previously
        """
        self.vector_store = AzureSearch(
            azure_search_endpoint=os.getenv(
                "AZURE_SEARCH_ENDPOINT"
            ),

            azure_search_key=os.getenv(
                "AZURE_SEARCH_API_KEY"
            ),

            index_name=os.getenv(
                "AZURE_SEARCH_INDEX_NAME"
            ),

            embedding_function=self.embeddings.embed_query
        )

    def retrieve_rules(
        self,
        query: str,
        k: int = 3
    ) -> List[str]:
        """
        Retrieve the most relevant policy chunks.

        FLOW:
        query
            ↓
        embeddings
            ↓
        vector similarity search
            ↓
        relevant compliance rules
        """

        logger.info(
            "[Azure Retrieval] Running similarity search"
        )

        """
        Run semantic similarity search against
        the vector database.
        """
        docs = self.vector_store.similarity_search(
            query,
            k=k
        )

        """
        Normalize output.

        IMPORTANT:
        The orchestration layer should NOT know:
        - AzureSearch exists
        - embeddings exist
        - vector DB implementation details

        It only receives:
            List[str]
        """

        return [
            doc.page_content
            for doc in docs
        ]