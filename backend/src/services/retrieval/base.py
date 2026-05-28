from abc import ABC, abstractmethod
from typing import List


class BaseRetrievalService(ABC):
    """
    Abstract base class for all policy retrieval providers.

    Retrieval providers are responsible for:
    - vector similarity search
    - policy grounding
    - returning relevant compliance documents
    """

    @abstractmethod
    def retrieve_rules(
        self,
        query: str,
        k: int = 3
    ) -> List[str]:
        """
        Retrieve relevant compliance rules.

        Returns:
            List[str]: Relevant policy text chunks
        """
        pass