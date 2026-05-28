"""
LLM Service Abstraction

PURPOSE:
This defines the orchestration-facing contract
for all LLM providers.

WHY THIS EXISTS:
LangGraph nodes should NOT directly know:
- Azure OpenAI
- OpenAI API
- Ollama
- Claude
- Gemini

Nodes should only know:
    audit_content(...)

This allows future provider swapping
without changing orchestration logic.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseLLMService(ABC):
    """
    Abstract base class for all LLM providers.
    """

    @abstractmethod
    def audit_content(
        self,
        transcript: str,
        ocr_text: list[str],
        video_metadata: Dict[str, Any],
        retrieved_rules: str
    ) -> Dict[str, Any]:
        """
        Run compliance audit reasoning.

        Returns:
            Structured compliance audit response.
        """
        pass