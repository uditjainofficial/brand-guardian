"""
Azure OpenAI LLM Provider

PURPOSE:
This service isolates:
- AzureChatOpenAI
- prompting
- reasoning execution
- response parsing

behind a clean orchestration contract.

WHY THIS EXISTS:
LangGraph nodes should NOT directly know:
- Azure OpenAI
- prompt execution details
- JSON parsing logic

Nodes should only call:

    audit_content(...)

This allows future migration to:
- OpenAI API
- Ollama
- Claude
- Gemini

WITHOUT changing orchestration logic.
"""

import json
import os
import logging
import re

from typing import Dict, Any

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import (
    SystemMessage,
    HumanMessage
)

from backend.src.services.llm.base import BaseLLMService


"""
Dedicated LLM logger.

Useful later for:
- token monitoring
- latency tracing
- prompt debugging
- provider observability
"""
logger = logging.getLogger("azure-llm")


class AzureLLMService(BaseLLMService):
    """
    Azure OpenAI implementation of the LLM contract.
    """

    def __init__(self):
        """
        Initialize Azure OpenAI chat model.
        """

        self.llm = AzureChatOpenAI(
            azure_deployment=os.getenv(
                "AZURE_OPENAI_CHAT_DEPLOYMENT"
            ),

            openai_api_version=os.getenv(
                "AZURE_OPENAI_API_VERSION"
            ),

            temperature=0.0
        )

    def audit_content(
        self,
        transcript: str,
        ocr_text: list[str],
        video_metadata: Dict[str, Any],
        retrieved_rules: str
    ) -> Dict[str, Any]:
        """
        Execute compliance reasoning workflow.

        FLOW:
        transcript + OCR
            ↓
        regulatory grounding
            ↓
        LLM reasoning
            ↓
        structured JSON output
        """

        logger.info(
            "[Azure LLM] Running compliance audit"
        )

        """
        System prompt containing:
        - compliance policies
        - audit instructions
        - output schema requirements
        """
        system_prompt = f"""
        You are a Senior Brand Compliance Auditor.

        OFFICIAL REGULATORY RULES:
        {retrieved_rules}

        INSTRUCTIONS:
        1. Analyze the Transcript and OCR text below.
        2. Identify ANY violations of the rules.
        3. Return strictly JSON in the following format:

        {{
            "compliance_results": [
                {{
                    "category": "Claim Validation",
                    "severity": "CRITICAL",
                    "description": "Explanation..."
                }}
            ],
            "status": "FAIL",
            "final_report": "Summary..."
        }}

        If no violations are found:
        - set "status" to "PASS"
        - set "compliance_results" to []
        """

        """
        User content containing multimodal inputs.
        """
        user_message = f"""
        VIDEO METADATA:
        {video_metadata}

        TRANSCRIPT:
        {transcript}

        ON-SCREEN TEXT (OCR):
        {ocr_text}
        """

        try:

            """
            Execute LLM reasoning.
            """
            response = self.llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_message)
            ])

            """
            Clean markdown formatting if model
            returns JSON wrapped inside ```json blocks.
            """
            content = response.content

            if "```" in content:
                content = re.search(
                    r"```(?:json)?(.*?)```",
                    content,
                    re.DOTALL
                ).group(1)

            """
            Parse structured JSON response.
            """
            audit_data = json.loads(
                content.strip()
            )

            """
            Normalize output into orchestration-friendly schema.
            """
            return {
                "compliance_results": audit_data.get(
                    "compliance_results",
                    []
                ),

                "final_status": audit_data.get(
                    "status",
                    "FAIL"
                ),

                "final_report": audit_data.get(
                    "final_report",
                    "No report generated."
                )
            }

        except Exception as e:

            logger.error(
                f"LLM Audit Failure: {str(e)}"
            )

            logger.error(
                f"Raw LLM Response: "
                f"{response.content if 'response' in locals() else 'None'}"
            )

            return {
                "errors": [str(e)],
                "final_status": "FAIL"
            }