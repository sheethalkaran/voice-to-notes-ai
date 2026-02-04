#!/bin/bash

# This file is needed for Hugging Face Spaces deployment
# It will be automatically run when your Space boots up

# Create directories
mkdir -p logs
mkdir -p cache

# Install requirements
pip install -r requirements.txt

# Download Whisper model
python -c "import whisper; whisper.load_model('base', cache_dir='./cache')"

# Run the app
streamlit run app.py --server.headless true --server.port 7860
