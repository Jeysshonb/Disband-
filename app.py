#!/usr/bin/env python3
"""
🎵 DISBAND - Separador de Stems usando API
Funciona en Streamlit Cloud sin instalar dependencias pesadas
"""

import streamlit as st
import requests
import time
import zipfile
from io import BytesIO
import base64

# Configuración de página
st.set_page_config(
    page_title="🎵 Disband - AI Stem Separator",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS simplificado pero bonito
def load_css():
    st.markdown("""
    <style>
    .stApp {
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    #MainMenu, footer, header { visibility: hidden; }
    
    .hero-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    
    .upload-container {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid #f0f2f6;
        margin-bottom: 2rem;
    }
    
    .results-container {
        background: linear-gradient(135deg, #00c851 0%, #00a085 100%);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        margin: 2rem 0;
    }
    
    .processing-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin: 2rem 0;
    }
    
    .warning-container {
        background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin: 2rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Función para convertir archivo a base64
def file_to_base64(uploaded_file):
    """Convierte archivo subido a base64 para enviar a API"""
    return base64.b64encode(uploaded_file.getbuffer()).decode()

# Función para usar Replicate API (GRATUITA)
def separate_with_replicate_api(uploaded_file, model="mdx_extra"):
    """
    Usa la API gratuita de Replicate para separar stems
    """
    try:
        # Configuración correcta para Demucs en Replicate
        url = "https://api.replicate.com/v1/predictions"
        
        headers = {
            "Authorization": f"Token {st.secrets.get('REPLICATE_API_TOKEN', '')}",
            "Content-Type": "application/json"
        }
        
        # Convertir archivo a base64 correctamente
        audio_bytes = uploaded_file.getbuffer()
        audio_b64 = base64.b64encode(audio_bytes).decode('utf-8')
        
        # Detectar tipo de archivo
        file_type = uploaded_file.type
        if file_type == "audio/mpeg":
            mime_type = "audio/mp3"
        elif file_type == "audio/wav":
            mime_type = "audio/wav"
        else:
            mime_type = "audio/mp3"  # Default
        
        # Usar modelo correcto de Demucs disponible
        data = {
            "version": "07c6b006d47c0188bb1c8288a81fa2f1b0e82f1d8a1b1cdf05c0aef55a1da2b4",  # Meta Demucs v4
            "input": {
                "audio": f"data:{mime_type};base64,{audio_b64}"
            }
        }
        
        # Debugging: mostrar request info
        st.write(f"🔍 Sending to Replicate - File: {uploaded_file.name}, Size: {len(audio_bytes)} bytes")
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 201:
            result = response.json()
            return True, result["urls"]["get"]
        else:
            # Mostrar error detallado
            error_detail = response.text
            st.error(f"API Response: {response.status_code} - {error_detail}")
            return False, f"HTTP {response.status_code}: {error_detail}"
            
    except Exception as e:
        st.error(f"Exception details: {str(e)}")
        return False, f"Exception: {str(e)}"

# Función alternativa usando Hugging Face (TAMBIÉN GRATUITA)
def separate_with_huggingface(audio_data):
    """
    Alternativa usando Hugging Face Inference API
    También gratuita pero con límites de uso
    """
    try:
        API_URL = "https://api-inference.huggingface.co/models/facebook/demucs-waveform-hdemucs"
        headers = {"Authorization": f"Bearer {st.secrets.get('HF_API_TOKEN', '')}"}
        
        # Decodificar base64 para enviar como bytes
        audio_bytes = base64.b64decode(audio_data)
        
        response = requests.post(API_URL, headers=headers, data=audio_bytes)
        
        if response.status_code == 200:
            return True, response.content
        else:
            return False, f"Error HF: {response.status_code}"
            
    except Exception as e:
        return False, f"Error: {str(e)}"

# Función para chequear estado de predicción
def check_prediction_status(prediction_url):
    """Chequea el estado de la predicción en Replicate"""
    try:
        headers = {
            "Authorization": "Token " + st.secrets.get("REPLICATE_API_TOKEN", "")
        }
        
        response = requests.get(prediction_url, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            status = result.get("status")
            
            if status == "succeeded":
                return "completed", result.get("output", {})
            elif status == "failed":
                return "failed", result.get("error", "Unknown error")
            else:
                return "processing", None
        else:
            return "error", f"HTTP {response.status_code}"
            
    except Exception as e:
        return "error", str(e)

# Función para crear ZIP de descarga
def create_download_zip(stems_dict):
    """Crear ZIP con los stems para descarga"""
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for stem_name, stem_url in stems_dict.items():
            # Descargar cada stem
            stem_response = requests.get(stem_url)
            if stem_response.status_code == 200:
                zip_file.writestr(f"{stem_name}.mp3", stem_response.content)
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue()

def main():
    load_css()
    
    # Hero Section
    st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">🎵 Disband</h1>
        <p style="font-size: 1.3rem; margin: 1rem 0 0 0;">AI-Powered Stem Separator</p>
        <p style="font-size: 1rem; margin: 0.5rem 0 0 0; opacity: 0.8;">Powered by Replicate API</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Verificar configuración de API
    replicate_token = st.secrets.get("REPLICATE_API_TOKEN", "")
    hf_token = st.secrets.get("HF_API_TOKEN", "")
    
    if not replicate_token and not hf_token:
        st.markdown("""
        <div class="warning-container">
            <h3>⚠️ Configuración Requerida</h3>
            <p>Para usar esta app, necesitas configurar una API key gratuita.</p>
            <p><strong>Opciones:</strong></p>
            <ul style="text-align: left; max-width: 600px; margin: 0 auto;">
                <li><a href="https://replicate.com" target="_blank" style="color: white;">Replicate.com</a> - Gratis hasta 1000 predicciones/mes</li>
                <li><a href="https://huggingface.co" target="_blank" style="color: white;">Hugging Face</a> - Gratis con límites por hora</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("📋 Instrucciones de Configuración"):
            st.markdown("""
            ### Opción 1: Replicate (Recomendado)
            1. Ve a [replicate.com](https://replicate.com) y crea cuenta gratis
            2. Ve a Account → API Tokens
            3. Copia tu token
            4. En Streamlit Cloud: Settings → Secrets
            5. Agrega: `REPLICATE_API_TOKEN = "tu_token_aqui"`
            
            ### Opción 2: Hugging Face
            1. Ve a [huggingface.co](https://huggingface.co) y crea cuenta
            2. Ve a Settings → Access Tokens  
            3. Crea token con permisos de lectura
            4. En Streamlit Cloud: Settings → Secrets
            5. Agrega: `HF_API_TOKEN = "tu_token_aqui"`
            
            ### ¿Dónde están los Secrets en Streamlit?
            1. Ve a share.streamlit.io
            2. Click en tu app → "⚙️" → "Secrets"
            3. Agrega el token como se muestra arriba
            """)
        return
    
    # Interfaz principal
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="upload-container">
            <h2 style="margin-top: 0; color: #333;">📁 Upload Your Audio</h2>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose your audio file",
            type=['mp3', 'wav', 'm4a'],
            help="Supported: MP3, WAV, M4A (max 25MB for free APIs)",
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            file_size_mb = len(uploaded_file.getbuffer()) / (1024 * 1024)
            
            if file_size_mb > 25:
                st.error("⚠️ File too large! Free APIs support max 25MB. Try compressing your audio.")
                return
            
            st.info(f"📄 **{uploaded_file.name}** ({file_size_mb:.1f} MB)")
            
            # Model selection
            model = st.selectbox(
                "🤖 AI Model",
                ["mdx_extra", "hdemucs_mmi", "htdemucs"],
                format_func=lambda x: {
                    "mdx_extra": "🚀 Ultra Fast (2-3 min)",
                    "hdemucs_mmi": "⚡ Fast (3-5 min)", 
                    "htdemucs": "🎯 High Quality (5-8 min)"
                }[x]
            )
            
            # Process button
            if st.button("🚀 Separate Stems", type="primary", use_container_width=True):
                st.session_state.processing = True
                st.session_state.uploaded_file = uploaded_file
                st.session_state.model = model
                st.rerun()
    
    with col2:
        st.markdown("### 📊 Quick Info")
        if uploaded_file:
            st.metric("File Size", f"{file_size_mb:.1f} MB")
            st.metric("Processing", "~3-8 min")
            st.metric("API", "Replicate/HF")
        
        st.markdown("### 💡 Features")
        st.markdown("""
        - ✅ No installation required
        - ✅ Runs in the cloud  
        - ✅ Professional quality
        - ✅ Multiple formats
        - ✅ Free API usage
        """)
    
    # Processing section
    if st.session_state.get('processing', False):
        uploaded_file = st.session_state.get('uploaded_file')
        model = st.session_state.get('model', 'mdx_extra')
        
        st.markdown("""
        <div class="processing-container">
            <h3>⚡ Processing Your Audio</h3>
            <p>Using cloud AI to separate stems...</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Convert file directly and start separation
        if replicate_token:
            st.info("🔄 Using Replicate API...")
            success, result = separate_with_replicate_api(uploaded_file, model)
            
            if success:
                prediction_url = result
                st.info("⏳ Waiting for processing to complete...")
                
                # Poll for results
                progress_bar = st.progress(0)
                for i in range(60):  # Max 10 minutes
                    status, data = check_prediction_status(prediction_url)
                    
                    if status == "completed":
                        progress_bar.progress(100)
                        st.session_state.stems = data
                        st.session_state.processing = False
                        st.success("✅ Separation completed!")
                        st.rerun()
                    elif status == "failed":
                        st.error(f"❌ Processing failed: {data}")
                        st.session_state.processing = False
                        break
                    else:
                        progress_bar.progress(min(95, i * 100 // 60))
                        time.sleep(10)
                
                if status != "completed":
                    st.error("⏰ Processing timeout. Try with a smaller file.")
                    st.session_state.processing = False
            else:
                st.error(f"❌ API Error: {result}")
                st.session_state.processing = False
        
        elif hf_token:
            st.info("🔄 Using Hugging Face API...")
            # Para HF, aún necesitamos base64
            audio_b64 = file_to_base64(uploaded_file)
            success, result = separate_with_huggingface(audio_b64)
            
            if success:
                st.session_state.stems = {"stems": result}
                st.session_state.processing = False
                st.success("✅ Separation completed!")
                st.rerun()
            else:
                st.error(f"❌ {result}")
                st.session_state.processing = False
    
    # Results section
    if st.session_state.get('stems'):
        st.markdown("""
        <div class="results-container">
            <h2>🎉 Separation Complete!</h2>
            <p>Your stems are ready for download</p>
        </div>
        """, unsafe_allow_html=True)
        
        stems = st.session_state.stems
        
        # Download section
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Individual Stems:**")
            if isinstance(stems, dict):
                for stem_name, stem_url in stems.items():
                    if stem_url and stem_name != "stems":
                        st.markdown(f"🎵 **{stem_name}**")
                        st.link_button(f"⬇️ Download {stem_name}", stem_url)
        
        with col2:
            st.markdown("**Complete Package:**")
            if st.button("📦 Create ZIP Download"):
                with st.spinner("Creating ZIP..."):
                    zip_data = create_download_zip(stems)
                    st.download_button(
                        "⬇️ Download All Stems (ZIP)",
                        data=zip_data,
                        file_name="stems.zip",
                        mime="application/zip"
                    )
        
        # Reset button
        if st.button("🔄 Process Another File"):
            for key in ['processing', 'stems', 'uploaded_file', 'model']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem 0;">
        <p>🎵 <strong>Disband</strong> - Powered by Replicate API</p>
        <p>Free • Fast • Professional Quality</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
