"""
Prompt Templates

PURPOSE:
Centralize all compliance prompts.

WHY THIS EXISTS:
Multiple LLM providers should share
the same reasoning instructions.

Providers:
- Azure OpenAI
- Groq
- Future OpenAI
- Future Gemini

should all use identical prompts.
"""


def build_system_prompt(
    retrieved_rules: str
) -> str:

    return f"""
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


def build_user_prompt(
    transcript: str,
    ocr_text: list[str],
    video_metadata: dict
) -> str:

    return f"""
    VIDEO METADATA:
    {video_metadata}

    TRANSCRIPT:
    {transcript}

    ON-SCREEN TEXT (OCR):
    {ocr_text}
    """