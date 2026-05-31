"""
Groq LLM Provider

PURPOSE:
Provides compliance auditing using Groq.

ARCHITECTURE BENEFITS:
- provider independence
- structured JSON output
- retry protection
- robust response parsing
"""

import json
import logging
import re
import time

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

    MAX_RETRIES = 3

    def __init__(self):

        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.0
        )

    def _extract_json(
        self,
        content: str
    ) -> Dict[str, Any]:
        """
        Extract JSON from LLM response.

        Handles:

        ```json
        {...}
        ```

        or

        Here's my analysis:

        {...}
        """

        if "```" in content:

            match = re.search(
                r"```(?:json)?(.*?)```",
                content,
                re.DOTALL
            )

            if match:
                content = match.group(1)

        try:
            return json.loads(
                content.strip()
            )

        except Exception:

            match = re.search(
                r"\{.*\}",
                content,
                re.DOTALL
            )

            if match:
                return json.loads(
                    match.group(0)
                )

            raise ValueError(
                "No valid JSON found in response."
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

        response = None

        for attempt in range(
            1,
            self.MAX_RETRIES + 1
        ):

            try:

                logger.info(
                    f"[Groq] Attempt "
                    f"{attempt}/{self.MAX_RETRIES}"
                )

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

                audit_data = (
                    self._extract_json(
                        response.content
                    )
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

                logger.warning(
                    f"[Groq] Attempt "
                    f"{attempt} failed: {e}"
                )

                if attempt < self.MAX_RETRIES:

                    wait_time = (
                        2 ** attempt
                    )

                    logger.info(
                        f"[Groq] Retrying in "
                        f"{wait_time}s..."
                    )

                    time.sleep(
                        wait_time
                    )

                else:

                    logger.error(
                        "[Groq] Exhausted retries"
                    )

                    logger.error(
                        f"Raw Response: "
                        f"{response.content if response else 'None'}"
                    )

                    return {
                        "errors": [str(e)],
                        "final_status": "FAIL"
                    }