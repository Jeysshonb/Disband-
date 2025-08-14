import streamlit as st
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from io import BytesIO
import time
import os

# Configuración
st.set_page_config(
    page_title="Disband - Separador Rápido",
    page_icon="🎵",
    layout="centered"
)

# CSS simple
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .status-ok {
        background: #e8f5e8;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4caf50;
        margin: 1rem 0;
    }
    .processing {
        background: #fff3e0;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #ff9800;
        margin: 1rem 0;
        text-align: center;
    }
    .results {
        background: #e8f5e8;
        padding: 1.5rem;
        border-radius: 8px;
        color: #2e7d32;
        margin: 1rem 0;
    }
    .stem-file {
        background: white;
        padding: 0.8rem;
        margin: 0.3rem 0;
        border-radius: 5px;
        border-left: 3px solid #4ECDC4;
        display: flex;
        align-items: center;
    }
</style>
""", unsafe_allow_html=True)

def init_session():
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    if 'completed' not in st.session_state:
        st.session_state.completed = False
    if 'stems' not in st.session_state:
        st.session_state.stems = {}

def check_separator():
    """Verificar si audio-separator está listo"""
    try:
        result = subprocess.run([sys.executable, "-c", "from audio_separator import Separator"], 
                               capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def separate_audio(uploaded_file):
    """Separar con audio-separator"""
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Guardar archivo
        input_file = temp_path / uploaded_file.name
        with open(input_file, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Configurar salida
        output_dir = temp_path / "separated"
        output_dir.mkdir()
        
        # Comando audio-separator
        cmd = [
            sys.executable, "-m", "audio_separator",
            str(input_file),
            "--output_dir", str(output_dir),
            "--model_name", "UVR_MDXNET_KARA_2",
            "--output_format", "mp3"
        ]
        
        # Mostrar progreso
        status_container = st.empty()
        progress_container = st.empty()
        log_container = st.empty()
        
        with status_container.container():
            st.markdown("""
            <div class="processing">
                <h3>🚀 Separando Audio</h3>
                <p>Usando IA moderna y rápida</p>
            </div>
            """, unsafe_allow_html=True)
        
        progress_bar = progress_container.progress(0)
        
        try:
            # Ejecutar separador
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            
            current_progress = 10
            progress_bar.progress(current_progress)
            
            logs = []
            for line in process.stdout:
                line = line.strip()
                if line:
                    logs.append(line)
                    
                    # Actualizar progreso
                    if "processing" in line.lower() and current_progress < 30:
                        current_progress = 30
                        progress_bar.progress(current_progress)
                        with log_container:
                            st.text("🎯 Iniciando separación...")
                    elif "separating" in line.lower() and current_progress < 70:
                        current_progress = 70
                        progress_bar.progress(current_progress)
                        with log_container:
                            st.text("🎵 Separando instrumentos...")
                    elif "saving" in line.lower() or "done" in line.lower():
                        current_progress = 90
                        progress_bar.progress(current_progress)
                        with log_container:
                            st.text("💾 Guardando archivos...")
                    
                    # Mostrar logs
                    if len(logs) > 5:
                        logs.pop(0)
                    
                    with log_container:
                        st.code('\n'.join(logs[-2:]))
            
            process.wait()
            progress_bar.progress(100)
            
            time.sleep(1)
            status_container.empty()
            progress_container.empty()
            log_container.empty()
            
            if process.returncode == 0:
                # Buscar archivos separados
                stem_files = {}
                
                # Buscar todos los archivos MP3 en el directorio de salida
                for mp3_file in output_dir.rglob("*.mp3"):
                    with open(mp3_file, "rb") as f:
                        stem_files[mp3_file.name] = f.read()
                
                if stem_files:
                    return True, stem_files
                else:
                    st.error("❌ No se encontraron archivos separados")
                    return False, {}
            else:
                st.error("❌ Error en separación")
                return False, {}
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            return False, {}

def create_zip(stems, filename):
    """Crear ZIP"""
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zf:
        for name, data in stems.items():
            zf.writestr(f"{Path(filename).stem}_stems/{name}", data)
    zip_buffer.seek(0)
    return zip_buffer.getvalue()

def main():
    init_session()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎵 Disband</h1>
        <h3>Separador Moderno de Stems</h3>
        <p>Por @jeysshon - IA de última generación</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Verificar separador
    if not check_separator():
        st.warning("⚡ Instalando separador de audio...")
        st.info("Esto toma unos minutos la primera vez. Refresca la página en 2-3 minutos.")
        
        if st.button("🔄 Verificar"):
            st.rerun()
        return
    
    # Mostrar que está listo
    st.markdown("""
    <div class="status-ok">
        <h4>✅ ¡Listo para separar!</h4>
        <p>Separador de audio instalado y funcionando</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Interface principal
    if not st.session_state.completed:
        st.markdown("### 📁 Sube tu música")
        
        uploaded_file = st.file_uploader(
            "Selecciona archivo",
            type=['mp3', 'wav', 'flac', 'm4a'],
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            file_size = len(uploaded_file.getbuffer()) / (1024 * 1024)
            
            st.success(f"""
            **📄 {uploaded_file.name}**  
            📏 Tamaño: {file_size:.1f} MB  
            ⚡ Tiempo estimado: 3-8 minutos
            """)
            
            if not st.session_state.processing:
                if st.button("🚀 Separar Ahora", type="primary", use_container_width=True):
                    st.session_state.processing = True
                    st.rerun()
            else:
                # Procesar
                success, stems = separate_audio(uploaded_file)
                
                if success:
                    st.session_state.stems = stems
                    st.session_state.completed = True
                    st.session_state.processing = False
                    st.rerun()
                else:
                    st.session_state.processing = False
    
    # Resultados
    if st.session_state.completed and st.session_state.stems:
        st.markdown("""
        <div class="results">
            <h3>🎉 ¡Separación completada!</h3>
            <p>Tus stems están listos</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Mostrar stems
        stem_icons = {
            "vocals": "🎤",
            "instrumental": "🎹",
            "drums": "🥁", 
            "bass": "🎸",
            "other": "🎵"
        }
        
        for stem_name in st.session_state.stems.keys():
            # Detectar tipo de stem basado en el nombre del archivo
            stem_type = "other"
            for key in stem_icons.keys():
                if key in stem_name.lower():
                    stem_type = key
                    break
            
            icon = stem_icons.get(stem_type, "🎵")
            
            st.markdown(f"""
            <div class="stem-file">
                <span style="font-size: 1.5em; margin-right: 10px;">{icon}</span>
                <strong>{stem_name}</strong>
            </div>
            """, unsafe_allow_html=True)
        
        # Descargas
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Individuales:**")
            for name, data in st.session_state.stems.items():
                st.download_button(
                    f"⬇️ {name}",
                    data=data,
                    file_name=name,
                    mime="audio/mpeg"
                )
        
        with col2:
            st.markdown("**Todo junto:**")
            if uploaded_file:
                zip_data = create_zip(st.session_state.stems, uploaded_file.name)
                st.download_button(
                    "📦 ZIP completo",
                    data=zip_data,
                    file_name=f"{Path(uploaded_file.name).stem}_stems.zip"
                )
        
        if st.button("🔄 Separar otra"):
            st.session_state.processing = False
            st.session_state.completed = False
            st.session_state.stems = {}
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("**Disband** por @jeysshon • Separación moderna de audio")

if __name__ == "__main__":
    main()
