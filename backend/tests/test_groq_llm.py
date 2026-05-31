from dotenv import load_dotenv

load_dotenv()

from backend.src.services.llm.groq_llm import (
    GroqLLMService
)

llm = GroqLLMService()

result = llm.audit_content(
    transcript="""
    This product cures diabetes in 7 days.
    Buy now using my affiliate link.
    """,

    ocr_text=[
        "Guaranteed Results",
        "Limited Time Offer"
    ],

    video_metadata={
        "platform": "youtube"
    },

    retrieved_rules="""
    Endorsements must be disclosed.

    Health claims require evidence.

    Misleading claims are prohibited.
    """
)

print(result)