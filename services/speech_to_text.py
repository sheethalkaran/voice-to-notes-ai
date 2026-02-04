# -*- coding: utf-8 -*-
import os
import tempfile
from typing import Optional
from openai import OpenAI

class SpeechToTextService:
    """Handle audio transcription using OpenAI Whisper"""
    
    def __init__(self):
        # Using free Whisper via OpenAI API (requires free API key)
        # Alternative: Use local Whisper with: pip install openai-whisper
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))
    
    @staticmethod
    def transcribe_with_local_whisper(audio_path: str, language: str = "en") -> dict:
        """
        Transcribe using local Whisper (FREE - no API key needed)
        Install with: pip install openai-whisper
        """
        try:
            import whisper
            
            # Load model (base model = 140MB, smaller than large)
            # Models: tiny, base, small, medium, large
            model = whisper.load_model("base", device="cpu")
            
            # Transcribe
            result = model.transcribe(
                audio_path,
                language=language if language != "auto" else None,
                verbose=False
            )
            
            return {
                "success": True,
                "text": result["text"],
                "language": result.get("language", language),
                "segments": result.get("segments", []),
            }
        
        except ImportError:
            return {
                "success": False,
                "error": "Whisper not installed. Run: pip install openai-whisper"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Transcription error: {str(e)}"
            }
    
    def transcribe_with_openai(self, audio_path: str, language: Optional[str] = None) -> dict:
        """
        Transcribe using OpenAI Whisper API
        Requires OPENAI_API_KEY environment variable
        FREE: 25 hours/month
        """
        try:
            if not self.client.api_key:
                return {
                    "success": False,
                    "error": "OpenAI API key not configured. Set OPENAI_API_KEY environment variable"
                }
            
            with open(audio_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language=language if language and language != "auto" else None,
                    response_format="verbose_json"
                )
            
            return {
                "success": True,
                "text": transcript.text,
                "language": getattr(transcript, "language", language),
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"OpenAI transcription error: {str(e)}"
            }
    
    @staticmethod
    def get_available_languages() -> dict:
        """Get list of supported languages"""
        return {
            "auto": "Auto-detect",
            "en": "English",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "it": "Italian",
            "pt": "Portuguese",
            "nl": "Dutch",
            "ru": "Russian",
            "zh": "Chinese",
            "ja": "Japanese",
            "ko": "Korean",
            "ar": "Arabic",
            "hi": "Hindi",
            "tr": "Turkish",
        }

# Use this function in app
def transcribe_audio(audio_path: str, language: str = "en", use_local: bool = True) -> dict:
    """
    Transcribe audio file
    
    Args:
        audio_path: Path to audio file
        language: Language code (e.g., 'en', 'es', 'auto')
        use_local: Use local Whisper (recommended for FREE) or OpenAI API
    
    Returns:
        dict: Transcription result with 'success', 'text', and optional 'error'
    """
    if use_local:
        return SpeechToTextService.transcribe_with_local_whisper(audio_path, language)
    else:
        service = SpeechToTextService()
        return service.transcribe_with_openai(audio_path, language)
