import os
import json
from typing import Optional, Dict, Any

class FileHelpers:
    """File handling utilities"""
    
    @staticmethod
    def ensure_directory(path: str) -> bool:
        """Ensure directory exists, create if not"""
        try:
            os.makedirs(path, exist_ok=True)
            return True
        except Exception as e:
            print(f"Error creating directory: {e}")
            return False
    
    @staticmethod
    def save_json(data: Dict, filepath: str) -> bool:
        """Save data as JSON file"""
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving JSON: {e}")
            return False
    
    @staticmethod
    def load_json(filepath: str) -> Optional[Dict]:
        """Load JSON file"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading JSON: {e}")
        return None
    
    @staticmethod
    def delete_file(filepath: str) -> bool:
        """Delete a file"""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
        except Exception as e:
            print(f"Error deleting file: {e}")
        return False

class StringHelpers:
    """String manipulation utilities"""
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
        """Truncate text to max length"""
        if len(text) > max_length:
            return text[:max_length - len(suffix)] + suffix
        return text
    
    @staticmethod
    def count_words(text: str) -> int:
        """Count words in text"""
        return len(text.split())
    
    @staticmethod
    def count_sentences(text: str) -> int:
        """Count sentences in text"""
        sentences = text.split('.')
        return len([s for s in sentences if s.strip()])
    
    @staticmethod
    def highlight_keywords(text: str, keywords: list) -> str:
        """Highlight keywords in text (for markdown)"""
        result = text
        for keyword in keywords:
            result = result.replace(keyword, f"**{keyword}**")
        return result
