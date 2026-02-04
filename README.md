# Voice-to-Notes Generator

A professional application that converts lecture audio recordings into comprehensive study materials using advanced AI technology.

## Overview

This application streamlines the study preparation process by automatically converting audio lectures into multiple formats including transcripts, summaries, quizzes, flashcards, and concept extractions. Built with Streamlit and powered by AI services, it enables students and educators to maximize learning efficiency.

## Key Features

- **Audio Transcription**: Convert audio files to text with support for multiple formats and languages
- **Content Summarization**: Generate concise, AI-powered summaries from transcripts
- **Quiz Generation**: Create automatically generated multiple-choice quizzes
- **Flashcard Creation**: Build digital study flashcards from lecture content
- **Concept Extraction**: Identify and extract key concepts automatically
- **Multi-language Support**: Process content in 5+ languages

## Tech Stack

- **Frontend**: Streamlit
- **AI Services**: Groq API or Google Gemini
- **Audio Processing**: Whisper AI
- **Backend**: Python 3.9+
- **Database**: Firebase (optional)

## Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager
- Virtual environment (recommended)

### Setup Steps

1. Clone the repository:
```bash
git clone <repository-url>
cd lecture-voice-notes
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

5. Run the application:
```bash
streamlit run app.py
```

## Configuration

### API Keys

Set up your API keys in `.env` file:

```
GROQ_API_KEY=your_groq_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

Get API keys from:
- Groq: https://console.groq.com/
- Google: https://aistudio.google.com/app/apikey

### Application Settings

Access settings through the sidebar to configure:
- Reading level (Beginner to Expert)
- Preferred tone (Professional, Casual, Academic, Conversational)
- Language preference
- Quiz difficulty level

## Usage

1. **Upload Audio**: Select an audio file (MP3, WAV, M4A, OGG, WEBM, FLAC)
2. **Transcribe**: Click "Start Transcription" to convert audio to text
3. **Generate Materials**: Use study materials tab to create summaries, quizzes, and flashcards
4. **Study**: Use the generated materials in the Quiz and Flashcards sections

## Project Structure

```
lecture-voice-notes/
├── app.py                  # Main Streamlit application
├── config/
│   ├── settings.py         # Configuration settings
│   └── __init__.py
├── services/
│   ├── ai.py              # AI service integration
│   ├── audio_processor.py # Audio file processing
│   ├── speech_to_text.py  # Transcription service
│   ├── firebase_service.py # Database integration
│   └── __init__.py
├── utils/
│   ├── formatters.py      # Data formatting utilities
│   ├── helpers.py         # Helper functions
│   ├── validators.py      # Input validation
│   └── __init__.py
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## Supported Audio Formats

- MP3
- WAV
- M4A
- OGG
- WEBM
- FLAC


## Troubleshooting

### Audio Upload Issues
- Ensure file size is under 25MB
- Check file format is supported
- Verify audio quality is clear

### API Errors
- Confirm API keys are correctly set in .env
- Check internet connection
- Verify API quota has not been exceeded

### Transcription Quality
- Use high-quality audio recordings
- Minimize background noise
- Ensure clear speaker audio

## Performance Notes

- Transcription time varies based on audio length
- AI generation depends on content complexity
- Larger files may take longer to process

## Security

- API keys are stored locally in .env (not committed to git)
- .gitignore prevents credential exposure
- No data is permanently stored in the cloud

## Limitations

- Free API tiers have rate limits
- Maximum audio file size depends on service provider
- Processing time increases with content length

## Future Enhancements

- Real-time audio recording
- Cloud storage integration
- Batch processing capabilities
- Export to multiple formats (PDF, DOCX)
- Collaborative features

## Acknowledgments

- Groq for fast AI inference
- Google for Gemini API
- OpenAI for Whisper technology
- Streamlit for web framework


