# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

class Settings:
    """Application settings and configuration"""
    
    # Google Gemini API
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    
    # Application Settings
    MAX_UPLOAD_SIZE: int = 25 * 1024 * 1024  # 25MB
    SUPPORTED_AUDIO_FORMATS: tuple = ("mp3", "wav", "m4a", "ogg", "webm", "flac")
    
    # Streamlit Settings
    PAGE_TITLE: str = "Lecture Voice-to-Notes Generator"
    PAGE_ICON: str = "🎙️"
    LAYOUT: str = "wide"
    INITIAL_SIDEBAR_STATE: str = "auto"
    
    # AI Model Settings
    GEMINI_MODEL: str = "gemini-1.5-flash"
    TEMPERATURE: float = 0.7
    TOP_P: float = 0.9
    TOP_K: int = 40
    
    # Supported Languages
    LANGUAGES: dict = {
        "English": "en",
        "Spanish": "es",
        "French": "fr",
        "German": "de",
        "Chinese": "zh",
        "Japanese": "ja",
        "Hindi": "hi",
        "Arabic": "ar",
    }
    
    # Tone Options
    TONES: list = ["Formal", "Casual", "Technical", "Academic", "Conversational"]
    
    # Reading Levels
    READING_LEVELS: list = ["Elementary", "High School", "University", "Professional"]
    
    # Quiz Difficulty Levels
    DIFFICULTY_LEVELS: list = ["Easy", "Medium", "Hard"]
    
    @staticmethod
    def validate_config() -> bool:
        """Validate that all required settings are configured"""
        required_keys = ["GOOGLE_API_KEY"]
        settings = Settings()
        
        for key in required_keys:
            if not getattr(settings, key, ""):
                print(f"❌ Missing required config: {key}")
                return False
        
        return True

settings = Settings()
