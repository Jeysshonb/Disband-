#!/usr/bin/env python3
"""
🎵 DISBAND - Separador de Stems con IA
Creado por @jeysshon

FUNCIONA INMEDIATAMENTE - Sin instalaciones, sin esperas
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
    page_title="🎵 Disband - Separador de Stems",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS moderno
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.stApp {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.hero-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 3rem 2rem;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 2rem;
    color: white;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 700;
    margin: 0;
    text-shadow: 0 2px 10px rgba(0,0,0,0.3);
}

.hero-subtitle {
    font-size: 1.3rem;
    opacity: 0.9;
    margin: 1rem 0 0 0;
}

.upload-container {
    background: white;
    padding: 2rem;
    border-radius: 16px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    margin-bottom: 2rem;
}

.processing-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 16px;
    color: white;
    text-align: center;
    margin: 2rem 0;
}

.processing-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}

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
}

.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.75rem 2rem;
    font-weight: 600;
    font-size: 1rem;
    transition: all 0.3s ease;
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
}

.file-info {
    background: linear-gradient(135deg, #17a2b8 0%, #138496 100%);
    color: white;
    padding: 1rem;
    border-radius: 12px;
    margin: 1rem 0;
}

.feature-card {
    background: white;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    border-left: 4px solid #667eea;
    margin: 1rem 0;
}

[data-testid="metric-container"] {
    background: white;
    border: 1px solid #e8f0ff;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

def separate_audio(uploaded_file):
    """Separar audio usando Demucs - FUNCIÓN PRINCIPAL"""
    
    # Crear directorio temporal
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        
        # Guardar archivo subido
        input_path = temp_dir / uploaded_file.name
        with open(input_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Directorio de salida
        output_dir = temp_dir / "output"
        output_dir.mkdir()
        
        # Comando Demucs (MÁXIMA CALIDAD SIEMPRE)
        cmd = [
            sys.executable, "-m", "demucs",
            "--model", "htdemucs_ft",  # Mejor modelo
            "--out", str(output_dir),
            "--float32",  # Mejor calidad
            str(input_path)
        ]
        
        # Mostrar progreso
        progress_placeholder = st.empty()
        status_placeholder = st.empty()
        log_placeholder = st.empty()
        
        # Ejecutar separación
        with progress_placeholder.container():
            st.markdown("""
            <div class="processing-container">
                <div class="processing-icon">🎵</div>
                <h3>🚀 IA Trabajando en Tu Música</h3>
                <p><strong>Separando con Calidad Profesional</strong></p>
                <p>Tiempo estimado: 15-30 minutos</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Barra de progreso
        progress_bar = st.progress(0)
        
        try:
            # Ejecutar proceso
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                universal_newlines=True
            )
            
            # Leer output en tiempo real
            progress = 10
            status_placeholder.text("🔄 Iniciando separación...")
            progress_bar.progress(progress)
            
            logs = []
            for line in process.stdout:
                line = line.strip()
                if line:
                    logs.append(line)
                    
                    # Actualizar progreso basado en keywords
                    if any(word in line.lower() for word in ['loading', 'model']):
                        if progress < 30:
                            status_placeholder.text("📂 Cargando modelo de IA...")
                            progress_bar.progress(30)
                            progress = 30
                    elif any(word in line.lower() for word in ['separate', 'processing']):
                        if progress < 70:
                            status_placeholder.text("🎯 Separando instrumentos...")
                            progress_bar.progress(70)
                            progress = 70
                    elif any(word in line.lower() for word in ['saving', 'writing']):
                        if progress < 90:
                            status_placeholder.text("💾 Guardando stems...")
                            progress_bar.progress(90)
                            progress = 90
                    
                    # Mostrar logs recientes
                    if len(logs) > 10:
                        logs.pop(0)
                    
                    with log_placeholder.container():
                        if logs:
                            st.code('\n'.join(logs[-3:]), language='text')
            
            # Esperar que termine
            process.wait()
            
            # Finalizar progreso
            status_placeholder.text("✅ ¡Separación completada!")
            progress_bar.progress(100)
            
            # Limpiar indicadores
            time.sleep(2)
            progress_placeholder.empty()
            status_placeholder.empty()
            log_placeholder.empty()
            progress_bar.empty()
            
            if process.returncode == 0:
                # Buscar archivos generados
                stem_folder = output_dir / "htdemucs_ft" / input_path.stem
                
                if stem_folder.exists():
                    # Leer archivos WAV
                    stem_files = {}
                    for stem_file in stem_folder.glob("*.wav"):
                        with open(stem_file, "rb") as f:
                            stem_files[stem_file.name] = f.read()
                    
                    return True, stem_files, f"🎉 ¡{len(stem_files)} stems generados!"
                else:
                    return False, {}, "❌ No se encontraron archivos de salida"
            else:
                return False, {}, f"❌ Error en separación (código: {process.returncode})"
                
        except Exception as e:
            return False, {}, f"❌ Error: {str(e)}"

def create_zip_download(stem_files, original_filename):
    """Crear ZIP para descarga"""
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for filename, file_data in stem_files.items():
            zip_file.writestr(f"{Path(original_filename).stem}_stems/{filename}", file_data)
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue()

def main():
    """Aplicación principal"""
    
    # Inicializar estado
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    if 'stems_ready' not in st.session_state:
        st.session_state.stems_ready = False
    if 'stem_files' not in st.session_state:
        st.session_state.stem_files = {}
    
    # Verificar que Demucs esté disponible
    try:
        import demucs
        deps_ok = True
    except ImportError:
        deps_ok = False
    
    # Header
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">🎵 Disband</h1>
        <p class="hero-subtitle">Separador de Stems con IA Profesional</p>
        <p>Creado por @jeysshon</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Si dependencias no están listas
    if not deps_ok:
        st.error("""
        🔧 **Streamlit Cloud aún está instalando dependencias**
        
        **Esto es normal en el primer deployment.**
        
        ⏰ **Tiempo estimado:** 5-10 minutos  
        🔄 **Qué hacer:** Espera y refresca la página  
        ✅ **Después:** La app funcionará instantáneamente
        """)
        
        if st.button("🔄 Verificar de Nuevo"):
            st.rerun()
        return
    
    # Interface principal
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Sección de subida
        st.markdown("""
        <div class="upload-container">
            <h2 style="margin-top: 0; color: #333;">📁 Sube Tu Música</h2>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Arrastra tu archivo o haz click para buscar",
            type=['mp3', 'wav', 'flac', 'm4a', 'aac'],
            help="Formatos: MP3, WAV, FLAC, M4A, AAC",
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            # Info del archivo
            file_size_mb = len(uploaded_file.getbuffer()) / (1024 * 1024)
            st.markdown(f"""
            <div class="file-info">
                <h4>📄 {uploaded_file.name}</h4>
                <p>📏 Tamaño: {file_size_mb:.1f} MB | 🎵 Tipo: {uploaded_file.type}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Configuración automática
            st.markdown("### ⚡ Configuración Automática")
            st.success("""
            **🏆 Modelo:** Máxima Calidad (htdemucs_ft)  
            **💎 Formato:** WAV (Sin pérdida)  
            **⏱️ Tiempo:** ~15-30 minutos  
            **🎯 Resultado:** Calidad profesional
            """)
            
            # Botón de procesamiento
            if not st.session_state.processing and not st.session_state.stems_ready:
                if st.button("🚀 Separar con Máxima Calidad", use_container_width=True, type="primary"):
                    st.session_state.processing = True
                    st.session_state.stems_ready = False
                    st.session_state.stem_files = {}
                    st.rerun()
            elif st.session_state.processing:
                st.button("🎵 Procesando...", disabled=True, use_container_width=True)
            else:
                if st.button("🔄 Procesar Otra Canción", use_container_width=True):
                    st.session_state.processing = False
                    st.session_state.stems_ready = False
                    st.session_state.stem_files = {}
                    st.rerun()
    
    with col2:
        # Estadísticas
        st.markdown("### 📊 Stats")
        
        if uploaded_file:
            st.metric("⏱️ Tiempo", "15-30 min")
            st.metric("🏆 Calidad", "⭐⭐⭐⭐⭐")
            st.metric("📏 Tamaño", f"{file_size_mb:.1f} MB")
        else:
            st.info("👆 Sube un archivo para empezar")
        
        # Info de resultados
        st.markdown("### 🎯 Qué Obtienes")
        st.markdown("""
        <div class="feature-card">
            <strong>🥁 Drums:</strong><br>
            Batería aislada perfecta
        </div>
        <div class="feature-card">
            <strong>🎸 Bass:</strong><br>
            Bajo limpio y definido
        </div>
        <div class="feature-card">
            <strong>🎤 Vocals:</strong><br>
            Voces sin instrumentos
        </div>
        <div class="feature-card">
            <strong>🎹 Other:</strong><br>
            Instrumentos y guitarras
        </div>
        """, unsafe_allow_html=True)
    
    # Procesamiento
    if st.session_state.processing and uploaded_file:
        success, stem_files, message = separate_audio(uploaded_file)
        
        if success:
            st.session_state.stem_files = stem_files
            st.session_state.stems_ready = True
            st.session_state.processing = False
            st.rerun()
        else:
            st.session_state.processing = False
            st.error(message)
    
    # Resultados
    if st.session_state.stems_ready and st.session_state.stem_files:
        st.markdown("""
        <div class="results-container">
            <h2>🎉 ¡Separación Completada!</h2>
            <p>Tus stems están listos para descargar</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 🎵 Stems Generados")
            
            stem_icons = {
                "drums": "🥁",
                "bass": "🎸", 
                "vocals": "🎤",
                "other": "🎹"
            }
            
            for filename in st.session_state.stem_files.keys():
                stem_type = filename.split('.')[0]
                icon = stem_icons.get(stem_type, "🎵")
                
                st.markdown(f"""
                <div class="stem-item">
                    <span style="font-size: 1.5rem; margin-right: 1rem;">{icon}</span>
                    <strong>{filename}</strong>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 💾 Descargas")
            
            # Descargas individuales
            for filename, file_data in st.session_state.stem_files.items():
                st.download_button(
                    label=f"⬇️ {filename}",
                    data=file_data,
                    file_name=filename,
                    mime="audio/wav"
                )
            
            # Descarga ZIP
            if uploaded_file:
                zip_data = create_zip_download(st.session_state.stem_files, uploaded_file.name)
                st.download_button(
                    label="📦 Descargar Todo (ZIP)",
                    data=zip_data,
                    file_name=f"{Path(uploaded_file.name).stem}_stems.zip",
                    mime="application/zip"
                )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem 0;">
        <p>🎵 <strong>Disband</strong> - Creado con ❤️ por <strong>@jeysshon</strong></p>
        <p>Powered by Demucs AI • Gratis & Open Source • Privacy First</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
