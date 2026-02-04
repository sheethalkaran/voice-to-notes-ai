import firebase_admin
from firebase_admin import credentials, db, storage, auth
import os
import json
from typing import Optional, Dict, List
from datetime import datetime

class FirebaseService:
    """Handle Firebase Realtime Database and Storage operations"""
    
    _initialized = False
    
    def __init__(self):
        if not FirebaseService._initialized:
            self._initialize_firebase()
            FirebaseService._initialized = True
    
    @staticmethod
    def _initialize_firebase():
        """Initialize Firebase Admin SDK"""
        try:
            # Try to load from environment variables first
            firebase_config = {
                "type": os.getenv("FIREBASE_TYPE", "service_account"),
                "project_id": os.getenv("FIREBASE_PROJECT_ID", ""),
                "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID", ""),
                "private_key": os.getenv("FIREBASE_PRIVATE_KEY", "").replace("\\n", "\n"),
                "client_email": os.getenv("FIREBASE_CLIENT_EMAIL", ""),
                "client_id": os.getenv("FIREBASE_CLIENT_ID", ""),
                "auth_uri": os.getenv("FIREBASE_AUTH_URI", "https://accounts.google.com/o/oauth2/auth"),
                "token_uri": os.getenv("FIREBASE_TOKEN_URI", "https://oauth2.googleapis.com/token"),
                "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL", "https://www.googleapis.com/oauth2/v1/certs"),
                "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL", ""),
            }
            
            # Check if service-account-key.json exists (for local development)
            if os.path.exists("service-account-key.json"):
                cred = credentials.Certificate("service-account-key.json")
            else:
                cred = credentials.Certificate(firebase_config)
            
            firebase_admin.initialize_app(cred, {
                'databaseURL': os.getenv("FIREBASE_DATABASE_URL", ""),
                'storageBucket': os.getenv("FIREBASE_STORAGE_BUCKET", ""),
            })
        
        except Exception as e:
            print(f"Firebase initialization warning: {str(e)}")
            print("Some features will be limited without Firebase. Continue for local mode.")
    
    def save_lecture(self, user_id: str, lecture_data: Dict) -> Dict:
        """Save lecture transcription and metadata"""
        try:
            timestamp = datetime.now().isoformat()
            lecture_id = f"lecture_{timestamp.replace(':', '_')}"
            
            ref = db.reference(f"users/{user_id}/lectures/{lecture_id}")
            ref.set({
                "id": lecture_id,
                "title": lecture_data.get("title", "Untitled Lecture"),
                "transcript": lecture_data.get("transcript", ""),
                "summary": lecture_data.get("summary", ""),
                "language": lecture_data.get("language", "en"),
                "tone": lecture_data.get("tone", "Academic"),
                "created_at": timestamp,
                "duration_seconds": lecture_data.get("duration", 0),
                "metadata": lecture_data.get("metadata", {})
            })
            
            return {
                "success": True,
                "lecture_id": lecture_id,
                "message": "Lecture saved successfully"
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Error saving lecture: {str(e)}"
            }
    
    def save_quiz(self, user_id: str, quiz_data: Dict) -> Dict:
        """Save quiz to database"""
        try:
            timestamp = datetime.now().isoformat()
            quiz_id = f"quiz_{timestamp.replace(':', '_')}"
            
            ref = db.reference(f"users/{user_id}/quizzes/{quiz_id}")
            ref.set({
                "id": quiz_id,
                "lecture_id": quiz_data.get("lecture_id", ""),
                "questions": quiz_data.get("questions", []),
                "difficulty": quiz_data.get("difficulty", "Medium"),
                "created_at": timestamp,
                "user_score": quiz_data.get("score", 0)
            })
            
            return {
                "success": True,
                "quiz_id": quiz_id,
                "message": "Quiz saved successfully"
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Error saving quiz: {str(e)}"
            }
    
    def save_flashcards(self, user_id: str, flashcard_data: Dict) -> Dict:
        """Save flashcards to database"""
        try:
            timestamp = datetime.now().isoformat()
            deck_id = f"deck_{timestamp.replace(':', '_')}"
            
            ref = db.reference(f"users/{user_id}/flashcard_decks/{deck_id}")
            ref.set({
                "id": deck_id,
                "lecture_id": flashcard_data.get("lecture_id", ""),
                "name": flashcard_data.get("name", "Study Deck"),
                "cards": flashcard_data.get("cards", []),
                "created_at": timestamp,
                "total_cards": len(flashcard_data.get("cards", []))
            })
            
            return {
                "success": True,
                "deck_id": deck_id,
                "message": "Flashcards saved successfully"
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Error saving flashcards: {str(e)}"
            }
    
    def get_user_lectures(self, user_id: str) -> Dict:
        """Get all lectures for a user"""
        try:
            ref = db.reference(f"users/{user_id}/lectures")
            lectures = ref.get()
            
            return {
                "success": True,
                "lectures": lectures.val() if lectures.exists() else {}
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Error fetching lectures: {str(e)}"
            }
    
    def upload_audio_to_storage(self, user_id: str, file_path: str, file_name: str) -> Dict:
        """Upload audio file to Firebase Storage"""
        try:
            bucket = storage.bucket()
            blob = bucket.blob(f"lectures/{user_id}/{file_name}")
            blob.upload_from_filename(file_path)
            
            return {
                "success": True,
                "url": blob.public_url,
                "message": "Audio uploaded successfully"
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Error uploading audio: {str(e)}"
            }
    
    def create_user_profile(self, user_id: str, user_data: Dict) -> Dict:
        """Create or update user profile"""
        try:
            ref = db.reference(f"users/{user_id}")
            ref.set({
                "user_id": user_id,
                "email": user_data.get("email", ""),
                "name": user_data.get("name", ""),
                "created_at": datetime.now().isoformat(),
                "preferences": user_data.get("preferences", {})
            })
            
            return {
                "success": True,
                "message": "User profile created"
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Error creating profile: {str(e)}"
            }
