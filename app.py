#!/usr/bin/env python3
"""
🎵 DISBAND - Separación Local REAL
Usando Spleeter que funciona sin APIs
"""

import streamlit as st
import subprocess
import sys
import tempfile
import os
import zipfile
from pathlib import Path
from io import BytesIO
import time

# Configuración de página
st.set_page_config(
    page_title="🎵 Disband - Local AI",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def load_css():
    st.markdown("""
    <style>
    .stApp { font-family: -apple-system, BlinkMacSystemFont, sans-serif; }
    #MainMenu, footer, header { visibility: hidden; }
    
    .hero-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem; border-radius: 20px; text-align: center;
        margin-bottom: 2rem; color: white;
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

def check_and_install_spleeter():
    """Verificar e instalar Spleeter si es necesario"""
    try:
        # Verificar si Spleeter está instalado
        import spleeter
        return True, "✅ Spleeter ya instalado"
    except ImportError:
        # Instalar Spleeter
        st.info("📦 Instalando Spleeter por primera vez...")
        try:
            # Instalar tensorflow (CPU)
            subprocess.run([
                sys.executable, "-m", "pip", "install", 
                "tensorflow==2.10.0", "--quiet"
            ], check=True)
            
            # Instalar spleeter
            subprocess.run([
                sys.executable, "-m", "pip", "install", 
                "spleeter==2.3.2", "--quiet"
            ], check=True)
            
            # Instalar ffmpeg-python
            subprocess.run([
                sys.executable, "-m", "pip", "install", 
                "ffmpeg-python", "--quiet"
            ], check=True)
            
            return True, "✅ Spleeter instalado correctamente"
            
        except subprocess.CalledProcessError as e:
            return False, f"❌ Error instalando Spleeter: {e}"

def separate_with_spleeter(uploaded_file, stems_count=2):
    """Separar audio usando Spleeter local"""
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Guardar archivo subido
            input_file = temp_path / uploaded_file.name
            with open(input_file, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Directorio de salida
            output_dir = temp_path / "output"
            output_dir.mkdir()
            
            # Comando Spleeter
            stems_config = f"spleeter:{stems_count}stems-16kHz"
            
            cmd = [
                sys.executable, "-m", "spleeter", "separate",
                str(input_file),
                "-p", stems_config,
                "-o", str(output_dir)
            ]
            
            st.info(f"🎯 Ejecutando: spleeter separate con {stems_count} stems")
            
            # Ejecutar Spleeter
            process = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=600  # 10 minutos máximo
            )
            
            if process.returncode == 0:
                # Buscar archivos generados
                stem_folder = output_dir / input_file.stem
                
                if stem_folder.exists():
                    stem_files = {}
                    
                    # Leer archivos WAV generados
                    for wav_file in stem_folder.glob("*.wav"):
                        with open(wav_file, "rb") as f:
                            stem_files[wav_file.name] = f.read()
                    
                    if stem_files:
                        return True, stem_files, f"✅ {len(stem_files)} stems generados localmente"
                    else:
                        return False, {}, "❌ No se encontraron archivos de salida"
                else:
                    return False, {}, f"❌ Directorio no encontrado: {stem_folder}"
            else:
                error_msg = process.stderr if process.stderr else "Error desconocido"
                return False, {}, f"❌ Error Spleeter: {error_msg}"
                
    except subprocess.TimeoutExpired:
        return False, {}, "❌ Timeout: Procesamiento tomó más de 10 minutos"
    except Exception as e:
        return False, {}, f"❌ Error: {str(e)}"

def create_download_zip(stems_dict, original_name):
    """Crear ZIP con stems para descarga"""
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for filename, file_data in stems_dict.items():
            # Asegurar que file_data es bytes
            if isinstance(file_data, bytes):
                zip_file.writestr(filename, file_data)
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue()

def main():
    load_css()
    
    # Header
    st.markdown("""
    <div class="hero-container">
        <h1 style="font-size: 3.5rem; font-weight: 700; margin: 0;">🎵 Disband</h1>
        <p style="font-size: 1.3rem; margin: 1rem 0 0 0;">Separación Local con Spleeter</p>
        <p style="font-size: 1rem; margin: 0.5rem 0 0 0; opacity: 0.8;">IA real funcionando en el servidor</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Verificar/instalar Spleeter
    spleeter_ok, spleeter_msg = check_and_install_spleeter()
    
    if not spleeter_ok:
        st.markdown(f"""
        <div class="status-error">
            <h3>🔧 Error de Instalación</h3>
            <p>{spleeter_msg}</p>
            <p>Recarga la página e intenta de nuevo.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Mostrar estado
    st.markdown(f'<div class="status-success">{spleeter_msg}</div>', unsafe_allow_html=True)
    
    # Interfaz principal
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📁 Subir Audio para Separación Local")
        
        uploaded_file = st.file_uploader(
            "Selecciona tu archivo de audio",
            type=['mp3', 'wav', 'flac', 'm4a'],
            help="Procesamiento 100% local con Spleeter"
        )
        
        if uploaded_file:
            file_size_mb = len(uploaded_file.getbuffer()) / (1024 * 1024)
            st.success(f"✅ **{uploaded_file.name}** ({file_size_mb:.1f} MB)")
            
            # Configuración de stems
            stems_option = st.selectbox(
                "🎯 Tipo de separación:",
                [2, 4, 5],
                format_func=lambda x: {
                    2: "🎤 2 stems: Vocals + Accompaniment",
                    4: "🎵 4 stems: Vocals + Drums + Bass + Other", 
                    5: "🎼 5 stems: Vocals + Drums + Bass + Piano + Other"
                }[x],
                index=0
            )
            
            if st.button("🚀 Separar con IA Local", type="primary", use_container_width=True):
                st.session_state.processing = True
                st.session_state.uploaded_file = uploaded_file
                st.session_state.stems_count = stems_option
                st.rerun()
    
    with col2:
        st.markdown("### 📊 Información")
        if uploaded_file:
            st.metric("Tamaño", f"{file_size_mb:.1f} MB")
            st.metric("Método", "Spleeter (Local)")
            st.metric("Costo", "🆓 Gratis")
        
        st.markdown("### ⚡ Características")
        st.markdown("""
        - 🏠 **100% Local** - Todo en el servidor
        - 🤖 **IA Real** - Spleeter de Deezer
        - 🆓 **Gratis** - Sin APIs externas
        - ⚡ **Rápido** - 3-8 minutos
        - 🎯 **2, 4 o 5 stems** según elijas
        - 📦 **Descarga ZIP** automática
        """)
    
    # Procesamiento
    if st.session_state.get('processing', False):
        uploaded_file = st.session_state.get('uploaded_file')
        stems_count = st.session_state.get('stems_count', 2)
        
        st.markdown(f"""
        <div class="status-processing">
            <h3>🎯 Separando con Spleeter ({stems_count} stems)</h3>
            <p>IA funcionando localmente en el servidor...</p>
            <p>Esto puede tomar 3-8 minutos según el tamaño del archivo</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Ejecutar separación
        with st.spinner(f"🤖 Spleeter procesando {stems_count} stems..."):
            success, stems, message = separate_with_spleeter(uploaded_file, stems_count)
        
        # Reset estado
        st.session_state.processing = False
        
        if success:
            st.session_state.stems = stems
            st.session_state.stems_count = stems_count
            
            st.markdown(f"""
            <div class="status-success">
                <h3>🎉 ¡Separación Completada!</h3>
                <p>{message}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="status-error">
                <h3>❌ Error en Separación</h3>
                <p>{message}</p>
                <p><strong>Posibles soluciones:</strong></p>
                <ul>
                    <li>Intenta con un archivo más pequeño</li>
                    <li>Usa formato MP3 o WAV</li>
                    <li>Prueba con 2 stems en lugar de 4 o 5</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    # Mostrar resultados
    if st.session_state.get('stems'):
        stems = st.session_state.stems
        stems_count = st.session_state.get('stems_count', 2)
        
        st.markdown("### 🎵 Stems Generados")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📁 Descargas Individuales:**")
            
            # Iconos para tipos de stems
            stem_icons = {
                "vocals": "🎤",
                "accompaniment": "🎹", 
                "drums": "🥁",
                "bass": "🎸",
                "other": "🎼",
                "piano": "🎹"
            }
            
            for filename, file_data in stems.items():
                # Extraer tipo de stem del nombre de archivo
                stem_type = filename.replace('.wav', '').lower()
                icon = stem_icons.get(stem_type, "🎵")
                
                st.markdown(f"{icon} **{filename}**")
                
                # Botón de descarga individual
                st.download_button(
                    f"⬇️ Descargar {filename}",
                    data=file_data,
                    file_name=filename,
                    mime="audio/wav",
                    key=f"download_{filename}"
                )
        
        with col2:
            st.markdown("**📦 Descarga Completa:**")
            
            # Información de los stems
            st.info(f"""
            **📊 Información:**
            - **Stems generados:** {len(stems)}
            - **Formato:** WAV alta calidad
            - **Modelo:** Spleeter {stems_count}-stems
            - **Procesamiento:** 100% local
            """)
            
            # ZIP download
            if st.button("📦 Crear ZIP de Todos los Stems"):
                with st.spinner("📦 Creando archivo ZIP..."):
                    zip_data = create_download_zip(stems, uploaded_file.name)
                    
                    st.download_button(
                        "⬇️ Descargar ZIP Completo",
                        data=zip_data,
                        file_name=f"{Path(uploaded_file.name).stem}_stems.zip",
                        mime="application/zip"
                    )
        
        # Botón para procesar otro archivo
        if st.button("🔄 Procesar Otro Archivo", use_container_width=True):
            for key in ['processing', 'stems', 'uploaded_file', 'stems_count']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    # Información técnica
    with st.expander("🔬 Información Técnica"):
        st.markdown("""
        ### 🤖 Sobre Spleeter
        
        **Spleeter** es la librería de separación de fuentes de **Deezer** (como Spotify):
        - Desarrollado por Deezer Research
        - Usado en producción por Deezer
        - Open source y gratuito
        - Funciona completamente offline
        
        ### 📊 Modelos Disponibles
        
        - **2-stems**: Vocals + Accompaniment (más rápido)
        - **4-stems**: Vocals + Drums + Bass + Other (balanceado)  
        - **5-stems**: + Piano separado (más detallado)
        
        ### ⚡ Rendimiento
        
        - **CPU**: Funciona sin GPU (más lento pero compatible)
        - **Tiempo**: 3-8 minutos según archivo y stems
        - **Calidad**: Profesional, usado por Deezer
        - **Memoria**: ~2-4GB durante procesamiento
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem 0;">
        <p>🎵 <strong>Disband</strong> - Separación local con Spleeter</p>
        <p>Powered by Deezer Research • 100% Local • Open Source</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
