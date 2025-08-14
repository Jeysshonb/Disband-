#!/usr/bin/env python3
"""
🎵 DISBAND - Separador de Stems que SÍ FUNCIONA
Usando ryan5453/demucs que tiene mejor compatibilidad
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

# CSS simplificado
def load_css():
    st.markdown("""
    <style>
    .stApp {
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    #MainMenu, footer, header { visibility: hidden; }
    
    .hero-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem; border-radius: 20px; text-align: center;
        margin-bottom: 2rem; color: white;
    }
    
    .hero-title {
        font-size: 3.5rem; font-weight: 700; margin: 0;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    
    .results-container {
        background: linear-gradient(135deg, #00c851 0%, #00a085 100%);
        padding: 2rem; border-radius: 16px; color: white; margin: 2rem 0;
    }
    
    .processing-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem; border-radius: 16px; color: white; text-align: center; margin: 2rem 0;
    }
    
    .warning-container {
        background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
        padding: 2rem; border-radius: 16px; color: white; text-align: center; margin: 2rem 0;
    }
    
    .success-container {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        padding: 1rem; border-radius: 12px; color: white; margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

def separate_with_replicate_simple(uploaded_file):
    """
    Usa ryan5453/demucs que es más simple y confiable
    """
    try:
        # API endpoint
        url = "https://api.replicate.com/v1/predictions"
        
        # Headers
        headers = {
            "Authorization": f"Token {st.secrets.get('REPLICATE_API_TOKEN', '')}",
            "Content-Type": "application/json"
        }
        
        # Convertir archivo a base64
        audio_bytes = uploaded_file.getbuffer()
        audio_b64 = base64.b64encode(audio_bytes).decode('utf-8')
        
        # Detectar tipo MIME
        file_type = uploaded_file.type
        if "mp3" in file_type or "mpeg" in file_type:
            mime_type = "audio/mp3"
        elif "wav" in file_type:
            mime_type = "audio/wav"
        else:
            mime_type = "audio/mp3"
        
        # Payload para ryan5453/demucs (más simple)
        data = {
            "version": "bd1ba71f38bae6b8b03be4d1d71a3a0c11e5a1b8b83b5dc95dd31d1b47b12094",
            "input": {
                "audio": f"data:{mime_type};base64,{audio_b64}"
            }
        }
        
        st.info(f"📤 Enviando archivo: {uploaded_file.name} ({len(audio_bytes)/1024/1024:.1f} MB)")
        
        # Hacer request
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 201:
            result = response.json()
            prediction_url = result["urls"]["get"]
            return True, prediction_url
        else:
            error_text = response.text
            st.error(f"❌ Error {response.status_code}: {error_text}")
            return False, error_text
            
    except Exception as e:
        st.error(f"❌ Excepción: {str(e)}")
        return False, str(e)

def check_prediction_status(prediction_url):
    """Verificar estado de la predicción"""
    try:
        headers = {
            "Authorization": f"Token {st.secrets.get('REPLICATE_API_TOKEN', '')}"
        }
        
        response = requests.get(prediction_url, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            status = result.get("status")
            
            if status == "succeeded":
                return "completed", result.get("output", {})
            elif status == "failed":
                return "failed", result.get("error", "Error desconocido")
            else:
                return "processing", result.get("logs", "Procesando...")
        else:
            return "error", f"HTTP {response.status_code}"
            
    except Exception as e:
        return "error", str(e)

def main():
    load_css()
    
    # Header
    st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">🎵 Disband</h1>
        <p style="font-size: 1.3rem; margin: 1rem 0 0 0;">AI Stem Separator que SÍ funciona</p>
        <p style="font-size: 1rem; margin: 0.5rem 0 0 0; opacity: 0.8;">Powered by Replicate API</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Verificar token
    token = st.secrets.get("REPLICATE_API_TOKEN", "")
    
    if not token:
        st.markdown("""
        <div class="warning-container">
            <h3>⚠️ Token de API Requerido</h3>
            <p>Necesitas configurar REPLICATE_API_TOKEN en Streamlit Secrets</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Interfaz principal
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📁 Subir Audio")
        
        uploaded_file = st.file_uploader(
            "Selecciona tu archivo de audio",
            type=['mp3', 'wav', 'm4a'],
            help="Máximo 25MB para APIs gratuitas"
        )
        
        if uploaded_file:
            file_size_mb = len(uploaded_file.getbuffer()) / (1024 * 1024)
            
            if file_size_mb > 25:
                st.error("⚠️ Archivo muy grande! Máximo 25MB para APIs gratuitas.")
                return
            
            st.success(f"✅ Archivo listo: **{uploaded_file.name}** ({file_size_mb:.1f} MB)")
            
            if st.button("🚀 Separar Stems", type="primary", use_container_width=True):
                st.session_state.processing = True
                st.session_state.uploaded_file = uploaded_file
                st.rerun()
    
    with col2:
        st.markdown("### 📊 Información")
        if uploaded_file:
            st.metric("Tamaño", f"{file_size_mb:.1f} MB")
            st.metric("Tiempo estimado", "3-8 min")
            st.metric("Costo", "~$0.04")
        
        st.markdown("### ✨ Características")
        st.markdown("""
        - 🎤 **Vocals** - Voz principal
        - 🥁 **Drums** - Batería
        - 🎸 **Bass** - Bajo  
        - 🎹 **Other** - Otros instrumentos
        - 📦 **Descarga todo** en ZIP
        """)
    
    # Procesamiento
    if st.session_state.get('processing', False):
        uploaded_file = st.session_state.get('uploaded_file')
        
        st.markdown("""
        <div class="processing-container">
            <h3>⚡ Procesando tu audio...</h3>
            <p>La IA está separando los stems en servidores con GPU</p>
            <p>Esto puede tomar 3-8 minutos</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Iniciar separación
        with st.spinner("Enviando a Replicate..."):
            success, result = separate_with_replicate_simple(uploaded_file)
        
        if success:
            prediction_url = result
            st.success("✅ Procesamiento iniciado correctamente!")
            
            # Esperar resultados
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            max_attempts = 60  # 10 minutos máximo
            for attempt in range(max_attempts):
                status, data = check_prediction_status(prediction_url)
                
                progress_percentage = min(95, (attempt / max_attempts) * 100)
                progress_bar.progress(int(progress_percentage))
                
                if status == "completed":
                    progress_bar.progress(100)
                    status_text.empty()
                    
                    # Guardar resultados
                    st.session_state.stems = data
                    st.session_state.processing = False
                    
                    st.markdown("""
                    <div class="success-container">
                        <h3>🎉 ¡Separación completada!</h3>
                        <p>Tus stems están listos para descargar</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.rerun()
                    
                elif status == "failed":
                    progress_bar.empty()
                    status_text.empty()
                    st.error(f"❌ Procesamiento falló: {data}")
                    st.session_state.processing = False
                    break
                    
                elif status == "processing":
                    status_text.text(f"🔄 Procesando... ({attempt + 1}/{max_attempts})")
                    if isinstance(data, str) and data.strip():
                        with st.expander("📋 Ver logs"):
                            st.text(data[-500:])  # Últimos 500 caracteres
                else:
                    status_text.text(f"⏳ Esperando respuesta... ({attempt + 1}/{max_attempts})")
                
                time.sleep(10)
            
            # Timeout
            if status != "completed":
                progress_bar.empty()
                status_text.empty()
                st.error("⏰ Timeout: El procesamiento tomó demasiado tiempo.")
                st.session_state.processing = False
        else:
            st.error(f"❌ Error iniciando procesamiento: {result}")
            st.session_state.processing = False
    
    # Mostrar resultados
    if st.session_state.get('stems'):
        stems = st.session_state.stems
        
        st.markdown("""
        <div class="results-container">
            <h2>🎉 ¡Separación Completada!</h2>
            <p>Descarga tus stems individuales o todo en ZIP</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Organizar descargas
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🎵 Stems Individuales:**")
            
            stem_icons = {
                "vocals": "🎤", "drums": "🥁", "bass": "🎸", "other": "🎹"
            }
            
            if isinstance(stems, dict):
                for stem_name, stem_url in stems.items():
                    if stem_url and isinstance(stem_url, str) and stem_url.startswith('http'):
                        icon = stem_icons.get(stem_name, "🎵")
                        st.markdown(f"{icon} **{stem_name.title()}**")
                        
                        # Descargar archivo
                        try:
                            response = requests.get(stem_url)
                            if response.status_code == 200:
                                st.download_button(
                                    f"⬇️ Descargar {stem_name}",
                                    data=response.content,
                                    file_name=f"{stem_name}.wav",
                                    mime="audio/wav"
                                )
                        except:
                            st.link_button(f"🔗 Abrir {stem_name}", stem_url)
        
        with col2:
            st.markdown("**📦 Descarga Completa:**")
            
            if st.button("📦 Crear ZIP de todos los stems"):
                with st.spinner("Creando ZIP..."):
                    zip_buffer = BytesIO()
                    
                    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
                        for stem_name, stem_url in stems.items():
                            if stem_url and isinstance(stem_url, str) and stem_url.startswith('http'):
                                try:
                                    response = requests.get(stem_url, timeout=30)
                                    if response.status_code == 200:
                                        zf.writestr(f"{stem_name}.wav", response.content)
                                except:
                                    pass
                    
                    zip_buffer.seek(0)
                    
                    st.download_button(
                        "⬇️ Descargar ZIP Completo",
                        data=zip_buffer.getvalue(),
                        file_name="stems_separados.zip",
                        mime="application/zip"
                    )
            
            # Info adicional
            st.info(f"""
            **ℹ️ Información:**
            - Stems generados: {len([k for k, v in stems.items() if v])}
            - Formato: WAV alta calidad
            - Procesado con IA en GPU
            """)
        
        # Botón para procesar otro archivo
        if st.button("🔄 Procesar Otro Archivo", use_container_width=True):
            for key in ['processing', 'stems', 'uploaded_file']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem 0;">
        <p>🎵 <strong>Disband</strong> - Separación de stems con IA</p>
        <p>Powered by Replicate API • Rápido • Confiable</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
