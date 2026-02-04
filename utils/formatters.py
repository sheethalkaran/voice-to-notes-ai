import math
from typing import List, Dict
from datetime import datetime

class Formatters:
    """Output formatting utilities"""
    
    @staticmethod
    def format_duration(seconds: float) -> str:
        """Format duration in human-readable format"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours}h {minutes}m {secs}s"
        elif minutes > 0:
            return f"{minutes}m {secs}s"
        else:
            return f"{secs}s"
    
    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.2f} TB"
    
    @staticmethod
    def estimate_reading_time(text: str, words_per_minute: int = 200) -> str:
        """Estimate reading time for text"""
        words = len(text.split())
        minutes = math.ceil(words / words_per_minute)
        
        if minutes < 1:
            return "Less than 1 minute"
        elif minutes == 1:
            return "1 minute"
        else:
            return f"{minutes} minutes"
    
    @staticmethod
    def format_timestamp(timestamp: str) -> str:
        """Format ISO timestamp to readable format"""
        try:
            dt = datetime.fromisoformat(timestamp)
            return dt.strftime("%B %d, %Y at %I:%M %p")
        except:
            return timestamp
    
    @staticmethod
    def format_text_with_line_breaks(text: str, max_line_width: int = 80) -> str:
        """Format text with proper line breaks"""
        lines = []
        current_line = ""
        
        for word in text.split():
            if len(current_line) + len(word) + 1 <= max_line_width:
                current_line += word + " "
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        
        if current_line:
            lines.append(current_line.strip())
        
        return "\n".join(lines)
    
    @staticmethod
    def create_summary_bullets(summary: str) -> List[str]:
        """Convert summary to bullet points"""
        paragraphs = summary.split('\n')
        bullets = [p.strip() for p in paragraphs if p.strip()]
        return bullets
    
    @staticmethod
    def format_quiz_display(questions: List[Dict]) -> str:
        """Format quiz questions for display"""
        formatted = []
        for idx, q in enumerate(questions, 1):
            formatted.append(f"\n**Question {idx}:** {q.get('question', '')}\n")
            for i, option in enumerate(q.get('options', []), 1):
                formatted.append(f"  {chr(64+i)}) {option}")
        
        return "\n".join(formatted)
