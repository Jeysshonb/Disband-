#!/usr/bin/env python3
"""
🎵 DISBAND - Con instalación automática de emergencia
"""

import streamlit as st
import subprocess
import sys
import os
import tempfile
import zipfile
import time
from pathlib import Path
from io import BytesIO

# Configuración de página
st.set_page_config(
    page_title="🎵 Disband Rápido",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS minimalista
def load_css():
    st.markdown("""
    <style>
    .stApp { font-family: -apple-system, BlinkMacSystemFont, sans-serif; }
    #MainMenu, footer, header { visibility: hidden; }
    
    .main-header {
        background: linear-gradient(90deg, #667eea, #764ba2);
        padding: 2rem; border-radius: 12px; color: white;
        text-align: center; margin-bottom: 2rem;
    }
    
    .status-success {
        background: #d4edda; border-left: 4px solid #28a745;
        padding: 1rem; border-radius: 4px; margin: 1rem 0;
    }
    
    .status-processing {
        background: #fff3cd; border-left: 4px solid #ffc107;
        padding: 1rem; border-radius: 4px; margin: 1rem 0;
    }
    
    .status-error {
        background: #f8d7da; border-left: 4px solid #dc3545;
        padding: 1rem; border-radius: 4px; margin: 1rem 0;
    }
    
    .install-box {
        background: #e3f2fd; border: 2px solid #2196f3;
        padding: 1.5rem; border-radius: 8px; margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

def emergency_install():
    """Instalación de emergencia si requirements.txt falló"""
    st.markdown("""
    <div class="install-box">
        <h3>🔧 Instalación de Emergencia</h3>
        <p>Instalando dependencias que no se cargaron desde requirements.txt...</p>
    </div>
    """, unsafe_allow_html=True)
    
    packages_to_install = [
        "torch",
        "torchaudio", 
        "demucs",
        "librosa",
        "soundfile"
    ]
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, package in enumerate(packages_to_install):
        try:
            status_text.text(f"📦 Instalando {package}...")
            progress_bar.progress((i + 1) / len(packages_to_install))
            
            # Instalar paquete
            subprocess.run([
                sys.executable, "-m", "pip", "install", package, 
                "--quiet", "--no-cache-dir"
            ], check=True, timeout=300)
            
            status_text.text(f"✅ {package} instalado")
            time.sleep(0.5)
            
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            status_text.text(f"❌ Error instalando {package}")
            st.error(f"No se pudo instalar {package}: {e}")
            return False
    
    progress_bar.progress(1.0)
    status_text.text("✅ Instalación completada!")
    time.sleep(2)
    
    progress_bar.empty()
    status_text.empty()
    
    return True

def check_dependencies():
    """Verificar dependencias con opción de instalación automática"""
    missing_modules = []
    
    modules_to_check = {
        "demucs": "demucs",
        "torch": "torch", 
        "torchaudio": "torchaudio",
        "librosa": "librosa",
        "soundfile": "soundfile"
    }
    
    for display_name, module_name in modules_to_check.items():
        try:
            __import__(module_name)
        except ImportError:
            missing_modules.append(display_name)
    
    if missing_modules:
        return False, missing_modules
    else:
        return True, []

# Modelos optimizados
MODELS = {
    "mdx_extra": {
        "name": "🚀 Ultra Rápido",
        "time": "2-3 min",
        "desc": "Calidad buena, velocidad máxima"
    },
    "hdemucs_mmi": {
        "name": "⚡ Rápido", 
        "time": "3-5 min",
        "desc": "Buen balance calidad/velocidad"
    }
}

def separate_stems(uploaded_file, model="mdx_extra"):
    """Separar stems usando Demucs"""
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Guardar archivo
            input_file = temp_path / uploaded_file.name
            with open(input_file, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            output_dir = temp_path / "separated"
            
            # Comando optimizado
            cmd = [
                sys.executable, "-m", "demucs",
                "--model", model,
                "--out", str(output_dir),
                "--mp3",
                "--mp3-bitrate", "192",
                "--jobs", "1",
                "--device", "cpu",
                str(input_file)
            ]
            
            # Ejecutar
            process = subprocess.run(
                cmd, capture_output=True, text=True, timeout=1800
            )
            
            if process.returncode == 0:
                model_dir = output_dir / model / input_file.stem
                
                if model_dir.exists():
                    stem_files = {}
                    for mp3_file in model_dir.glob("*.mp3"):
                        with open(mp3_file, "rb") as f:
                            stem_files[mp3_file.name] = f.read()
                    
                    if stem_files:
                        return True, stem_files, f"✅ {len(stem_files)} stems generados"
                    
            return False, {}, f"❌ Error: {process.stderr}"
                
    except Exception as e:
        return False, {}, f"❌ Error: {str(e)}"

def create_zip(files, original_name):
    """Crear ZIP para descarga"""
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        for filename, data in files.items():
            zf.writestr(filename, data)
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue()

def main():
    load_css()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎵 Disband Rápido</h1>
        <p>Separación de stems con instalación automática</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Verificar dependencias
    deps_ok, missing = check_dependencies()
    
    if not deps_ok:
        st.markdown(f"""
        <div class="status-error">
            <h3>🔧 Dependencias Faltantes</h3>
            <p><strong>Módulos no encontrados:</strong> {', '.join(missing)}</p>
            <p>Esto significa que Streamlit Cloud no instaló correctamente desde requirements.txt</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Botón de instalación automática
        if st.button("🚀 Instalar Dependencias Automáticamente", type="primary"):
            if emergency_install():
                st.success("✅ ¡Instalación completada! Recargando...")
                time.sleep(2)
                st.rerun()
            else:
                st.error("❌ La instalación automática falló. Revisar configuración del repositorio.")
        
        # Información de troubleshooting
        with st.expander("🔍 Información para Solucionar"):
            st.markdown(f"""
            **Versión de Python detectada:** {sys.version}
            
            **Posibles causas del problema:**
            1. El archivo `requirements.txt` no está en la raíz del repositorio
            2. Streamlit Cloud no completó la instalación inicial
            3. Hay un error en el formato de requirements.txt
            4. Timeout durante la instalación
            
            **Soluciones recomendadas:**
            1. **Usa el botón de arriba** para instalación automática
            2. **Verifica tu repositorio** tenga esta estructura:
               ```
               tu-repo/
               ├── app.py
               ├── requirements.txt  ← Debe estar aquí
               ├── packages.txt
               └── .streamlit/config.toml
               ```
            3. **Re-deploy tu app** en Streamlit Cloud
            4. **Espera 10-15 minutos** para instalación completa
            
            **requirements.txt debe contener:**
            ```
            streamlit>=1.28.0
            torch>=2.0.0
            torchaudio>=2.0.0
            demucs>=4.0.0
            numpy>=1.21.0
            scipy>=1.7.0
            librosa>=0.9.0
            soundfile>=0.12.0
            ffmpeg-python>=0.2.0
            ```
            """)
        
        return
    
    # Si todo está bien, mostrar interfaz principal
    st.markdown("""
    <div class="status-success">
        <strong>✅ Todas las dependencias están cargadas correctamente</strong>
    </div>
    """, unsafe_allow_html=True)
    
    # Interfaz de upload
    uploaded_file = st.file_uploader(
        "📁 Sube tu archivo de audio",
        type=['mp3', 'wav', 'flac', 'm4a', 'aac'],
        help="Máximo 200MB"
    )
    
    if uploaded_file:
        size_mb = len(uploaded_file.getbuffer()) / (1024 * 1024)
        st.info(f"📄 **{uploaded_file.name}** ({size_mb:.1f} MB)")
        
        # Selección de modelo
        col1, col2 = st.columns([2, 1])
        
        with col1:
            model = st.selectbox(
                "🤖 Velocidad",
                options=list(MODELS.keys()),
                format_func=lambda x: f"{MODELS[x]['name']} ({MODELS[x]['time']})",
                index=0
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚀 Separar", type="primary", use_container_width=True):
                st.session_state.processing = True
    
    # Procesamiento
    if uploaded_file and st.session_state.get('processing', False):
        st.markdown("""
        <div class="status-processing">
            <h3>⚡ Procesando...</h3>
            <p>Separando stems, esto tomará unos minutos...</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.spinner("Procesando audio..."):
            success, files, message = separate_stems(uploaded_file, model)
        
        st.session_state.processing = False
        
        if success:
            st.markdown(f"""
            <div class="status-success">
                <h3>🎉 ¡Separación completada!</h3>
                <p>{message}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Downloads
            st.markdown("### 📥 Descargar Stems")
            
            col1, col2 = st.columns(2)
            
            with col1:
                for filename, data in files.items():
                    st.download_button(
                        f"🎵 {filename}",
                        data=data,
                        file_name=filename,
                        mime="audio/mpeg"
                    )
            
            with col2:
                zip_data = create_zip(files, uploaded_file.name)
                st.download_button(
                    "📦 Descargar Todo",
                    data=zip_data,
                    file_name=f"{Path(uploaded_file.name).stem}_stems.zip",
                    mime="application/zip"
                )
        else:
            st.markdown(f"""
            <div class="status-error">
                <h3>❌ Error en procesamiento</h3>
                <p>{message}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("🎵 **Disband** - Con instalación automática de dependencias")

if __name__ == "__main__":
    main()
