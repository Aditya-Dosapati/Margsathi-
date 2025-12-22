from typing import Literal, Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field


router = APIRouter()


LanguageCode = Literal["en", "hi", "bn", "ta", "te", "mr", "kn", "ml", "gu"]


class TranslationRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)
    target_lang: LanguageCode = Field(
        ...,
        description="Target language code, e.g. 'en', 'hi', 'ta'.",
    )
    source_lang: Optional[LanguageCode] = Field(
        default=None,
        description="Optional source language code. If omitted, would be auto-detected in a real implementation.",
    )


class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str
    source_lang: LanguageCode
    target_lang: LanguageCode
    is_mock: bool = Field(
        default=True,
        description="Indicates this is a mocked translation for hackathon/demo use.",
    )


@router.post(
    "/simple",
    response_model=TranslationResponse,
    summary="Translate text between languages (mocked)",
)
async def translate_text(payload: TranslationRequest) -> TranslationResponse:
    """
    Minimal, dependency-free translation stub.

    For hackathons we avoid heavy external dependencies. This endpoint
    simply echoes the text back with a lightweight marker so your
    frontend can be built and demoed. Later, you can swap the internals
    out for a real translation service or LLM.
    """
    # In a real implementation, you'd call your translation provider here.
    marker = f"[{payload.target_lang.upper()}]"
    translated = f"{marker} {payload.text}"

    return TranslationResponse(
        original_text=payload.text,
        translated_text=translated,
        source_lang=payload.source_lang or "en",
        target_lang=payload.target_lang,
        is_mock=True,
    )


