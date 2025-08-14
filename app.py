#!/usr/bin/env python3
"""
🎵 DISBAND - Beautiful AI Stem Separator
Created by @jeysshon

Deploy to Streamlit Cloud from GitHub
Beautiful, fast, and professional stem separation
"""

import streamlit as st
import subprocess
import sys
import os
import tempfile
import zipfile
import time
from pathlib import Path
import base64
from io import BytesIO

# Page config - MUST be first Streamlit command
st.set_page_config(
    page_title="🎵 Disband - AI Stem Separator",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def load_css():
    """Load beautiful custom CSS"""
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container */
    .main > div {
        padding-top: 1rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Hero Section */
    .hero-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        color: white;
        margin: 0;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        letter-spacing: -0.02em;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        color: rgba(255,255,255,0.9);
        margin: 1rem 0 0 0;
        font-weight: 400;
    }
    
    .hero-author {
        font-size: 1rem;
        color: rgba(255,255,255,0.7);
        margin: 0.5rem 0 0 0;
        font-weight: 300;
    }
    
    /* Upload Section */
    .upload-container {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid #f0f2f6;
        margin-bottom: 2rem;
    }
    
    .upload-zone {
        border: 2px dashed #667eea;
        border-radius: 12px;
        padding: 3rem 2rem;
        text-align: center;
        background: linear-gradient(135deg, #f8faff 0%, #f0f4ff 100%);
        transition: all 0.3s ease;
    }
    
    .upload-zone:hover {
        border-color: #764ba2;
        background: linear-gradient(135deg, #f0f4ff 0%, #e8f0ff 100%);
    }
    
    /* Cards */
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        transition: transform 0.2s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }
    
    .model-card {
        background: linear-gradient(135deg, #fff 0%, #f8faff 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e8f0ff;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .model-card:hover {
        border-color: #667eea;
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(102,126,234,0.15);
    }
    
    .model-card.selected {
        border-color: #667eea;
        background: linear-gradient(135deg, #f0f4ff 0%, #e8f0ff 100%);
    }
    
    /* Progress Section */
    .progress-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin: 2rem 0;
    }
    
    .progress-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    /* Results Section */
    .results-container {
        background: linear-gradient(135deg, #00c851 0%, #00a085 100%);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        margin: 2rem 0;
    }
    
    .stem-item {
        background: rgba(255,255,255,0.15);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        display: flex;
        align-items: center;
        backdrop-filter: blur(10px);
    }
    
    .stem-icon {
        font-size: 1.5rem;
        margin-right: 1rem;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102,126,234,0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102,126,234,0.4);
    }
    
    .stDownloadButton > button {
        background: linear-gradient(135deg, #00c851 0%, #00a085 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        margin: 0.2rem;
        transition: all 0.2s ease;
    }
    
    .stDownloadButton > button:hover {
        transform: scale(1.05);
    }
    
    /* File Info */
    .file-info {
        background: linear-gradient(135deg, #17a2b8 0%, #138496 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    /* Success Messages */
    .success-message {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
    }
    
    /* Warning Messages */
    .warning-message {
        background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8faff 0%, #f0f4ff 100%);
    }
    
    /* Metrics */
    [data-testid="metric-container"] {
        background: white;
        border: 1px solid #e8f0ff;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    /* Custom spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        
        .hero-subtitle {
            font-size: 1.1rem;
        }
        
        .upload-container {
            padding: 1rem;
        }
        
        .upload-zone {
            padding: 2rem 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import demucs
        return True, "✅ Ready to separate stems!"
    except ImportError:
        return False, "Dependencies still installing..."

def show_dependency_error():
    """Show dependency installation instructions"""
    st.markdown("""
    <div class="warning-message">
        <h3>⚡ Setting up Disband</h3>
        <p>Dependencies are being installed by Streamlit Cloud...</p>
        <p><strong>Please wait 3-5 minutes and refresh this page.</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("""
    **What's happening:**
    1. Streamlit Cloud is installing PyTorch and Demucs
    2. This only happens once on first deployment
    3. Future visits will be instant
    """)
    
    if st.button("🔄 Check Again", use_container_width=True):
        st.rerun()
        
    st.markdown("---")
    st.markdown("⏱️ **Expected wait time:** 3-5 minutes")
    st.markdown("🔄 **Then:** Refresh this page")
    st.markdown("✅ **Result:** Beautiful stem separation!")

def get_model_info():
    """Get information about available models"""
    return {
        "htdemucs_ft": {
            "name": "🏆 Hybrid Transformer Fine-tuned",
            "quality": "⭐⭐⭐⭐⭐",
            "speed": "Slow (Best Quality)",
            "desc": "Maximum quality for professional results",
            "time": "15-30 min",
            "icon": "🏆"
        },
        "htdemucs": {
            "name": "🎯 Hybrid Transformer",
            "quality": "⭐⭐⭐⭐",
            "speed": "Medium (Balanced)",
            "desc": "Perfect balance of quality and speed",
            "time": "8-15 min",
            "icon": "🎯"
        },
        "htdemucs_6s": {
            "name": "🎼 6 Sources Model",
            "quality": "⭐⭐⭐⭐",
            "speed": "Medium (6 Stems)",
            "desc": "Separates vocals, drums, bass, other, piano, guitar",
            "time": "10-20 min",
            "icon": "🎼"
        },
        "hdemucs_mmi": {
            "name": "⚡ Hybrid Demucs v3",
            "quality": "⭐⭐⭐",
            "speed": "Fast (Good Quality)",
            "desc": "Quick processing with solid results",
            "time": "5-10 min",
            "icon": "⚡"
        },
        "mdx_extra": {
            "name": "🚀 MDX Extra",
            "quality": "⭐⭐⭐",
            "speed": "Very Fast",
            "desc": "Lightning fast for quick tests",
            "time": "2-5 min",
            "icon": "🚀"
        }
    }

def create_model_card(model_key, model_info, selected_model):
    """Create a beautiful model selection card"""
    is_selected = model_key == selected_model
    card_class = "model-card selected" if is_selected else "model-card"
    
    return f"""
    <div class="{card_class}">
        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
            <span style="font-size: 1.5rem; margin-right: 0.5rem;">{model_info['icon']}</span>
            <strong style="font-size: 1.1rem;">{model_info['name']}</strong>
        </div>
        <div style="margin-bottom: 0.5rem;">
            <span style="color: #666;">Quality: {model_info['quality']}</span>
            <span style="color: #666; margin-left: 1rem;">Time: ~{model_info['time']}</span>
        </div>
        <div style="color: #888; font-size: 0.9rem;">{model_info['desc']}</div>
    </div>
    """

def separate_audio(uploaded_file, model, output_format):
    """Separate audio using Demucs"""
    try:
        # Create temp directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = Path(temp_dir)
            
            # Save uploaded file
            input_path = temp_dir / uploaded_file.name
            with open(input_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Output directory
            output_dir = temp_dir / "output"
            output_dir.mkdir()
            
            # Build command
            cmd = [
                sys.executable, "-m", "demucs",
                "--model", model,
                "--out", str(output_dir)
            ]
            
            # Add format options
            if output_format == "MP3":
                cmd.extend(["--mp3", "--mp3-bitrate", "320"])
            elif output_format == "FLAC":
                cmd.append("--flac")
            else:  # WAV
                cmd.append("--float32")
            
            cmd.append(str(input_path))
            
            # Progress tracking
            progress_placeholder = st.empty()
            log_placeholder = st.empty()
            
            # Execute separation
            with progress_placeholder.container():
                st.markdown("""
                <div class="progress-container">
                    <div class="progress-icon">🎵</div>
                    <h3>AI is working its magic...</h3>
                    <p>This may take a few minutes depending on your model choice</p>
                </div>
                """, unsafe_allow_html=True)
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            
            # Read output
            logs = []
            for line in process.stdout:
                line = line.strip()
                if line:
                    logs.append(line)
                    if len(logs) > 10:
                        logs.pop(0)
                    
                    with log_placeholder.container():
                        st.code('\n'.join(logs[-5:]), language='text')
            
            process.wait()
            
            progress_placeholder.empty()
            log_placeholder.empty()
            
            if process.returncode == 0:
                # Find output files
                stem_folder = output_dir / model / input_path.stem
                
                if stem_folder.exists():
                    # Get file extension
                    ext = "mp3" if output_format == "MP3" else "flac" if output_format == "FLAC" else "wav"
                    
                    # Read files
                    stem_files = {}
                    for stem_file in stem_folder.glob(f"*.{ext}"):
                        with open(stem_file, "rb") as f:
                            stem_files[stem_file.name] = f.read()
                    
                    return True, stem_files, f"🎉 Successfully separated into {len(stem_files)} stems!"
                else:
                    return False, {}, "❌ No output files found"
            else:
                return False, {}, "❌ Separation failed"
                
    except Exception as e:
        return False, {}, f"❌ Error: {str(e)}"

def create_zip_download(stem_files, original_filename):
    """Create ZIP file for download"""
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for filename, file_data in stem_files.items():
            zip_file.writestr(filename, file_data)
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue()

def main():
    """Main Streamlit app"""
    load_css()
    
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
        <h1 class="hero-title">🎵 Disband</h1>
        <p class="hero-subtitle">Beautiful AI-Powered Stem Separator</p>
        <p class="hero-author">Created by @jeysshon</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check dependencies
    deps_ok, deps_msg = check_dependencies()
    
    if not deps_ok:
        show_dependency_error()
        # Don't return - show the interface anyway for testing
        st.warning("⚠️ Some features may not work until dependencies are installed")
    
    # Main interface (always show)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Upload section
        st.markdown("""
        <div class="upload-container">
            <h2 style="margin-top: 0; color: #333; font-weight: 600;">📁 Upload Your Audio</h2>
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
                <h4>📄 {uploaded_file.name}</h4>
                <p>📏 Size: {file_size_mb:.1f} MB | 🎵 Type: {uploaded_file.type}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Model selection
            st.markdown("### 🤖 Choose AI Model")
            
            models = get_model_info()
            selected_model = st.radio(
                "Select model",
                options=list(models.keys()),
                index=1,  # htdemucs default
                format_func=lambda x: f"{models[x]['icon']} {models[x]['name']} - {models[x]['time']}",
                label_visibility="collapsed"
            )
            
            # Format selection
            col_format, col_process = st.columns([1, 1])
            
            with col_format:
                output_format = st.selectbox(
                    "💾 Output Format",
                    ["MP3", "WAV", "FLAC"],
                    help="MP3: Smaller files, WAV: Best quality, FLAC: Compressed lossless"
                )
            
            with col_process:
                st.markdown("<br>", unsafe_allow_html=True)  # Spacing
                if not deps_ok:
                    st.button("🔄 Dependencies Installing...", disabled=True, use_container_width=True)
                elif not st.session_state.processing and not st.session_state.stems_ready:
                    if st.button("🎯 Separate Stems", use_container_width=True):
                        st.session_state.processing = True
                        st.session_state.stems_ready = False
                        st.session_state.stem_files = {}
                        st.rerun()
                elif st.session_state.processing:
                    st.button("🔄 Processing...", disabled=True, use_container_width=True)
                else:
                    if st.button("🔄 Process New File", use_container_width=True):
                        st.session_state.processing = False
                        st.session_state.stems_ready = False
                        st.session_state.stem_files = {}
                        st.rerun()
    
    with col2:
        # Sidebar info
        st.markdown("### 📊 Quick Stats")
        
        if uploaded_file:
            model_info = models[selected_model]
            st.metric("Estimated Time", model_info['time'])
            st.metric("Quality Level", model_info['quality'])
            st.metric("File Size", f"{file_size_mb:.1f} MB")
        else:
            st.info("👆 Upload a file to see stats")
        
        # Tips section
        st.markdown("### 💡 Pro Tips")
        st.markdown("""
        <div class="feature-card">
            <strong>🏆 Best Quality:</strong><br>
            Use htdemucs_ft for professional results
        </div>
        <div class="feature-card">
            <strong>⚡ Quick Test:</strong><br>
            Use mdx_extra for fast previews
        </div>
        <div class="feature-card">
            <strong>🎼 Six Stems:</strong><br>
            Use htdemucs_6s for complex songs
        </div>
        """, unsafe_allow_html=True)
    
    # Processing section
    if st.session_state.processing and uploaded_file:
        success, stem_files, message = separate_audio(uploaded_file, selected_model, output_format)
        
        if success:
            st.session_state.stem_files = stem_files
            st.session_state.stems_ready = True
            st.session_state.processing = False
            st.rerun()
        else:
            st.session_state.processing = False
            st.error(message)
    
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
                "drums": "🥁",
                "bass": "🎸", 
                "vocals": "🎤",
                "other": "🎹",
                "piano": "🎹",
                "guitar": "🎸"
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
                    mime="audio/mpeg"
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
        <p>🎵 <strong>Disband</strong> - Created with ❤️ by <strong>@jeysshon</strong></p>
        <p>Powered by Demucs AI • Free & Open Source • Privacy First</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
