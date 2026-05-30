"""
Groq LLM Provider

PURPOSE:
Provides compliance auditing using Groq.

WHY THIS EXISTS:
Allows Brand Guardian to run without
Azure OpenAI.

Current Model:
- llama-3.3-70b-versatile

Future Models:
- openai/gpt-oss-120b
- deepseek-r1-distill-llama-70b
- future Groq releases
"""

import json
import logging
import re

from dotenv import load_dotenv

load_dotenv()

from typing import Dict, Any

from langchain_groq import ChatGroq

from backend.src.services.llm.base import (
    BaseLLMService
)

from backend.src.services.llm.prompt_templates import (
    build_system_prompt,
    build_user_prompt
)


logger = logging.getLogger("groq-llm")


class GroqLLMService(
    BaseLLMService
):
    """
    Groq implementation of the LLM contract.
    """

    def __init__(self):
        """
        Initialize Groq chat model.
        """

        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.0
        )

    def audit_content(
        self,
        transcript: str,
        ocr_text: list[str],
        video_metadata: Dict[str, Any],
        retrieved_rules: str
    ) -> Dict[str, Any]:

        logger.info(
            "[Groq LLM] Running compliance audit"
        )

        system_prompt = (
            build_system_prompt(
                retrieved_rules
            )
        )

        user_prompt = (
            build_user_prompt(
                transcript=transcript,
                ocr_text=ocr_text,
                video_metadata=video_metadata
            )
        )

        try:

            response = self.llm.invoke([
                (
                    "system",
                    system_prompt
                ),
                (
                    "human",
                    user_prompt
                )
            ])

            content = response.content

            if "```" in content:

                match = re.search(
                    r"```(?:json)?(.*?)```",
                    content,
                    re.DOTALL
                )

                if match:
                    content = match.group(1)

            audit_data = json.loads(
                content.strip()
            )

            return {
                "compliance_results":
                audit_data.get(
                    "compliance_results",
                    []
                ),

                "final_status":
                audit_data.get(
                    "status",
                    "FAIL"
                ),

                "final_report":
                audit_data.get(
                    "final_report",
                    "No report generated."
                )
            }

        except Exception as e:

            logger.error(
                f"Groq Audit Failure: {str(e)}"
            )

            logger.error(
                f"Raw LLM Response: "
                f"{response.content if 'response' in locals() else 'None'}"
            )

            return {
                "errors": [str(e)],
                "final_status": "FAIL"
            }