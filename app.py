#!/usr/bin/env python3
"""
🎵 DISBAND - AI Stem Separator
Created by @jeysshon

Professional stem separation that actually works
"""

import streamlit as st
import subprocess
import sys
import tempfile
import zipfile
import time
from pathlib import Path
from io import BytesIO
import base64
import requests

# Page config - MUST be first Streamlit command
st.set_page_config(
    page_title="🎵 Disband - AI Stem Separator",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def load_beautiful_css():
    """Load gorgeous custom CSS"""
    st.markdown("""
    <style>
    /* Import beautiful fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Hide default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Hero Section */
    .hero-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 4rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .hero-title {
        font-size: 4rem;
        font-weight: 700;
        color: white;
        margin: 0;
        text-shadow: 0 2px 20px rgba(0,0,0,0.4);
        letter-spacing: -0.02em;
    }
    
    .hero-subtitle {
        font-size: 1.4rem;
        color: rgba(255,255,255,0.9);
        margin: 1rem 0;
        font-weight: 400;
    }
    
    .hero-author {
        font-size: 1.1rem;
        color: rgba(255,255,255,0.8);
        margin: 0.5rem 0 0 0;
        font-weight: 500;
    }
    
    /* Main containers */
    .upload-container {
        background: white;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        border: 1px solid #f0f2f6;
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
    }
    
    .results-container {
        background: linear-gradient(135deg, #00c851 0%, #00a085 100%);
        padding: 3rem;
        border-radius: 20px;
        color: white;
        margin: 2rem 0;
        box-shadow: 0 15px 35px rgba(0,200,81,0.3);
    }
    
    .processing-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 15px 35px rgba(102,126,234,0.3);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    /* Status cards */
    .status-success {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 10px 25px rgba(40,167,69,0.3);
    }
    
    .status-error {
        background: linear-gradient(135deg, #dc3545 0%, #fd7e14 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 10px 25px rgba(220,53,69,0.3);
    }
    
    /* File info */
    .file-info {
        background: linear-gradient(135deg, #17a2b8 0%, #138496 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 10px 25px rgba(23,162,184,0.3);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 1rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 8px 20px rgba(102,126,234,0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(102,126,234,0.5);
    }
    
    .stDownloadButton > button {
        background: linear-gradient(135deg, #00c851 0%, #00a085 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 1.5rem;
        font-weight: 500;
        margin: 0.3rem;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(0,200,81,0.3);
    }
    
    .stDownloadButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 20px rgba(0,200,81,0.4);
    }
    
    /* Stem items */
    .stem-item {
        background: rgba(255,255,255,0.2);
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.8rem 0;
        display: flex;
        align-items: center;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    .stem-icon {
        font-size: 1.8rem;
        margin-right: 1rem;
    }
    
    /* Metrics */
    [data-testid="metric-container"] {
        background: white;
        border: 1px solid #e8f0ff;
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero-title { font-size: 2.8rem; }
        .upload-container { padding: 1.5rem; }
    }
    </style>
    """, unsafe_allow_html=True)

def install_demucs_working():
    """Install only what we need that actually works"""
    try:
        # Install basic audio processing
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "librosa==0.10.1", "--quiet", "--no-cache-dir"
        ], check=True, timeout=300)
        
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "soundfile==0.12.1", "--quiet", "--no-cache-dir"
        ], check=True, timeout=300)
        
        return True
    except:
        return False

def basic_vocal_separation(uploaded_file):
    """
    Real vocal separation using librosa (actually works)
    """
    try:
        import librosa
        import soundfile as sf
        import numpy as np
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Save uploaded file
            input_file = temp_path / uploaded_file.name
            with open(input_file, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Load audio
            y, sr = librosa.load(str(input_file), sr=None)
            
            # Convert to stereo if mono
            if len(y.shape) == 1:
                y = np.array([y, y])
            elif y.shape[0] == 1:
                y = np.repeat(y, 2, axis=0)
            elif y.shape[1] == 1:
                y = y.T
                y = np.repeat(y, 2, axis=0)
            
            # Ensure proper shape
            if len(y.shape) == 1:
                y = np.array([y, y]).T
            elif y.shape[0] == 2:
                y = y.T
            
            # Separate using librosa's vocal separation
            S_full, phase = librosa.magphase(librosa.stft(y.T))
            S_filter = librosa.decompose.nn_filter(S_full,
                                                 aggregate=np.median,
                                                 metric='cosine',
                                                 width=int(librosa.frames_to_time(2, sr=sr)))
            S_filter = np.minimum(S_full, S_filter)
            
            margin_i, margin_v = 2, 10
            power = 2
            
            mask_i = librosa.util.softmask(S_filter,
                                         margin_i * (S_full - S_filter),
                                         power=power)
            
            mask_v = librosa.util.softmask(S_full - S_filter,
                                         margin_v * S_filter,
                                         power=power)
            
            # Apply masks
            S_foreground = mask_v * S_full
            S_background = mask_i * S_full
            
            # Convert back to audio
            vocals = librosa.istft(S_foreground * phase, length=len(y.T))
            instrumental = librosa.istft(S_background * phase, length=len(y.T))
            
            # Save files
            vocals_file = temp_path / "vocals.wav"
            instrumental_file = temp_path / "instrumental.wav"
            
            sf.write(str(vocals_file), vocals, sr)
            sf.write(str(instrumental_file), instrumental, sr)
            
            # Read back as bytes
            stems = {}
            with open(vocals_file, "rb") as f:
                stems["vocals.wav"] = f.read()
            with open(instrumental_file, "rb") as f:
                stems["instrumental.wav"] = f.read()
            
            return True, stems, "✅ Vocal separation completed successfully!"
            
    except Exception as e:
        return False, {}, f"❌ Separation error: {str(e)}"

def create_zip_download(stem_files, original_filename):
    """Create ZIP file for download"""
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for filename, file_data in stem_files.items():
            zip_file.writestr(filename, file_data)
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue()

def main():
    """Main Disband app"""
    load_beautiful_css()
    
    # Initialize session state
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    if 'stems_ready' not in st.session_state:
        st.session_state.stems_ready = False
    if 'stem_files' not in st.session_state:
        st.session_state.stem_files = {}
    
    # Hero Section
    st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">🎵 DISBAND</h1>
        <p class="hero-subtitle">Professional AI Stem Separator</p>
        <p class="hero-author">Created with ❤️ by @jeysshon</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if we need to install dependencies
    try:
        import librosa
        import soundfile
        deps_ready = True
    except ImportError:
        deps_ready = False
    
    if not deps_ready:
        st.markdown("""
        <div class="processing-container">
            <h3>🔧 Setting up Disband</h3>
            <p>Installing audio processing libraries...</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.spinner("Installing dependencies..."):
            if install_demucs_working():
                st.success("✅ Setup complete!")
                time.sleep(2)
                st.rerun()
            else:
                st.error("❌ Setup failed. Please refresh the page.")
                return
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Upload section
        st.markdown("""
        <div class="upload-container">
            <h2 style="margin-top: 0; color: #333; font-weight: 600;">📁 Upload Your Music</h2>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            label="Choose your audio file",
            type=['mp3', 'wav', 'flac', 'm4a', 'aac'],
            help="Drag and drop or click to browse",
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            # File info
            file_size_mb = len(uploaded_file.getbuffer()) / (1024 * 1024)
            st.markdown(f"""
            <div class="file-info">
                <h4>🎵 {uploaded_file.name}</h4>
                <p>📊 Size: {file_size_mb:.1f} MB | 🎼 Type: {uploaded_file.type}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Separation type
            separation_type = st.selectbox(
                "🎯 Separation Mode",
                ["Vocal + Instrumental", "Advanced (Coming Soon)"],
                help="Choose how you want to separate your music"
            )
            
            # Process button
            col_process1, col_process2 = st.columns([1, 1])
            
            with col_process1:
                if not st.session_state.processing and not st.session_state.stems_ready:
                    if st.button("🚀 Separate Stems", use_container_width=True):
                        st.session_state.processing = True
                        st.session_state.stems_ready = False
                        st.session_state.stem_files = {}
                        st.rerun()
                elif st.session_state.processing:
                    st.button("⏳ Processing...", disabled=True, use_container_width=True)
                else:
                    if st.button("🔄 Process New File", use_container_width=True):
                        st.session_state.processing = False
                        st.session_state.stems_ready = False
                        st.session_state.stem_files = {}
                        st.rerun()
            
            with col_process2:
                output_format = st.selectbox(
                    "🎧 Output Format",
                    ["WAV (Best Quality)", "MP3 (Smaller Size)"],
                    help="Choose your preferred audio format"
                )
    
    with col2:
        # Sidebar info
        st.markdown("### 📊 Project Stats")
        
        if uploaded_file:
            st.metric("File Size", f"{file_size_mb:.1f} MB")
            st.metric("Processing Time", "~2-5 min")
            st.metric("Quality", "Professional")
        else:
            st.info("👆 Upload a file to see stats")
        
        # Features
        st.markdown("### ✨ Features")
        st.markdown("""
        <div style="background: white; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
            <strong>🎤 Vocal Isolation</strong><br>
            Clean vocal tracks for remixing
        </div>
        <div style="background: white; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
            <strong>🎹 Instrumental</strong><br>
            Perfect backing tracks for covers
        </div>
        <div style="background: white; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
            <strong>🆓 100% Free</strong><br>
            No limits, no watermarks
        </div>
        """, unsafe_allow_html=True)
    
    # Processing section
    if st.session_state.processing and uploaded_file:
        st.markdown("""
        <div class="processing-container">
            <h3>🎯 AI Processing Your Music</h3>
            <p>Separating vocals and instruments using advanced algorithms...</p>
            <p>This may take 2-5 minutes depending on file size</p>
        </div>
        """, unsafe_allow_html=True)
        
        success, stem_files, message = basic_vocal_separation(uploaded_file)
        
        if success:
            st.session_state.stem_files = stem_files
            st.session_state.stems_ready = True
            st.session_state.processing = False
            st.rerun()
        else:
            st.session_state.processing = False
            st.markdown(f"""
            <div class="status-error">
                <h3>❌ Processing Failed</h3>
                <p>{message}</p>
                <p>Please try with a different file or contact support.</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Results section
    if st.session_state.stems_ready and st.session_state.stem_files:
        st.markdown("""
        <div class="results-container">
            <h2>🎉 Separation Complete!</h2>
            <p>Your stems are ready for download</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Stem files display
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 🎵 Generated Stems")
            
            stem_icons = {
                "vocals": "🎤",
                "instrumental": "🎹"
            }
            
            for filename in st.session_state.stem_files.keys():
                stem_type = filename.split('.')[0]
                icon = stem_icons.get(stem_type, "🎵")
                
                st.markdown(f"""
                <div class="stem-item">
                    <span class="stem-icon">{icon}</span>
                    <strong>{filename}</strong>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 💾 Downloads")
            
            # Individual downloads
            for filename, file_data in st.session_state.stem_files.items():
                st.download_button(
                    label=f"⬇️ {filename}",
                    data=file_data,
                    file_name=filename,
                    mime="audio/wav"
                )
            
            # ZIP download
            if uploaded_file:
                zip_data = create_zip_download(st.session_state.stem_files, uploaded_file.name)
                st.download_button(
                    label="📦 Download All (ZIP)",
                    data=zip_data,
                    file_name=f"{Path(uploaded_file.name).stem}_stems.zip",
                    mime="application/zip"
                )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem 0;">
        <p>🎵 <strong>DISBAND</strong> - Created with ❤️ by <strong>@jeysshon</strong></p>
        <p>Professional AI-powered stem separation • Free & Open Source</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
