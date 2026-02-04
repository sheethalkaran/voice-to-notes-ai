# Lecture Voice-to-Notes Generator

Convert lecture audio recordings into comprehensive study materials using AI-powered transcription and content generation.

[Live Demo](https://huggingface.co/spaces/sheethalk/voice-to-notes-ai) | Try it online

## Features

- **Audio Transcription**: Convert lectures to text with multi-language support (MP3, WAV, M4A, OGG, WebM, FLAC)
- **Content Summarization**: AI-generated summaries with configurable tone and reading level
- **Concept Extraction**: Automatically identify and organize key concepts from lectures
- **Quiz Generation**: Create multiple-choice quizzes at varying difficulty levels
- **Flashcard Creation**: Generate study flashcards for active learning
- **Tone Analysis**: Evaluate and describe lecture tone characteristics

## Tech Stack

- **Frontend**: Streamlit
- **AI Services**: Groq (primary), Google Gemini (fallback)
- **Speech Recognition**: OpenAI Whisper API
- **Audio Processing**: librosa, pydub
- **Language**: Python 3.9+


## Usage

1. **Upload Audio**: Select an audio file (max 25MB)
2. **Choose Settings**: 
   - Select language and output language
   - Configure tone and reading level preferences
   - Select difficulty for quizzes
3. **Generate Materials**:
   - Transcribe lecture
   - Generate summary, concepts, quiz, and flashcards
4. **Download Results**: Export all generated content


## Project Structure

```
├── app.py                 # Main Streamlit application
├── config/
│   ├── settings.py       # Configuration and constants
├── services/
│   ├── ai.py             # AI content generation
│   ├── speech_to_text.py # Audio transcription
│   └── audio_processor.py # Audio handling
├── utils/
│   ├── validators.py     # Input validation
│   ├── formatters.py     # Output formatting
│   └── helpers.py        # Utility functions
└── requirements.txt      # Dependencies
```

## Requirements

- API keys for Groq and/or OpenAI/Google Gemini
- Minimum 4GB RAM for optimal performance
- Stable internet connection for API calls

## Performance

- Transcription time: ~1 minute per 10 minutes of audio
- Content generation: 30-60 seconds depending on lecture length and complexity

## Security

- API keys stored locally in `.env` (not version controlled)
- No permanent data storage in cloud
- Audio files processed temporarily and deleted after session


