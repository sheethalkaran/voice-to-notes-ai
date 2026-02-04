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

## Tech Stack

- **Frontend**: Streamlit
- **AI Services**: Groq API or Google Gemini
- **Audio Processing**: Whisper AI
- **Backend**: Python 3.9+
- **Database**: Firebase (optional)


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


