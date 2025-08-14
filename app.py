#!/usr/bin/env python3
"""
🎵 DISBAND - Separador Rápido para Streamlit Cloud
Sin instalación manual - Todo desde GitHub
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
    
    .quick-card {
        background: white; border: 1px solid #e0e0e0;
        border-radius: 8px; padding: 1.5rem; margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
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
    </style>
    """, unsafe_allow_html=True)

# Verificar si las dependencias están disponibles
def check_dependencies():
    """Verificar que todo esté instalado correctamente desde requirements.txt"""
    try:
        # Verificar imports principales
        import demucs
        import torch
        import torchaudio
        return True, "✅ Dependencias cargadas correctamente"
    except ImportError as e:
        return False, f"❌ Error: {e.name} no encontrado. Verifica requirements.txt"

# Modelos optimizados para velocidad
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
    },
    "htdemucs": {
        "name": "🎯 Alta Calidad",
        "time": "5-8 min", 
        "desc": "Máxima calidad (más lento)"
    }
}

def separate_stems(uploaded_file, model="mdx_extra"):
    """Separar stems usando Demucs con configuración optimizada"""
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Guardar archivo subido
            input_file = temp_path / uploaded_file.name
            with open(input_file, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Directorio de salida
            output_dir = temp_path / "separated"
            
            # Comando optimizado para Streamlit Cloud
            cmd = [
                sys.executable, "-m", "demucs",
                "--model", model,
                "--out", str(output_dir),
                "--mp3",                    # Formato MP3 para velocidad
                "--mp3-bitrate", "192",     # Bitrate reducido
                "--jobs", "1",              # Solo 1 trabajo (Streamlit Cloud)
                "--device", "cpu",          # Forzar CPU
                str(input_file)
            ]
            
            # Mostrar comando para debugging (opcional)
            if st.checkbox("🔍 Mostrar comando de debug", value=False):
                st.code(" ".join(cmd))
            
            # Ejecutar separación
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=1800  # 30 minutos máximo
            )
            
            # Verificar resultado
            if process.returncode == 0:
                # Buscar archivos de salida
                model_dir = output_dir / model / input_file.stem
                
                if model_dir.exists():
                    stem_files = {}
                    for mp3_file in model_dir.glob("*.mp3"):
                        with open(mp3_file, "rb") as f:
                            stem_files[mp3_file.name] = f.read()
                    
                    if stem_files:
                        return True, stem_files, f"✅ {len(stem_files)} stems generados"
                    else:
                        return False, {}, "❌ No se generaron archivos de salida"
                else:
                    return False, {}, f"❌ Directorio de salida no encontrado: {model_dir}"
            else:
                # Mostrar error detallado
                error_msg = process.stderr if process.stderr else process.stdout
                return False, {}, f"❌ Error en separación: {error_msg}"
                
    except subprocess.TimeoutExpired:
        return False, {}, "❌ Timeout: El procesamiento tomó más de 30 minutos"
    except Exception as e:
        return False, {}, f"❌ Error inesperado: {str(e)}"

def create_zip(files, original_name):
    """Crear archivo ZIP para descarga"""
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
        <p>Separación de stems optimizada para Streamlit Cloud</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Verificar dependencias
    deps_ok, deps_msg = check_dependencies()
    
    if not deps_ok:
        st.markdown(f"""
        <div class="status-error">
            <h3>🔧 Problema de Configuración</h3>
            <p>{deps_msg}</p>
            <p><strong>Solución:</strong> Verifica que tu repositorio tenga:</p>
            <ul>
                <li><code>requirements.txt</code> con las dependencias correctas</li>
                <li><code>packages.txt</code> con <code>ffmpeg</code></li>
                <li>El deployment esté completado en Streamlit Cloud</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Mostrar información de debug
        with st.expander("🔍 Información de Debug"):
            st.write("**Python version:**", sys.version)
            st.write("**Módulos disponibles:**")
            
            modules_to_check = ["demucs", "torch", "torchaudio", "librosa", "soundfile"]
            for module in modules_to_check:
                try:
                    __import__(module)
                    st.write(f"✅ {module}: Disponible")
                except ImportError:
                    st.write(f"❌ {module}: No encontrado")
        
        return
    
    # Interfaz principal
    st.markdown(f'<div class="status-success">{deps_msg}</div>', unsafe_allow_html=True)
    
    # Sección de upload
    with st.container():
        st.markdown('<div class="quick-card">', unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "📁 Sube tu archivo de audio",
            type=['mp3', 'wav', 'flac', 'm4a', 'aac'],
            help="Máximo 200MB - Formatos: MP3, WAV, FLAC, M4A, AAC"
        )
        
        if uploaded_file:
            # Info del archivo
            size_mb = len(uploaded_file.getbuffer()) / (1024 * 1024)
            st.info(f"📄 **{uploaded_file.name}** ({size_mb:.1f} MB)")
            
            # Selección de modelo
            col1, col2 = st.columns([2, 1])
            
            with col1:
                model = st.selectbox(
                    "🤖 Velocidad de procesamiento",
                    options=list(MODELS.keys()),
                    format_func=lambda x: f"{MODELS[x]['name']} ({MODELS[x]['time']})",
                    index=0  # mdx_extra por defecto
                )
                st.caption(f"📝 {MODELS[model]['desc']}")
            
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🚀 Separar Stems", type="primary", use_container_width=True):
                    st.session_state.processing = True
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Procesamiento
    if uploaded_file and st.session_state.get('processing', False):
        st.markdown("""
        <div class="status-processing">
            <h3>⚡ Procesando audio...</h3>
            <p>Esto puede tomar unos minutos. No cierres la pestaña.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Barra de progreso visual
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Simular progreso
        for i in range(20):
            progress_bar.progress((i + 1) * 5)
            status_text.text(f"Procesando... {(i + 1) * 5}%")
            time.sleep(0.5)
        
        # Ejecutar separación
        success, files, message = separate_stems(uploaded_file, model)
        
        # Limpiar elementos de progreso
        progress_bar.empty()
        status_text.empty()
        
        # Resetear estado
        st.session_state.processing = False
        
        if success:
            # Resultados exitosos
            st.markdown(f"""
            <div class="status-success">
                <h3>🎉 ¡Separación completada!</h3>
                <p>{message}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Sección de descargas
            st.markdown("### 📥 Descargar Stems")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Stems individuales:**")
                for filename, data in files.items():
                    # Obtener tipo de stem del nombre
                    stem_type = filename.split('.')[0]
                    icons = {
                        "drums": "🥁", "bass": "🎸", "vocals": "🎤", 
                        "other": "🎹", "piano": "🎹", "guitar": "🎸"
                    }
                    icon = icons.get(stem_type, "🎵")
                    
                    st.download_button(
                        f"{icon} {filename}",
                        data=data,
                        file_name=filename,
                        mime="audio/mpeg"
                    )
            
            with col2:
                st.markdown("**Descarga completa:**")
                zip_data = create_zip(files, uploaded_file.name)
                st.download_button(
                    "📦 Descargar Todo (ZIP)",
                    data=zip_data,
                    file_name=f"{Path(uploaded_file.name).stem}_stems.zip",
                    mime="application/zip"
                )
                
                # Información adicional
                st.info(f"""
                **Archivos generados:** {len(files)}  
                **Modelo usado:** {MODELS[model]['name']}  
                **Tiempo estimado:** {MODELS[model]['time']}
                """)
        else:
            # Error en procesamiento
            st.markdown(f"""
            <div class="status-error">
                <h3>❌ Error en procesamiento</h3>
                <p>{message}</p>
                <p><strong>Soluciones:</strong></p>
                <ul>
                    <li>Intenta con un archivo más pequeño</li>
                    <li>Usa el modelo "Ultra Rápido"</li>
                    <li>Verifica que el archivo no esté dañado</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    # Tips de uso
    if not uploaded_file:
        st.markdown("### 💡 Tips de Uso")
        st.markdown("""
        - **🚀 Ultra Rápido**: Ideal para pruebas rápidas (2-3 min)
        - **⚡ Rápido**: Mejor balance calidad/velocidad (3-5 min)  
        - **🎯 Alta Calidad**: Máximos resultados (5-8 min)
        - **📁 Archivos**: MP3 menores a 50MB procesan más rápido
        - **💾 Memoria**: El proceso usa CPU únicamente
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("🎵 **Disband Rápido** - Optimizado para Streamlit Cloud")

if __name__ == "__main__":
    main()
