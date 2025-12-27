"""
Enhanced Translation Module for MARGSATHI
Supports real translation, image OCR, and multiple translation providers
"""
from typing import Literal, Optional
from io import BytesIO
import logging
import os
import platform
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from pydantic import BaseModel, Field

# Translation providers
from deep_translator import GoogleTranslator
try:
    from googletrans import Translator as GoogleTransAPI
    GOOGLETRANS_AVAILABLE = True
except ImportError:
    GOOGLETRANS_AVAILABLE = False

logger = logging.getLogger(__name__)

router = APIRouter()

# Configure Tesseract path for Windows
# Configure OCR
EASYOCR_READER = None

def setup_ocr():
    """
    Initialize EasyOCR reader.
    Returns True if successful, False otherwise.
    """
    global EASYOCR_READER
    try:
        import easyocr
        # Initialize for English and Hindi by default, can add more
        # GPU=False to be safe on standard machines, set True if CUDA available
        logger.info("Initializing EasyOCR... (this may take a moment on first run)")
        EASYOCR_READER = easyocr.Reader(['en', 'hi'], gpu=False) 
        logger.info("EasyOCR initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize EasyOCR: {e}")
        return False

# Check OCR availability at startup
OCR_AVAILABLE = setup_ocr()



# Language mappings
LanguageCode = Literal["en", "hi", "bn", "ta", "te", "mr", "kn", "ml", "gu"]

LANGUAGE_NAMES = {
    "en": "English",
    "hi": "Hindi",
    "bn": "Bengali",
    "ta": "Tamil",
    "te": "Telugu",
    "mr": "Marathi",
    "kn": "Kannada",
    "ml": "Malayalam",
    "gu": "Gujarati",
}

DEEP_TRANSLATOR_CODES = {
    "en": "en",
    "hi": "hi",
    "bn": "bn",
    "ta": "ta",
    "te": "te",
    "mr": "mr",
    "kn": "kn",
    "ml": "ml",
    "gu": "gu",
}


class TranslationRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)
    target_lang: LanguageCode = Field(
        ...,
        description="Target language code, e.g. 'en', 'hi', 'ta'.",
    )
    source_lang: Optional[LanguageCode] = Field(
        default=None,
        description="Optional source language code. If omitted, auto-detected.",
    )
    provider: Optional[Literal["deep", "google", "mock"]] = Field(
        default="deep",
        description="Translation provider: 'deep' (free), 'google' (API), or 'mock' (demo)",
    )


class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str
    source_lang: str
    target_lang: str
    provider: str = "deep-translator"
    confidence: Optional[float] = Field(
        default=None,
        description="Translation confidence score (0-1)",
    )
    is_mock: bool = Field(
        default=False,
        description="Indicates if this is a mock translation",
    )


class ImageTranslationResponse(BaseModel):
    extracted_text: str
    translated_text: str
    source_lang: str
    target_lang: str
    provider: str
    ocr_confidence: Optional[float] = None
    is_mock: bool = False


class LanguageDetectionResponse(BaseModel):
    detected_lang: str
    language_name: str
    confidence: float


def translate_with_deep_translator(
    text: str, 
    source_lang: str, 
    target_lang: str
) -> tuple[str, float]:
    """Translate using Deep Translator (free, no API key needed)"""
    try:
        source_code = DEEP_TRANSLATOR_CODES.get(source_lang, "auto")
        target_code = DEEP_TRANSLATOR_CODES.get(target_lang, "en")
        
        translator = GoogleTranslator(source=source_code, target=target_code)
        translated = translator.translate(text)
        
        return translated, 0.95
    except Exception as e:
        logger.error(f"Deep Translator error: {e}")
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")


def translate_with_googletrans(
    text: str,
    source_lang: str,
    target_lang: str
) -> tuple[str, float]:
    """Translate using googletrans library (free, uses Google Translate)"""
    if not GOOGLETRANS_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Google Translate API not available. Install googletrans."
        )
    
    try:
        translator = GoogleTransAPI()
        result = translator.translate(
            text,
            src=source_lang if source_lang != "auto" else None,
            dest=target_lang
        )
        confidence = getattr(result, 'confidence', 0.9)
        return result.text, confidence
    except Exception as e:
        logger.error(f"Google Translate error: {e}")
        raise HTTPException(status_code=500, detail=f"Google Translate failed: {str(e)}")


def mock_translate(text: str, target_lang: str) -> tuple[str, float]:
    """Mock translation for demo purposes"""
    marker = f"[{target_lang.upper()}]"
    return f"{marker} {text}", 1.0


@router.post(
    "/translate",
    response_model=TranslationResponse,
    summary="Translate text with real translation support",
)
async def translate_text(payload: TranslationRequest) -> TranslationResponse:
    """
    Enhanced translation endpoint with multiple provider support.
    
    Providers:
    - 'deep': Deep Translator (free, recommended)
    - 'google': Google Translate API (requires setup)
    - 'mock': Demo mode (just adds language prefix)
    """
    source_lang = payload.source_lang or "auto"
    target_lang = payload.target_lang
    
    if payload.provider == "mock":
        translated_text, confidence = mock_translate(payload.text, target_lang)
        is_mock = True
        provider = "mock"
    elif payload.provider == "google":
        translated_text, confidence = translate_with_googletrans(
            payload.text, source_lang, target_lang
        )
        is_mock = False
        provider = "google-translate"
    else:  # default to deep translator
        translated_text, confidence = translate_with_deep_translator(
            payload.text, source_lang, target_lang
        )
        is_mock = False
        provider = "deep-translator"
    
    if source_lang == "auto":
        source_lang = "en"
    
    return TranslationResponse(
        original_text=payload.text,
        translated_text=translated_text,
        source_lang=source_lang,
        target_lang=target_lang,
        provider=provider,
        confidence=confidence,
        is_mock=is_mock,
    )


@router.post(
    "/translate-image",
    response_model=ImageTranslationResponse,
    summary="Extract text from image and translate",
)
async def translate_image(
    file: UploadFile = File(..., description="Image file containing text"),
    target_lang: LanguageCode = Form(..., description="Target language"),
    source_lang: Optional[LanguageCode] = Form(None, description="Source language"),
    provider: Literal["deep", "google", "mock"] = Form("deep", description="Translation provider"),
) -> ImageTranslationResponse:
    """
    OCR + Translation endpoint.
    1. Extracts text from uploaded image using Tesseract OCR
    2. Translates extracted text to target language
    
    Requires Tesseract OCR to be installed.
    """
    # Check if OCR is available
    if not OCR_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="OCR engine (EasyOCR) is not initialized. Please check server logs."
        )
    
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        image_data = await file.read()
        
        # Perform OCR using EasyOCR
        # detail=1 returns [box, text, confidence]
        results = EASYOCR_READER.readtext(image_data, detail=1)
        
        # Extract text and calculate average confidence
        extracted_parts = []
        confidences = []
        
        for _, text, conf in results:
            extracted_parts.append(text)
            confidences.append(conf)
            
        extracted_text = " ".join(extracted_parts)
        
        if not extracted_text.strip():
            raise HTTPException(
                status_code=400,
                detail="No text found in image. Please upload an image with clear text."
            )
        
        # Calculate average confidence
        ocr_confidence = sum(confidences) / len(confidences) if confidences else None
        
        # Translate extracted text
        source = source_lang or "auto"
        
        if provider == "mock":
            translated_text, _ = mock_translate(extracted_text, target_lang)
            is_mock = True
            provider_name = "mock"
        elif provider == "google":
            translated_text, _ = translate_with_googletrans(extracted_text, source, target_lang)
            is_mock = False
            provider_name = "google-translate"
        else:
            translated_text, _ = translate_with_deep_translator(extracted_text, source, target_lang)
            is_mock = False
            provider_name = "deep-translator"
        
        return ImageTranslationResponse(
            extracted_text=extracted_text.strip(),
            translated_text=translated_text,
            source_lang=source if source != "auto" else "en",
            target_lang=target_lang,
            provider=provider_name,
            ocr_confidence=ocr_confidence,
            is_mock=is_mock,
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Image translation error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process image: {str(e)}")


@router.post(
    "/detect-language",
    response_model=LanguageDetectionResponse,
    summary="Detect language of text",
)
async def detect_language(text: str = Form(...)) -> LanguageDetectionResponse:
    """Detect the language of input text."""
    try:
        if GOOGLETRANS_AVAILABLE:
            translator = GoogleTransAPI()
            detection = translator.detect(text)
            detected_code = detection.lang
            confidence = detection.confidence
        else:
            detected_code = "en"
            confidence = 0.5
        
        language_name = LANGUAGE_NAMES.get(detected_code, "Unknown")
        
        return LanguageDetectionResponse(
            detected_lang=detected_code,
            language_name=language_name,
            confidence=confidence,
        )
    except Exception as e:
        logger.error(f"Language detection error: {e}")
        raise HTTPException(status_code=500, detail=f"Language detection failed: {str(e)}")


@router.get("/status", summary="Check translation service status")
async def get_translation_status():
    """
    Returns the status of translation services and dependencies.
    """
    
    return {
        "text_translation": {
            "available": True,
            "providers": {
                "deep_translator": True,
                "googletrans": GOOGLETRANS_AVAILABLE,
                "mock": True
            }
        },
        "image_translation": {
            "available": OCR_AVAILABLE,
            "engine": "EasyOCR" if OCR_AVAILABLE else None,
            "installation_guide": None
        },
        "supported_languages": len(LANGUAGE_NAMES),
        "status": "healthy"
    }


@router.get("/languages", summary="Get supported languages")
async def get_supported_languages():
    """Returns list of supported languages."""
    return {
        "languages": [
            {"code": code, "name": name}
            for code, name in LANGUAGE_NAMES.items()
        ]
    }


# Backward compatible endpoint
@router.post(
    "/simple",
    response_model=TranslationResponse,
    summary="Simple translation (backward compatible)",
)
async def translate_text_simple(payload: TranslationRequest) -> TranslationResponse:
    """Backward compatible endpoint. Uses deep translator by default."""
    payload.provider = payload.provider or "deep"
    return await translate_text(payload)


