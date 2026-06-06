---
title: Lecture Voice-to-Notes Generator
emoji: 🎙️
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: 1.28.1
app_file: app.py
pinned: false
---

# Voice-to-Notes Generator

An application that automatically transforms audio lectures into multiple study formats including transcripts, summaries, quizzes, flashcards, and key concepts using advanced AI technology. Simply upload your audio file and receive professionally formatted study materials instantly.

## Key Features

- **Audio Transcription**: Convert audio files to text with support for multiple formats and languages
- **Content Summarization**: Generate concise, AI-powered summaries from transcripts
- **Quiz Generation**: Create automatically generated multiple-choice quizzes
- **Flashcard Creation**: Build digital study flashcards from lecture content
- **Concept Extraction**: Identify and extract key concepts automatically

## Tech Stack

- **Frontend**: Streamlit
- **AI Services**: Groq API, Google Gemini, and OpenAI
- **Audio Processing**: OpenAI Whisper
- **Audio Libraries**: librosa, pydub
- **Backend**: Python 3.9+

## Installation

1. Clone the repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```
3. Install dependencies: `pip install -r requirements.txt`
4. Configure API keys in `.env` file
5. Run: `streamlit run app.py` or use `./app_startup.sh`


## Usage

1. Upload an audio file (MP3, WAV, M4A formats supported)
2. Select desired output formats
3. Wait for processing to complete
4. Download generated study materials

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

## Performance

- Transcription time varies based on audio length
- AI generation depends on content complexity
- Larger files may take longer to process

## Limitations

- Free API tiers have rate limits
- Maximum audio file size depends on service provider
- Processing time increases with content length

## Deployment

This application is deployed on [Hugging Face Spaces](https://huggingface.co/spaces/sheethalk/voice-to-notes-ai) for easy access without local installation.