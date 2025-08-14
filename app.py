#!/usr/bin/env python3
"""
🎵 DISBAND RÁPIDO - Separador de Stems Ultra Optimizado
Versión mejorada para máximo rendimiento y simplicidad
"""

import streamlit as st
import subprocess
import sys
import os
import tempfile
import zipfile
import time
from pathlib import Path
import threading
import queue
from concurrent.futures import ThreadPoolExecutor

# Configuración de página optimizada
st.set_page_config(
    page_title="🎵 Disband Rápido",
    page_icon="🎵",
    layout="centered",  # Cambiado a centered para mejor rendimiento
    initial_sidebar_state="collapsed"
)

# CSS minimalista y optimizado
def load_minimal_css():
    st.markdown("""
    <style>
    /* Estilos mínimos para máximo rendimiento */
    .stApp {
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    
    .main-header {
        background: linear-gradient(90deg, #667eea, #764ba2);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .quick-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .status-success {
        background: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    .status-processing {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    .status-error {
        background: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Modelos optimizados (solo los más rápidos)
FAST_MODELS = {
    "mdx_extra": {
        "name": "🚀 Ultra Rápido (2-3 min)",
        "desc": "Calidad buena, velocidad máxima"
    },
    "hdemucs_mmi": {
        "name": "⚡ Rápido (3-5 min)", 
        "desc": "Buen balance calidad/velocidad"
    },
    "htdemucs": {
        "name": "🎯 Calidad Alta (5-8 min)",
        "desc": "Solo si necesitas máxima calidad"
    }
}

def check_demucs_installed():
    """Verificación rápida de Demucs"""
    try:
        import demucs
        return True
    except ImportError:
        return False

@st.cache_data(ttl=3600)  # Cache por 1 hora
def install_demucs_cached():
    """Instalación cacheada de Demucs"""
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "demucs==4.0.1", "--quiet", "--no-cache-dir"
        ], check=True, timeout=300)
        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return False

def process_audio_optimized(uploaded_file, model="mdx_extra"):
    """Procesamiento optimizado con configuraciones rápidas"""
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Guardar archivo
            input_file = temp_path / uploaded_file.name
            with open(input_file, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            output_dir = temp_path / "separated"
            
            # Comando optimizado para velocidad
            cmd = [
                sys.executable, "-m", "demucs",
                "--model", model,
                "--out", str(output_dir),
                "--mp3",  # Siempre MP3 para velocidad
                "--mp3-bitrate", "192",  # Bitrate reducido para velocidad
                "--jobs", "2",  # Máximo 2 trabajos paralelos
                str(input_file)
            ]
            
            # Ejecutar con timeout
            process = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=1800  # 30 minutos máximo
            )
            
            if process.returncode == 0:
                # Buscar archivos generados
                model_dir = output_dir / model / input_file.stem
                
                if model_dir.exists():
                    files = {}
                    for mp3_file in model_dir.glob("*.mp3"):
                        with open(mp3_file, "rb") as f:
                            files[mp3_file.name] = f.read()
                    return True, files
                    
            return False, {}
            
    except subprocess.TimeoutExpired:
        return False, {}
    except Exception as e:
        st.error(f"Error: {e}")
        return False, {}

def create_zip_fast(files, name):
    """Crear ZIP optimizado"""
    from io import BytesIO
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED, compresslevel=1) as zf:
        for filename, data in files.items():
            zf.writestr(filename, data)
    
    return zip_buffer.getvalue()

def main():
    load_minimal_css()
    
    # Header simple
    st.markdown("""
    <div class="main-header">
        <h1>🎵 Disband Rápido</h1>
        <p>Separación de stems ultra optimizada</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Verificar instalación
    if not check_demucs_installed():
        with st.spinner("🔧 Instalando Demucs por primera vez..."):
            if install_demucs_cached():
                st.success("✅ Listo para usar!")
                st.rerun()
            else:
                st.error("❌ Error de instalación. Recarga la página.")
                return
    
    # Interfaz principal simplificada
    with st.container():
        st.markdown('<div class="quick-card">', unsafe_allow_html=True)
        
        # Upload
        uploaded_file = st.file_uploader(
            "📁 Sube tu archivo de audio",
            type=['mp3', 'wav', 'flac', 'm4a'],
            help="Archivos hasta 200MB"
        )
        
        if uploaded_file:
            # Info del archivo
            size_mb = len(uploaded_file.getbuffer()) / (1024 * 1024)
            st.info(f"📄 {uploaded_file.name} ({size_mb:.1f} MB)")
            
            # Selección rápida de modelo
            col1, col2 = st.columns([2, 1])
            
            with col1:
                model = st.selectbox(
                    "🤖 Velocidad de procesamiento",
                    options=list(FAST_MODELS.keys()),
                    format_func=lambda x: FAST_MODELS[x]["name"],
                    index=0  # Por defecto el más rápido
                )
                st.caption(FAST_MODELS[model]["desc"])
            
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                process_btn = st.button(
                    "🚀 Separar Stems", 
                    type="primary",
                    use_container_width=True
                )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Procesamiento
    if uploaded_file and process_btn:
        # Status de procesamiento
        st.markdown("""
        <div class="status-processing">
            <strong>⚡ Procesando...</strong><br>
            Esto tomará unos minutos dependiendo del modelo seleccionado.
        </div>
        """, unsafe_allow_html=True)
        
        # Barra de progreso
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Simular progreso mientras procesa
        for i in range(10):
            progress_bar.progress((i + 1) * 10)
            status_text.text(f"Procesando... {(i + 1) * 10}%")
            time.sleep(1)
        
        # Procesar
        success, files = process_audio_optimized(uploaded_file, model)
        
        progress_bar.empty()
        status_text.empty()
        
        if success and files:
            # Resultados
            st.markdown("""
            <div class="status-success">
                <strong>✅ ¡Separación completada!</strong><br>
                Tus stems están listos para descargar.
            </div>
            """, unsafe_allow_html=True)
            
            # Downloads
            st.markdown("### 📥 Descargas")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Stems individuales:**")
                for filename, data in files.items():
                    st.download_button(
                        f"⬇️ {filename}",
                        data=data,
                        file_name=filename,
                        mime="audio/mpeg"
                    )
            
            with col2:
                st.markdown("**Descarga todo:**")
                zip_data = create_zip_fast(files, uploaded_file.name)
                st.download_button(
                    "📦 Descargar ZIP",
                    data=zip_data,
                    file_name=f"{Path(uploaded_file.name).stem}_stems.zip",
                    mime="application/zip"
                )
        else:
            st.markdown("""
            <div class="status-error">
                <strong>❌ Error en el procesamiento</strong><br>
                Intenta con un archivo más pequeño o un modelo más rápido.
            </div>
            """, unsafe_allow_html=True)
    
    # Tips de optimización
    if not uploaded_file:
        st.markdown("### 💡 Tips para mayor velocidad")
        st.markdown("""
        - **🚀 Ultra Rápido**: Para pruebas rápidas y resultados decentes
        - **⚡ Rápido**: Buen balance para uso general  
        - **🎯 Calidad Alta**: Solo si necesitas máxima calidad
        - **📁 Archivos**: MP3 menores a 50MB procesan más rápido
        - **⏰ Tiempo**: El modelo ultra rápido toma 2-3 minutos típicamente
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("🎵 **Disband Rápido** - Optimizado para velocidad máxima")

if __name__ == "__main__":
    main()
