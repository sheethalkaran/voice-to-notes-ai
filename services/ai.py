# -*- coding: utf-8 -*-
import os
import json
import time
import hashlib
from typing import Optional, Dict, List
from datetime import datetime, timedelta

class AIService:
    """Handle AI content generation - supports multiple providers"""
    
    def __init__(self):
        """Initialize AI service with best available provider"""
        # Try Groq first (recommended - free, no quota)
        groq_key = os.getenv("GROQ_API_KEY", "")
        gemini_key = os.getenv("GOOGLE_API_KEY", "")
        
        self.provider = None
        self.model = None
        
        if groq_key:
            try:
                from groq import Groq
                self.client = Groq(api_key=groq_key)
                self.provider = "groq"
                
                # List of available Groq models (updated regularly)
                models_to_try = [
                    "mixtral-8x7b-32768",      # May be deprecated
                    "gemma-7b-it",              # Fast, lightweight
                    "gemma2-9b-it",             # Gemma 2
                    "llama2-70b-4096",          # Powerful Llama 2
                    "llama-3-70b-8192",         # Llama 3
                    "llama-3.1-70b-versatile",  # Llama 3.1 Versatile
                    "llama-3.1-8b-instant",     # Fast Llama 3.1
                ]
                
                model_found = False
                for model_name in models_to_try:
                    try:
                        # Test the model with a simple request
                        response = self.client.chat.completions.create(
                            model=model_name,
                            messages=[{"role": "user", "content": "test"}],
                            max_tokens=10
                        )
                        self.model = model_name
                        print(f"✅ Using Groq Model: {model_name}")
                        model_found = True
                        break
                    except Exception as me:
                        # Silently skip unavailable models
                        continue
                
                if not model_found:
                    raise ValueError("No Groq models available - all models failed")
                    
            except Exception as e:
                print(f"⚠️ Groq setup failed: {str(e)[:100]}")
                self.provider = None
        
        if not self.provider and gemini_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=gemini_key)
                self.client = genai
                self.provider = "gemini"
                
                # Auto-detect best model
                models_to_try = [
                    "models/gemini-2.5-flash",
                    "models/gemini-2.5-pro",
                    "models/gemini-1.5-flash",
                    "models/gemini-1.5-pro",
                    "models/gemini-pro",
                ]
                
                for model_name in models_to_try:
                    try:
                        self.model_obj = genai.GenerativeModel(model_name)
                        # Test the model with a simple request
                        test = self.model_obj.generate_content("test", stream=False)
                        self.model = model_name
                        print(f"✅ Using Gemini: {model_name}")
                        break
                    except Exception as me:
                        # Silently skip unavailable models
                        continue
            except Exception as e:
                print(f"⚠️ Gemini setup failed: {str(e)[:50]}")
        
        if not self.provider:
            raise ValueError(
                "No AI API configured. Please set either:\n"
                "- GROQ_API_KEY (recommended: https://console.groq.com/)\n"
                "- GOOGLE_API_KEY (https://aistudio.google.com/app/apikey)"
            )
        
        # Cache
        self.cache = {}
        self.cache_timestamps = {}
        self.cache_ttl = 7200
        self.last_request_time = 0
        self.min_request_interval = 1
    
    def _get_cache_key(self, method: str, text: str, **kwargs) -> str:
        """Generate cache key"""
        key_data = f"{method}_{text[:100]}_{str(kwargs)}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _rate_limit(self):
        """Rate limiting"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)
        self.last_request_time = time.time()
    
    def _check_cache(self, cache_key: str) -> Optional[Dict]:
        """Check cache"""
        if cache_key in self.cache:
            cache_time = self.cache_timestamps.get(cache_key, 0)
            if time.time() - cache_time < self.cache_ttl:
                return self.cache[cache_key]
            else:
                del self.cache[cache_key]
                del self.cache_timestamps[cache_key]
        return None
    
    def _set_cache(self, cache_key: str, value: Dict):
        """Store in cache"""
        self.cache[cache_key] = value
        self.cache_timestamps[cache_key] = time.time()
        if len(self.cache) > 50:
            oldest_key = min(self.cache_timestamps, key=self.cache_timestamps.get)
            del self.cache[oldest_key]
            del self.cache_timestamps[oldest_key]
    
    def generate_summary(
        self,
        text: str,
        reading_level: str = "University",
        tone: str = "Academic",
        max_length: int = 500
    ) -> Dict:
        """Generate summary of lecture notes"""
        try:
            # Check cache
            cache_key = self._get_cache_key("summary", text, reading_level=reading_level, tone=tone)
            cached = self._check_cache(cache_key)
            if cached:
                return cached
            
            # Rate limit
            self._rate_limit()
            
            prompt = f"""
Summarize the following lecture content into study notes.

Reading Level: {reading_level}
Tone: {tone}
Max Words: {max_length}

Content:
{text[:2000]}

Provide a clear, well-structured summary that captures key points.
Format: Use bullet points for main concepts.
            """
            
            if self.provider == "groq":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=1000
                )
                result_text = response.choices[0].message.content
            else:  # gemini
                response = self.model_obj.generate_content(prompt)
                result_text = response.text
            
            result = {
                "success": True,
                "summary": result_text
            }
            self._set_cache(cache_key, result)
            return result
        
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "quota" in error_msg.lower():
                return {
                    "success": False,
                    "error": "API Quota Exceeded - Try again later or use Groq API (no quota limits)"
                }
            return {
                "success": False,
                "error": f"Error generating summary: {error_msg[:100]}"
            }
    
    def generate_quiz(
        self,
        text: str,
        num_questions: int = 5,
        difficulty: str = "Medium"
    ) -> Dict:
        """Generate multiple choice quiz from content"""
        try:
            # Check cache
            cache_key = self._get_cache_key("quiz", text, num=num_questions, difficulty=difficulty)
            cached = self._check_cache(cache_key)
            if cached:
                return cached
            
            # Rate limit
            self._rate_limit()
            
            prompt = f"""Create {num_questions} multiple choice questions from this content.
Difficulty Level: {difficulty}

Content:
{text[:1500]}

Return ONLY a valid JSON array, no markdown or extra text:
[{{"question": "Question text here?", "options": ["Option A", "Option B", "Option C", "Option D"], "correct_answer": 0, "explanation": "Explanation text"}}]

Make sure the JSON is valid and properly formatted."""
            
            if self.provider == "groq":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=2000
                )
                result_text = response.choices[0].message.content.strip()
            else:  # gemini
                response = self.model_obj.generate_content(prompt)
                result_text = response.text.strip()
            
            # Clean the response - remove markdown code blocks if present
            result_text = result_text.replace('```json', '').replace('```', '').strip()
            
            # Find JSON array
            json_start = result_text.find('[')
            json_end = result_text.rfind(']') + 1
            
            if json_start < 0 or json_end <= json_start:
                raise ValueError("No JSON array found in response")
            
            result_text = result_text[json_start:json_end]
            
            # Parse JSON
            questions = json.loads(result_text)
            
            # Validate questions
            if not isinstance(questions, list) or len(questions) == 0:
                raise ValueError("Invalid questions format")
            
            result = {
                "success": True,
                "questions": questions
            }
            self._set_cache(cache_key, result)
            return result
        
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "error": f"Failed to parse quiz response: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error generating quiz: {str(e)}"
            }
    
    def generate_flashcards(
        self,
        text: str,
        num_cards: int = 10
    ) -> Dict:
        """Generate flashcards from content"""
        try:
            cache_key = self._get_cache_key("flashcards", text, num=num_cards)
            cached = self._check_cache(cache_key)
            if cached:
                return cached
            
            self._rate_limit()
            
            prompt = f"""Create {num_cards} flashcards for studying.
Format each as: Question | Answer

Content:
{text[:1500]}

Return ONLY valid JSON array:
[{{"q": "question here", "a": "answer here"}}]
            """
            
            if self.provider == "groq":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.5,
                    max_tokens=2000
                )
                result_text = response.choices[0].message.content.strip()
            else:
                response = self.model_obj.generate_content(prompt)
                result_text = response.text.strip()
            
            # Extract JSON - handle markdown code blocks
            if '```' in result_text:
                result_text = result_text.split('```')[1]
                if result_text.startswith('json'):
                    result_text = result_text[4:]
            
            json_start = result_text.find('[')
            json_end = result_text.rfind(']') + 1
            if json_start >= 0 and json_end > json_start:
                result_text = result_text[json_start:json_end]
            
            # Try to parse and fix common issues
            try:
                flashcards = json.loads(result_text)
            except json.JSONDecodeError:
                # Try removing control characters
                result_text = ''.join(c for c in result_text if c.isprintable() or c in '\n\r\t')
                flashcards = json.loads(result_text)
            
            # Normalize to standard format
            normalized = []
            for card in flashcards:
                if isinstance(card, dict):
                    q = card.get('q') or card.get('question') or card.get('Q')
                    a = card.get('a') or card.get('answer') or card.get('A')
                    if q and a:
                        normalized.append({"question": str(q), "answer": str(a)})
            
            result = {
                "success": True,
                "flashcards": normalized
            }
            self._set_cache(cache_key, result)
            return result
        
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "error": f"Failed to parse flashcard response: {str(e)[:50]}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error generating flashcards: {str(e)[:100]}"
            }
    
    def extract_key_concepts(self, text: str) -> Dict:
        """Extract key concepts and topics from content"""
        try:
            cache_key = self._get_cache_key("concepts", text)
            cached = self._check_cache(cache_key)
            if cached:
                return cached
            
            self._rate_limit()
            
            prompt = f"""Extract key concepts from this content.

Content:
{text[:1500]}

Return a JSON object ONLY (no markdown, no text before or after):
{{"main_topics": ["Topic1", "Topic2"], "key_concepts": ["Concept1"], "important_points": ["Point1"], "technical_terms": {{"term": "definition"}}}}
            """
            
            if self.provider == "groq":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=1500
                )
                result_text = response.choices[0].message.content.strip()
            else:
                response = self.model_obj.generate_content(prompt)
                result_text = response.text.strip()
            
            # Extract JSON
            json_start = result_text.find('{')
            json_end = result_text.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                result_text = result_text[json_start:json_end]
            
            concepts = json.loads(result_text)
            result = {"success": True, "concepts": concepts}
            self._set_cache(cache_key, result)
            return result
        
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "error": f"Failed to parse concepts: {str(e)[:50]}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error extracting concepts: {str(e)[:100]}"
            }
    
    def translate_content(self, text: str, target_language: str) -> Dict:
        """Translate content to target language"""
        try:
            prompt = f"Translate to {target_language}:\n\n{text[:2000]}"
            
            if self.provider == "groq":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=2000
                )
                result_text = response.choices[0].message.content
            else:
                response = self.model_obj.generate_content(prompt)
                result_text = response.text
            
            return {"success": True, "translated_text": result_text}
        
        except Exception as e:
            return {"success": False, "error": f"Error translating: {str(e)[:100]}"}
    
    def analyze_tone(self, text: str) -> Dict:
        """Analyze the tone and sentiment of content"""
        try:
            prompt = f"""Analyze this content's tone and sentiment.

Content: {text[:1000]}

Return a JSON object ONLY (no markdown, no text before or after):
{{"detected_tone": "formal/casual", "formality_level": 8, "technical_level": 7, "sentiment": "positive", "primary_audience": "description"}}
            """
            
            if self.provider == "groq":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=500
                )
                result_text = response.choices[0].message.content.strip()
            else:
                response = self.model_obj.generate_content(prompt)
                result_text = response.text.strip()
            
            # Extract JSON
            json_start = result_text.find('{')
            json_end = result_text.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                result_text = result_text[json_start:json_end]
            
            analysis = json.loads(result_text)
            return {"success": True, "analysis": analysis}
        
        except json.JSONDecodeError as e:
            return {"success": False, "error": f"Failed to parse tone analysis: {str(e)[:50]}"}
        except Exception as e:
            return {"success": False, "error": f"Error analyzing tone: {str(e)[:100]}"}


# Keep old class name for backwards compatibility
class GeminiAIService(AIService):
    """Backwards compatibility wrapper"""
    pass
