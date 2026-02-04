from typing import Tuple
import re

class Validators:
    """Input validation utilities"""
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            return True, "Valid email"
        return False, "Invalid email format"
    
    @staticmethod
    def validate_text_length(text: str, min_length: int = 10, max_length: int = 100000) -> Tuple[bool, str]:
        """Validate text length"""
        length = len(text)
        if length < min_length:
            return False, f"Text too short. Minimum: {min_length} characters"
        if length > max_length:
            return False, f"Text too long. Maximum: {max_length} characters"
        return True, "Valid text length"
    
    @staticmethod
    def validate_title(title: str) -> Tuple[bool, str]:
        """Validate lecture title"""
        if len(title.strip()) == 0:
            return False, "Title cannot be empty"
        if len(title) > 200:
            return False, "Title too long (max 200 characters)"
        return True, "Valid title"
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Remove invalid characters from filename"""
        invalid_chars = r'[<>:"/\\|?*]'
        return re.sub(invalid_chars, '_', filename)
