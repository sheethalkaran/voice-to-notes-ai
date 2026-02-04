# -*- coding: utf-8 -*-
import io
import os
import tempfile
from typing import Tuple, Optional
import librosa
import soundfile as sf
import numpy as np
from pydub import AudioSegment

class AudioProcessor:
    """Handle audio file processing and conversion"""
    
    SUPPORTED_FORMATS = ("mp3", "wav", "m4a", "ogg", "webm", "flac")
    MAX_FILE_SIZE = 25 * 1024 * 1024  # 25MB
    
    @staticmethod
    def validate_audio_file(file_path: str) -> Tuple[bool, str]:
        """Validate audio file format and size"""
        # Check file extension
        ext = os.path.splitext(file_path)[1].lstrip(".").lower()
        if ext not in AudioProcessor.SUPPORTED_FORMATS:
            return False, f"Unsupported format. Supported: {', '.join(AudioProcessor.SUPPORTED_FORMATS)}"
        
        # Check file size
        file_size = os.path.getsize(file_path)
        if file_size > AudioProcessor.MAX_FILE_SIZE:
            return False, f"File too large. Maximum: 25MB, Your file: {file_size / (1024*1024):.2f}MB"
        
        return True, "Valid audio file"
    
    @staticmethod
    def convert_to_wav(input_path: str, output_path: Optional[str] = None) -> str:
        """Convert any audio format to WAV"""
        try:
            # Load audio with librosa
            audio_data, sample_rate = librosa.load(input_path, sr=16000, mono=True)
            
            # Create temp file if output not specified
            if output_path is None:
                output_path = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
            
            # Save as WAV
            sf.write(output_path, audio_data, sample_rate)
            return output_path
        
        except Exception as e:
            raise Exception(f"Error converting audio: {str(e)}")
    
    @staticmethod
    def get_audio_duration(file_path: str) -> float:
        """Get audio duration in seconds"""
        try:
            audio_data, sample_rate = librosa.load(file_path, sr=None)
            duration = librosa.get_duration(y=audio_data, sr=sample_rate)
            return duration
        except Exception as e:
            raise Exception(f"Error getting audio duration: {str(e)}")
    
    @staticmethod
    def split_audio_chunks(file_path: str, chunk_duration: int = 600) -> list:
        """
        Split long audio into chunks for processing
        Default: 10 minute chunks
        """
        try:
            audio = AudioSegment.from_file(file_path)
            chunk_duration_ms = chunk_duration * 1000
            
            chunks = []
            for i in range(0, len(audio), chunk_duration_ms):
                chunk = audio[i:i + chunk_duration_ms]
                temp_path = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
                chunk.export(temp_path, format="wav")
                chunks.append(temp_path)
            
            return chunks
        
        except Exception as e:
            raise Exception(f"Error splitting audio: {str(e)}")
    
    @staticmethod
    def get_audio_stats(file_path: str) -> dict:
        """Get audio file statistics"""
        try:
            audio_data, sample_rate = librosa.load(file_path, sr=16000, mono=True)
            
            stats = {
                "duration_seconds": librosa.get_duration(y=audio_data, sr=sample_rate),
                "sample_rate": sample_rate,
                "channels": 1,
                "rms_energy": float(np.sqrt(np.mean(audio_data ** 2))),
                "max_amplitude": float(np.max(np.abs(audio_data))),
            }
            return stats
        
        except Exception as e:
            raise Exception(f"Error getting audio stats: {str(e)}")
