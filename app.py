# -*- coding: utf-8 -*-
"""
Lecture Voice-to-Notes Generator

A professional application that converts lecture audio recordings into 
comprehensive study materials using AI technology.

Main Features:
- Audio transcription with multi-language support
- AI-powered content summarization
- Automatic quiz generation
- Digital flashcard creation
- Key concept extraction
"""

import streamlit as st
import os
import sys
import tempfile
import json
from datetime import datetime

# Custom imports
from config.settings import settings
from services.speech_to_text import transcribe_audio
from services.ai import AIService
from services.audio_processor import AudioProcessor
from utils.validators import Validators
from utils.formatters import Formatters
from utils.helpers import FileHelpers, StringHelpers

# Page Configuration
st.set_page_config(
    page_title=settings.PAGE_TITLE,
    page_icon=settings.PAGE_ICON,
    layout=settings.LAYOUT,
    initial_sidebar_state=settings.INITIAL_SIDEBAR_STATE,
)

# Custom CSS for better UI
st.markdown("""
    <style>
    :root {
        --primary-color: #001f3f;
        --secondary-color: #0066cc;
        --accent-color: #667eea;
        --success-color: #28a745;
        --error-color: #dc3545;
        --warning-color: #ffc107;
        --info-color: #17a2b8;
    }
    
    .main {
        background-color: #f5f7fa;
        color: #1a1a1a;
    }
    
    /* Tab styling - matching header */
    .stTabs [data-baseweb="tab-list"] button {
        background-color: #ffffff;
        color: #001f3f;
        border: 2px solid #e0e6f2;
        border-radius: 10px;
        font-weight: 700;
        padding: 12px 24px;
        transition: all 0.3s ease;
        letter-spacing: 0.3px;
        font-size: 14px;
        text-transform: uppercase;
    }
    
    .stTabs [data-baseweb="tab-list"] button:hover {
        border-color: #0066cc;
        color: #0066cc;
        box-shadow: 0 4px 12px rgba(0, 102, 204, 0.2);
        transform: translateY(-2px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #001f3f 0%, #003d7a 100%) !important;
        color: white !important;
        border-color: #0066cc !important;
        box-shadow: 0 4px 12px rgba(0, 102, 204, 0.4) !important;
        font-weight: 800 !important;
    }
    
    .stTabs [aria-selected="true"] span {
        color: white !important;
        font-weight: 800 !important;
    }
    
    .stTabs [aria-selected="true"] div {
        color: white !important;
        font-weight: 800 !important;
    }
    
    .stTabs [aria-selected="true"] p {
        color: white !important;
        font-weight: 800 !important;
    }
    
    button[role="tab"][aria-selected="true"] {
        color: white !important;
        font-weight: 800 !important;
    }
    
    button[role="tab"][aria-selected="true"] * {
        color: white !important;
        font-weight: 800 !important;
    }
    
    /* Headings - matching header style */
    h1 {
        color: #001f3f;
        text-align: center;
        font-weight: 800;
        font-size: 32px;
        margin-bottom: 24px;
        letter-spacing: 0.5px;
        font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
        text-shadow: none;
    }
    
    h2 {
        color: #001f3f;
        border-bottom: 3px solid #0066cc;
        padding-bottom: 12px;
        font-weight: 800;
        font-size: 22px;
        letter-spacing: 0.3px;
        margin-top: 20px;
        margin-bottom: 16px;
    }
    
    h3 {
        color: #0066cc;
        font-weight: 700;
        font-size: 16px;
        letter-spacing: 0.2px;
    }
    
    /* Text visibility */
    p, .stText, label {
        color: #1a1a1a !important;
        font-weight: 500;
        font-size: 14px;
    }
    
    /* Content sections */
    .section-box {
        background-color: #ffffff;
        border: 2px solid #e0e6f2;
        border-radius: 10px;
        padding: 20px;
        margin: 16px 0;
        box-shadow: 0 2px 8px rgba(0, 31, 63, 0.08);
    }
    
    .section-box:hover {
        box-shadow: 0 4px 16px rgba(0, 31, 63, 0.12);
        border-color: #0066cc;
    }
    
    /* Transcript box - prominent border */
    .transcript-box {
        background: linear-gradient(135deg, #f0f4ff 0%, #f8f9fb 100%);
        border: 3px solid #0066cc;
        border-radius: 12px;
        padding: 24px;
        margin: 16px 0;
        font-family: 'Segoe UI', 'Courier New', monospace;
        font-size: 15px;
        line-height: 2;
        color: #001f3f;
        white-space: pre-wrap;
        word-wrap: break-word;
        box-shadow: 0 4px 16px rgba(0, 102, 204, 0.15);
        letter-spacing: 0.3px;
        font-weight: 500;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #001f3f 0%, #0066cc 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 12px rgba(0, 31, 63, 0.2);
        border: 2px solid #0066cc;
    }
    
    /* Input fields */
    .stTextInput, .stTextArea, .stSelectbox, .stSlider, .stFileUploader {
        background-color: #ffffff;
        border: 2px solid #e0e6f2 !important;
        border-radius: 8px;
    }
    
    .stTextInput input, .stTextArea textarea {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #e0e6f2 !important;
        font-size: 14px !important;
    }
    
    .stTextArea textarea {
        font-family: 'Courier New', monospace !important;
        line-height: 1.8 !important;
    }
    
    .stTextArea label {
        color: #001f3f !important;
        font-weight: 700;
        font-size: 14px;
    }
    
    /* Button styling - header gradient - ONLY for action buttons */
    .stButton > button {
        background: linear-gradient(135deg, #001f3f 0%, #0066cc 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 800 !important;
        padding: 12px 24px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(0, 31, 63, 0.2) !important;
        letter-spacing: 0.3px !important;
        font-size: 14px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 6px 20px rgba(0, 102, 204, 0.4) !important;
    }
    
    .stButton > button div, .stButton > button span, .stButton > button p {
        color: white !important;
        font-weight: 800 !important;
    }
    
    /* Exclude file uploader, close buttons, and 3dots menu */
    [data-testid="fileUploadDropzone"] button,
    [data-testid="stFileUploadDropzone"] button,
    .stFileUploader button {
        background: auto !important;
        color: auto !important;
        font-weight: auto !important;
    }
    
    [data-testid="stFileUploadDropzone"] button div,
    [data-testid="stFileUploadDropzone"] button span {
        color: auto !important;
        font-weight: auto !important;
    }
    
    /* Expander */
    .streamlit-expander {
        border: 2px solid #e0e6f2;
        border-radius: 8px;
        background-color: #ffffff;
    }
    
    /* Metric styling */
    .stMetric {
        background-color: #ffffff;
        padding: 16px;
        border-radius: 8px;
        border: 2px solid #e0e6f2;
        border-left: 4px solid #0066cc;
        box-shadow: 0 2px 6px rgba(0, 31, 63, 0.08);
    }
    
    .stMetric label {
        color: #001f3f !important;
        font-weight: 700;
        font-size: 12px;
    }
    
    .stMetric [data-testid="metric-container"] {
        background: transparent;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #001f3f 0%, #0066cc 100%);
    }
    
    /* Sidebar improvements */
    .stSidebar {
        background: linear-gradient(135deg, #001f3f 0%, #0066cc 100%);
        border-right: 3px solid #0066cc;
    }
    
    .stSidebar h2, .stSidebar h3 {
        color: #ffffff !important;
        font-weight: 800;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    
    .stSidebar h2 {
        font-size: 18px;
        margin-bottom: 4px;
    }
    
    .stSidebar h3 {
        font-size: 14px;
        margin-top: 12px;
        margin-bottom: 8px;
    }
    
    .stSidebar [data-testid="stMarkdownContainer"] h2,
    .stSidebar [data-testid="stMarkdownContainer"] h3 {
        color: #ffffff !important;
    }
    
    .stSidebar strong {
        color: #ffffff;
        font-size: 13px;
        font-weight: 700;
        display: block;
        margin: 8px 0 6px 0;
        letter-spacing: 0.2px;
        line-height: 1;
    }
    
    .stSidebar p {
        color: #ffffff !important;
        margin: 4px 0 !important;
        line-height: 1.6;
    }
    
    .stSidebar [data-testid="stMarkdownContainer"] {
        color: #ffffff;
        line-height: 1.6;
    }
    
    .stSidebar .stSelectbox {
        margin-top: -8px !important;
        margin-bottom: 12px !important;
    }
    
    .stSidebar .stSelectbox select {
        background-color: rgba(255, 255, 255, 0.98) !important;
        color: #001f3f !important;
        border: 2px solid #ffffff !important;
        border-radius: 6px !important;
        font-weight: 600;
        font-size: 13px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
    }
    
    .stSidebar .stSelectbox select:hover {
        border-color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25) !important;
    }
    
    .stSidebar hr {
        border-color: rgba(255, 255, 255, 0.4);
        margin: 12px 0;
    }
    
    .stSidebar .stExpander {
        background: rgba(255, 255, 255, 0.96) !important;
        border: 2px solid rgba(255, 255, 255, 0.8) !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
        margin-top: 8px;
    }
    
    .stSidebar .stExpander [data-testid="stExpanderDetails"] {
        background: rgba(255, 255, 255, 0.98) !important;
        border-top: 1px solid rgba(0, 102, 204, 0.2) !important;
    }
    
    .stSidebar [data-testid="stExpander"] button {
        color: #001f3f !important;
        font-weight: 700 !important;
    }
    
    .stSidebar [data-testid="stExpander"] button span {
        color: #001f3f !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if "transcript" not in st.session_state:
        st.session_state.transcript = ""
    if "summary" not in st.session_state:
        st.session_state.summary = ""
    if "quiz" not in st.session_state:
        st.session_state.quiz = []
    if "flashcards" not in st.session_state:
        st.session_state.flashcards = []
    if "concepts" not in st.session_state:
        st.session_state.concepts = {}
    if "tone_analysis" not in st.session_state:
        st.session_state.tone_analysis = {}
    if "user_id" not in st.session_state:
        st.session_state.user_id = f"user_{datetime.now().timestamp()}"
    
    # UI control flags
    if "show_summary" not in st.session_state:
        st.session_state.show_summary = False
    if "show_concepts" not in st.session_state:
        st.session_state.show_concepts = False
    if "show_tone" not in st.session_state:
        st.session_state.show_tone = False
    if "show_all_cards" not in st.session_state:
        st.session_state.show_all_cards = False
    if "current_card" not in st.session_state:
        st.session_state.current_card = 0
    if "flipped" not in st.session_state:
        st.session_state.flipped = False
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False

init_session_state()

# Header with custom styling
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown("""
        <div style="margin-top: -30px; margin-bottom: 0px;">
            <h1 style="color: #001f3f; margin: 0; padding: 0; font-size: 36px; font-weight: 800; letter-spacing: 0.5px; text-align: center; font-family: 'Segoe UI', 'Helvetica Neue', sans-serif; text-transform: uppercase; tracking: 2px;">🎙️ Lecture Voice-to-Notes Generator</h1>
            <h3 style="color: #0066cc; margin-top: 8px; text-align: center; font-weight: 600; font-size: 16px; letter-spacing: 1px; font-style: italic;">Convert Lectures into Study Materials with AI</h3>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Sidebar Configuration
with st.sidebar:
    st.markdown('<h3 style="color: #000a2e; margin: 0; font-size: 18px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px;">⚙️ SETTINGS & CONFIGURATION</h3>', unsafe_allow_html=True)
    
    # Settings Box using expander
    with st.expander("⚙️ Select Your Settings", expanded=True):
        st.markdown("**📖 Reading Level**", unsafe_allow_html=True)
        reading_level = st.selectbox(
            "📖 Reading Level",
            ["Beginner", "Intermediate", "Advanced", "Expert"],
            index=1,
            label_visibility="collapsed",
            key="reading_level"
        )
        
        st.markdown("**🎭 Preferred Tone**", unsafe_allow_html=True)
        tone = st.selectbox(
            "🎭 Preferred Tone",
            ["Professional", "Casual", "Academic", "Conversational"],
            index=0,
            label_visibility="collapsed",
            key="tone_select"
        )
        
        st.markdown("**🌐 Language**", unsafe_allow_html=True)
        selected_language = st.selectbox(
            "🌐 Language",
            ["English", "Spanish", "French", "German", "Chinese"],
            index=0,
            label_visibility="collapsed",
            key="language_select"
        )
        
        st.markdown("**📊 Quiz Difficulty**", unsafe_allow_html=True)
        difficulty = st.selectbox(
            "📊 Quiz Difficulty",
            ["Easy", "Medium", "Hard"],
            index=1,
            label_visibility="collapsed",
            key="difficulty_select"
        )
    
    st.markdown('<h3 style="color: #000a2e; margin: 12px 0 0 0; font-size: 18px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px;">📋 ABOUT THIS PROJECT</h3>', unsafe_allow_html=True)
    
    with st.expander("📌 Key Features", expanded=True):
        st.markdown("""
        🎙️ **Transcribe** - Convert lectures to text instantly
        
        📝 **Summarize** - AI-powered summaries & notes
        
        ❓ **Quiz** - Auto-generated quiz questions
        
        📇 **Flashcards** - Create study flashcards
        
        🔍 **Concepts** - Extract key concepts automatically
        """)

# Main Content Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📝 Transcribe", "📚 Study Materials", "❓ Quiz", "📇 Flashcards", "💾 Library"]
)

# TAB 1: TRANSCRIPTION
with tab1:
    st.markdown("## 🎙️ Audio Transcription")
    st.markdown("Upload or record your lecture to convert it to text")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Upload Audio File")
        audio_file = st.file_uploader(
            "Choose audio file",
            type=["mp3", "wav", "m4a", "ogg", "webm", "flac"],
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown("### 🎤 Record Live")
        st.info("💡 Tip: Use your phone or computer to record and upload")
    
    if audio_file:
        st.success(f"✅ File uploaded: {audio_file.name}")
        
        # Save temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_file.getbuffer())
            temp_path = tmp_file.name
        
        # Show audio stats
        try:
            stats = AudioProcessor.get_audio_stats(temp_path)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Duration", Formatters.format_duration(stats['duration_seconds']))
            with col2:
                st.metric("Sample Rate", f"{stats['sample_rate']} Hz")
            with col3:
                st.metric("Audio Quality", "Clear ✓" if stats['max_amplitude'] > 0.1 else "Low ⚠️")
        except:
            pass
        
        # Transcription Button
        if st.button("🚀 Start Transcription", key="transcribe_btn", use_container_width=True):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("🔄 Converting audio...")
            progress_bar.progress(30)
            
            try:
                # Convert to WAV if needed
                wav_path = AudioProcessor.convert_to_wav(temp_path)
                
                status_text.text("🤖 Transcribing with AI...")
                progress_bar.progress(60)
                
                # Transcribe
                result = transcribe_audio(wav_path, language=selected_language, use_local=True)
                
                if result["success"]:
                    st.session_state.transcript = result["text"]
                    progress_bar.progress(100)
                    status_text.empty()
                    
                    st.markdown('<div class="success-box">✅ Transcription Complete! Scroll down to see full transcript.</div>', unsafe_allow_html=True)
                    
                    # Quick stats
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Words", StringHelpers.count_words(st.session_state.transcript))
                    with col2:
                        st.metric("Duration", Formatters.estimate_reading_time(st.session_state.transcript))
                    with col3:
                        st.metric("Sentences", StringHelpers.count_sentences(st.session_state.transcript))
                
                else:
                    st.markdown(f'<div class="error-box">❌ Error: {result.get("error", "Unknown error")}</div>', unsafe_allow_html=True)
            
            except Exception as e:
                st.markdown(f'<div class="error-box">❌ Error: {str(e)}</div>', unsafe_allow_html=True)
            
            finally:
                # Cleanup
                try:
                    os.remove(temp_path)
                except:
                    pass
    
    # ALWAYS show transcript if it exists (persistent display)
    if st.session_state.transcript:
        st.markdown("### 📋 Your Transcript", unsafe_allow_html=True)
        st.markdown(f'<div class="transcript-box">{st.session_state.transcript}</div>', unsafe_allow_html=True)
        
        # Download and stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Words", StringHelpers.count_words(st.session_state.transcript))
        with col2:
            st.metric("Sentences", StringHelpers.count_sentences(st.session_state.transcript))
        with col3:
            st.metric("Reading Time", Formatters.estimate_reading_time(st.session_state.transcript))
        with col4:
            st.metric("Characters", len(st.session_state.transcript))
        
        # Download options
        st.markdown("### 💾 Download Options")
        col1, col2 = st.columns(2)
        with col1:
            txt_data = st.session_state.transcript.encode('utf-8')
            st.download_button(
                "📥 Download as TXT",
                txt_data,
                "transcript.txt",
                "text/plain"
            )
        with col2:
            st.info("💡 Use Study Materials tab to export as PDF/DOCX")

# TAB 2: STUDY MATERIALS
with tab2:
    st.markdown("## 📚 AI-Generated Study Materials")
    
    if not st.session_state.transcript:
        st.markdown('<div class="section-box" style="background-color: #e3f2fd; border-left: 4px solid #0066cc;"><strong style="color: #0066cc;">ℹ️ Please transcribe an audio file first in the Transcribe tab</strong></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="section-box" style="border-left: 4px solid #28a745;"><strong style="color: #28a745;">✅ Ready to process {StringHelpers.count_words(st.session_state.transcript)} words</strong></div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        # Generate Summary
        with col1:
            if st.button("📝 Generate Summary", use_container_width=True, key="gen_summary"):
                # Hide other sections
                st.session_state.show_concepts = False
                st.session_state.show_tone = False
                
                with st.spinner("⏳ Generating summary..."):
                    try:
                        ai = AIService()
                        result = ai.generate_summary(
                            st.session_state.transcript,
                            reading_level=reading_level,
                            tone=tone
                        )
                        
                        if result["success"]:
                            st.session_state.summary = result["summary"]
                            st.session_state.show_summary = True
                            st.success("✅ Summary generated!")
                        else:
                            st.error(f"Error: {result.get('error')}")
                    
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        # Extract Concepts
        with col2:
            if st.button("🔍 Extract Concepts", use_container_width=True, key="gen_concepts"):
                # Hide other sections
                st.session_state.show_summary = False
                st.session_state.show_tone = False
                
                with st.spinner("⏳ Extracting concepts..."):
                    try:
                        ai = AIService()
                        result = ai.extract_key_concepts(st.session_state.transcript)
                        
                        if result["success"]:
                            st.session_state.concepts = result["concepts"]
                            st.session_state.show_concepts = True
                            st.success("✅ Concepts extracted!")
                        else:
                            st.error(f"Error: {result.get('error')}")
                    
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        # Analyze Tone
        with col3:
            if st.button("🎭 Analyze Tone", use_container_width=True, key="gen_tone"):
                # Hide other sections
                st.session_state.show_summary = False
                st.session_state.show_concepts = False
                
                with st.spinner("⏳ Analyzing tone..."):
                    try:
                        ai = AIService()
                        result = ai.analyze_tone(st.session_state.transcript)
                        
                        if result["success"]:
                            st.session_state.tone_analysis = result["analysis"]
                            st.session_state.show_tone = True
                            st.success("✅ Tone analyzed!")
                        else:
                            st.error(f"Error: {result.get('error')}")
                    
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        # Display ONLY Summary if generated
        if st.session_state.get("show_summary") and st.session_state.summary:
            st.markdown("---")
            st.markdown("### 📝 Generated Summary")
            st.markdown(f'<div class="section-box">{st.session_state.summary}</div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.download_button(
                    "📥 Download Summary",
                    st.session_state.summary,
                    "summary.txt",
                    key="dl_summary"
                )
            with col2:
                if st.button("💾 Save to Library", key="save_summary"):
                    st.success("✅ Saved to library!")
            with col3:
                if st.button("❌ Clear", key="clear_summary"):
                    st.session_state.show_summary = False
                    st.rerun()
        
        # Display ONLY Concepts if generated
        if st.session_state.get("show_concepts") and st.session_state.concepts:
            st.markdown("---")
            st.markdown("### 🔍 Extracted Key Concepts")
            concepts_data = st.session_state.concepts
            
            if "main_topics" in concepts_data:
                st.markdown("**📌 Main Topics:**")
                for topic in concepts_data["main_topics"]:
                    st.write(f"• {topic}")
            
            if "key_concepts" in concepts_data:
                st.markdown("**💡 Key Concepts:**")
                for concept in concepts_data["key_concepts"]:
                    st.write(f"• {concept}")
            
            if "important_points" in concepts_data:
                st.markdown("**⭐ Important Points:**")
                for point in concepts_data["important_points"]:
                    st.write(f"• {point}")
            
            if "technical_terms" in concepts_data:
                st.markdown("**🔬 Technical Terms:**")
                terms = concepts_data["technical_terms"]
                for term, definition in terms.items():
                    st.write(f"**{term}:** {definition}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("💾 Save to Library", key="save_concepts"):
                    st.success("✅ Saved to library!")
            with col2:
                st.write("")  # Spacing
            with col3:
                if st.button("❌ Clear", key="clear_concepts"):
                    st.session_state.show_concepts = False
                    st.rerun()
        
        # Display ONLY Tone Analysis if generated
        if st.session_state.get("show_tone") and st.session_state.get("tone_analysis"):
            st.markdown("---")
            st.markdown("### 🎭 Tone Analysis")
            analysis = st.session_state.tone_analysis
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Detected Tone", analysis.get("detected_tone", "N/A"))
            with col2:
                st.metric("Formality", f"{analysis.get('formality_level', 0)}/10")
            with col3:
                st.metric("Technical", f"{analysis.get('technical_level', 0)}/10")
            with col4:
                st.metric("Sentiment", analysis.get("sentiment", "N/A"))
            
            st.info(f"📍 **Audience:** {analysis.get('primary_audience', 'General')}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("💾 Save to Library", key="save_tone"):
                    st.success("✅ Saved to library!")
            with col2:
                st.write("")  # Spacing
            with col3:
                if st.button("❌ Clear", key="clear_tone"):
                    st.session_state.show_tone = False
                    st.rerun()

# TAB 3: QUIZ
with tab3:
    st.markdown("## ❓ Interactive Quiz")
    
    if not st.session_state.transcript:
        st.markdown('<div class="section-box" style="background-color: #e3f2fd; border-left: 4px solid #0066cc;"><strong style="color: #0066cc;">ℹ️ Please transcribe an audio file first</strong></div>', unsafe_allow_html=True)
    else:
        if not st.session_state.quiz:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                num_questions = st.slider("Number of questions:", 1, 20, 5)
            with col2:
                if st.button("🎯 Generate Quiz", use_container_width=True):
                    with st.spinner("⏳ Generating quiz..."):
                        try:
                            ai = AIService()
                            result = ai.generate_quiz(
                                st.session_state.transcript,
                                num_questions=num_questions,
                                difficulty=difficulty
                            )
                            
                            if result["success"]:
                                st.session_state.quiz = result["questions"]
                                st.rerun()
                            else:
                                st.error(f"Error: {result.get('error')}")
                        
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
        
        if st.session_state.quiz:
            st.markdown("---")
            st.markdown("### 🎯 Take the Quiz")
            
            # Initialize answer tracking
            if "quiz_answers" not in st.session_state:
                st.session_state.quiz_answers = {}
            if "quiz_submitted" not in st.session_state:
                st.session_state.quiz_submitted = False
            
            # Display questions with radio buttons
            for idx, question in enumerate(st.session_state.quiz, 1):
                st.markdown(f"#### Question {idx}: {question['question']}")
                
                user_answer = st.radio(
                    "Select your answer:",
                    options=question['options'],
                    key=f"q_{idx}",
                    label_visibility="collapsed"
                )
                
                # Store answer
                st.session_state.quiz_answers[idx] = user_answer
                st.markdown("---")
            
            # Submit Button
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("✅ Submit Quiz", use_container_width=True, key="submit_quiz"):
                    st.session_state.quiz_submitted = True
                    st.rerun()
            
            # Show results if submitted
            if st.session_state.quiz_submitted:
                st.markdown("---")
                st.markdown("## 📊 Quiz Results")
                
                correct_count = 0
                for idx, question in enumerate(st.session_state.quiz, 1):
                    if idx in st.session_state.quiz_answers:
                        user_answer = st.session_state.quiz_answers[idx]
                        correct_idx = question['correct_answer']
                        if user_answer == question['options'][correct_idx]:
                            correct_count += 1
                
                # Calculate percentage
                total_questions = len(st.session_state.quiz)
                percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0
                
                # Display metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Score", f"{correct_count}/{total_questions}")
                with col2:
                    st.metric("Percentage", f"{percentage:.1f}%")
                with col3:
                    if percentage >= 80:
                        status = "🌟 Excellent"
                    elif percentage >= 60:
                        status = "✅ Good"
                    else:
                        status = "📚 Needs Review"
                    st.metric("Performance", status)
                
                # Show detailed results
                st.markdown("---")
                st.markdown("### 📝 Detailed Results")
                
                for idx, question in enumerate(st.session_state.quiz, 1):
                    user_answer = st.session_state.quiz_answers.get(idx)
                    correct_idx = question['correct_answer']
                    correct_answer = question['options'][correct_idx]
                    
                    if user_answer == correct_answer:
                        st.success(f"✅ Q{idx}: Correct!")
                    else:
                        st.error(f"❌ Q{idx}: Your answer: {user_answer}")
                        st.info(f"📌 Correct answer: {correct_answer}")
                    
                    if "explanation" in question:
                        st.markdown(f"💡 **Explanation:** {question['explanation']}")
                    st.markdown("---")
                
                # Retake Quiz Button
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    if st.button("🔄 Retake Test", use_container_width=True, key="retake_quiz"):
                        st.session_state.quiz = []
                        st.session_state.quiz_answers = {}
                        st.session_state.quiz_submitted = False
                        st.rerun()

# TAB 4: FLASHCARDS
with tab4:
    st.markdown("## 📇 Flashcard Study Dashboard")
    
    if not st.session_state.transcript:
        st.markdown('<div class="section-box" style="background-color: #e3f2fd; border-left: 4px solid #0066cc;"><strong style="color: #0066cc;">ℹ️ Please transcribe an audio file first</strong></div>', unsafe_allow_html=True)
    else:
        if not st.session_state.flashcards:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                num_cards = st.slider("Number of flashcards:", 1, 20, 10)
            with col2:
                if st.button("🎴 Generate Flashcards", use_container_width=True, key="gen_flashcards"):
                    with st.spinner("⏳ Generating flashcards..."):
                        try:
                            ai = AIService()
                            result = ai.generate_flashcards(
                                st.session_state.transcript,
                                num_cards=num_cards
                            )
                            
                            if result["success"]:
                                st.session_state.flashcards = result["flashcards"]
                                st.session_state.current_card = 0
                                st.session_state.flipped = False
                                st.rerun()
                            else:
                                st.error(f"Error: {result.get('error')}")
                        
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
        
        if st.session_state.flashcards:
            st.markdown("---")
            
            total_cards = len(st.session_state.flashcards)
            current_idx = st.session_state.current_card
            card = st.session_state.flashcards[current_idx]
            
            # Progress bar
            progress = (current_idx + 1) / total_cards
            st.progress(progress)
            st.markdown(f"**Progress:** Card {current_idx + 1} of {total_cards}")
            
            # Flashcard display
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 3, 1])
            
            with col2:
                flashcard_html = f"""
                <div style="
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-radius: 15px;
                    padding: 40px;
                    text-align: center;
                    color: white;
                    font-size: 18px;
                    min-height: 250px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4);
                    cursor: pointer;
                    transition: all 0.3s ease;
                ">
                    <div style="font-size: 14px; margin-bottom: 20px; opacity: 0.9;">
                        {'🔤 QUESTION' if not st.session_state.flipped else '📖 ANSWER'}
                    </div>
                    <div style="font-size: 20px; font-weight: 600;">
                        {card.get('answer') if st.session_state.flipped else card.get('question')}
                    </div>
                    <div style="font-size: 12px; margin-top: 20px; opacity: 0.8;">
                        Click "Flip Card" to toggle
                    </div>
                </div>
                """
                st.markdown(flashcard_html, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Flip button
            col1, col2, col3 = st.columns(3)
            with col2:
                if st.button("🔄 Flip Card", use_container_width=True, key="flip_card"):
                    st.session_state.flipped = not st.session_state.flipped
                    st.rerun()
            
            st.markdown("---")
            
            # Navigation buttons
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("⬅️ Previous", use_container_width=True, key="prev_card"):
                    if current_idx > 0:
                        st.session_state.current_card -= 1
                        st.session_state.flipped = False
                        st.rerun()
                    else:
                        st.warning("Already at first card")
            
            with col2:
                st.metric("Current", f"{current_idx + 1}/{total_cards}")
            
            with col3:
                st.write("")  # Spacing
            
            with col4:
                if st.button("Next ➡️", use_container_width=True, key="next_card"):
                    if current_idx < total_cards - 1:
                        st.session_state.current_card += 1
                        st.session_state.flipped = False
                        st.rerun()
                    else:
                        st.warning("Already at last card")
            
            st.markdown("---")
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("💾 Save Deck to Library", use_container_width=True):
                    st.success("✅ Deck saved to library!")
            with col2:
                if st.button("📊 View All Cards", use_container_width=True):
                    st.session_state.show_all_cards = True
            with col3:
                if st.button("🔄 Regenerate Deck", use_container_width=True):
                    st.session_state.flashcards = []
                    st.session_state.current_card = 0
                    st.rerun()
            
            # Show all cards view
            if st.session_state.get("show_all_cards"):
                st.markdown("---")
                st.markdown("### 📋 All Flashcards in Deck")
                
                for idx, fc in enumerate(st.session_state.flashcards, 1):
                    with st.expander(f"Card {idx}: {fc['question'][:50]}..."):
                        st.write(f"**Question:** {fc['question']}")
                        st.write(f"**Answer:** {fc['answer']}")

# TAB 5: LIBRARY
with tab5:
    st.markdown("## 💾 Study Library & Dashboard")
    
    # Stats Dashboard
    st.markdown("### 📊 Session Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        transcript_words = StringHelpers.count_words(st.session_state.transcript) if st.session_state.transcript else 0
        st.metric("📝 Transcript", f"{transcript_words} words")
    
    with col2:
        quiz_count = len(st.session_state.quiz) if st.session_state.quiz else 0
        st.metric("❓ Quiz Questions", quiz_count)
    
    with col3:
        flashcard_count = len(st.session_state.flashcards) if st.session_state.flashcards else 0
        st.metric("📇 Flashcards", flashcard_count)
    
    with col4:
        has_summary = "✅" if st.session_state.summary else "❌"
        st.metric("📚 Summary", has_summary)
    
    st.markdown("---")
    
    # Sections with better UI
    st.markdown("### 📥 Your Session Data")
    
    # Transcript section
    if st.session_state.transcript:
        with st.expander("📄 **Transcript** - Full text of your lecture", expanded=False):
            st.markdown(f'<div class="transcript-box">{st.session_state.transcript}</div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.download_button(
                    "📥 Download as TXT",
                    st.session_state.transcript,
                    "transcript.txt",
                    key="dl_transcript"
                )
            with col2:
                st.metric("Characters", len(st.session_state.transcript))
            with col3:
                st.metric("Sentences", StringHelpers.count_sentences(st.session_state.transcript))
    else:
        st.info("📌 No transcript yet. Upload and transcribe an audio file to get started!")
    
    # Summary section
    if st.session_state.summary:
        with st.expander("📝 **Summary** - AI-generated overview", expanded=False):
            st.markdown(f'<div class="section-box">{st.session_state.summary}</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    "📥 Download Summary",
                    st.session_state.summary,
                    "summary.txt",
                    key="dl_summary_lib"
                )
            with col2:
                st.metric("Words", StringHelpers.count_words(st.session_state.summary))
    
    # Concepts section
    if st.session_state.concepts:
        with st.expander("🔍 **Concepts** - Extracted key points", expanded=False):
            concepts_data = st.session_state.concepts
            
            if "main_topics" in concepts_data:
                st.markdown("**📌 Main Topics:**")
                for topic in concepts_data["main_topics"]:
                    st.write(f"• {topic}")
            
            if "key_concepts" in concepts_data:
                st.markdown("**💡 Key Concepts:**")
                for concept in concepts_data["key_concepts"]:
                    st.write(f"• {concept}")
            
            if "technical_terms" in concepts_data:
                st.markdown("**🔬 Technical Terms:**")
                terms = concepts_data["technical_terms"]
                for term, definition in terms.items():
                    st.write(f"• **{term}:** {definition}")
    
    # Quiz section
    if st.session_state.quiz:
        with st.expander(f"❓ **Quiz** - {len(st.session_state.quiz)} questions", expanded=False):
            for idx, q in enumerate(st.session_state.quiz, 1):
                st.markdown(f"**Q{idx}:** {q['question']}")
                st.write(f"Options: {', '.join(q['options'])}")
                st.write(f"Correct Answer: {q['options'][q['correct_answer']]}")
                if "explanation" in q:
                    st.info(f"💡 {q['explanation']}")
                st.markdown("---")
    
    # Flashcards section
    if st.session_state.flashcards:
        with st.expander(f"📇 **Flashcards** - {len(st.session_state.flashcards)} cards", expanded=False):
            for idx, card in enumerate(st.session_state.flashcards, 1):
                st.markdown(f"**Card {idx}**: {card.get('question', 'Q')[:80]}...")
                st.write(f"**Question:** {card.get('question')}")
                st.write(f"**Answer:** {card.get('answer')}")
                st.divider()
    
    st.markdown("---")
    
    # Export & Actions
    st.markdown("### 📤 Export & Share")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📋 Export All as Text", use_container_width=True):
            all_data = f"""
LECTURE STUDY MATERIALS EXPORT
================================
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

TRANSCRIPT
----------
{st.session_state.transcript or 'No transcript'}

SUMMARY
-------
{st.session_state.summary or 'No summary'}

CONCEPTS
--------
{json.dumps(st.session_state.concepts, indent=2) if st.session_state.concepts else 'No concepts'}
            """
            st.download_button(
                "📥 Download Export",
                all_data,
                "lecture_export.txt",
                key="export_all"
            )
    
    with col2:
        if st.button("🗑️ Clear All Session Data", use_container_width=True):
            st.session_state.transcript = ""
            st.session_state.summary = ""
            st.session_state.concepts = {}
            st.session_state.quiz = []
            st.session_state.flashcards = []
            st.session_state.show_summary = False
            st.session_state.show_concepts = False
            st.session_state.show_tone = False
            st.markdown('<div class="section-box" style="background-color: #d4edda; border-left: 4px solid #28a745;"><strong style="color: #28a745;">✅ All session data cleared!</strong></div>', unsafe_allow_html=True)
            st.rerun()
    
    with col3:
        if st.button("ℹ️ About This App", use_container_width=True):
            st.markdown("""
            <div class="section-box">
            <strong style="color: #001f3f; font-size: 16px;">Lecture Voice-to-Notes Generator</strong><br><br>
            Advanced lecture processing system featuring:<br>
            • Speech-to-Text transcription with AI<br>
            • Automated content generation and summarization<br>
            • Concept extraction and analysis<br>
            • Interactive quiz and flashcard creation<br><br>
            Transform your lectures into comprehensive, organized study materials.
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; font-size: 12px;">
    🎓 Lecture Voice-to-Notes Generator
    </div>
""", unsafe_allow_html=True)
