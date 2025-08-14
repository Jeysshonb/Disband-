import streamlit as st
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from io import BytesIO
import time

# Configuración básica
st.set_page_config(
    page_title="Disband - Separador de Stems",
    page_icon="🎵",
    layout="centered"
)

# CSS simple y bonito
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
    .upload-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .status-box {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2196f3;
        margin: 1rem 0;
    }
    .success-box {
        background: #e8f5e8;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4caf50;
        margin: 1rem 0;
    }
    .processing-box {
        background: #fff3e0;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ff9800;
        margin: 1rem 0;
        text-align: center;
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
    """Inicializar variables de sesión"""
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    if 'completed' not in st.session_state:
        st.session_state.completed = False
    if 'stems' not in st.session_state:
        st.session_state.stems = {}

def check_ready():
    """Verificar si está todo listo"""
    try:
        import demucs
        return True
    except ImportError:
        return False

def process_audio(uploaded_file):
    """Procesar audio y mostrar progreso en tiempo real"""
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Guardar archivo
        input_file = temp_path / uploaded_file.name
        with open(input_file, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Configurar salida
        output_dir = temp_path / "separated"
        output_dir.mkdir()
        
        # Comando demucs
        cmd = [
            sys.executable, "-m", "demucs",
            "--model", "htdemucs",
            "--out", str(output_dir),
            "--mp3",
            str(input_file)
        ]
        
        # Contenedores para mostrar progreso
        status_container = st.empty()
        progress_container = st.empty()
        log_container = st.empty()
        
        # Mostrar estado inicial
        with status_container.container():
            st.markdown("""
            <div class="processing-box">
                <h3>🎵 Procesando tu música</h3>
                <p>Esto tomará unos minutos...</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Barra de progreso
        progress_bar = progress_container.progress(0)
        
        try:
            # Ejecutar demucs
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                universal_newlines=True
            )
            
            # Leer output en tiempo real
            current_progress = 0
            logs = []
            
            for line in process.stdout:
                line = line.strip()
                if line:
                    logs.append(line)
                    
                    # Actualizar progreso
                    if "Loading" in line and current_progress < 30:
                        progress_bar.progress(30)
                        current_progress = 30
                        with log_container:
                            st.text("📥 Cargando modelo...")
                    elif "Separating" in line and current_progress < 70:
                        progress_bar.progress(70)
                        current_progress = 70
                        with log_container:
                            st.text("🎯 Separando instrumentos...")
                    elif "Saving" in line and current_progress < 90:
                        progress_bar.progress(90)
                        current_progress = 90
                        with log_container:
                            st.text("💾 Guardando archivos...")
                    
                    # Mostrar logs recientes
                    if len(logs) > 8:
                        logs.pop(0)
                    
                    with log_container:
                        st.code('\n'.join(logs[-3:]))
            
            # Esperar finalización
            process.wait()
            
            # Completar progreso
            progress_bar.progress(100)
            with log_container:
                st.text("✅ ¡Completado!")
            
            time.sleep(1)
            
            # Limpiar indicadores
            status_container.empty()
            progress_container.empty()
            log_container.empty()
            
            if process.returncode == 0:
                # Buscar archivos separados
                model_dir = output_dir / "htdemucs" / input_file.stem
                
                if model_dir.exists():
                    stem_files = {}
                    for mp3_file in model_dir.glob("*.mp3"):
                        with open(mp3_file, "rb") as f:
                            stem_files[mp3_file.name] = f.read()
                    
                    return True, stem_files
                else:
                    st.error("❌ No se encontraron archivos separados")
                    return False, {}
            else:
                st.error(f"❌ Error en el procesamiento (código {process.returncode})")
                return False, {}
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            return False, {}

def create_download_zip(stems, filename):
    """Crear ZIP para descarga"""
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        for stem_name, stem_data in stems.items():
            zf.writestr(f"{Path(filename).stem}_separado/{stem_name}", stem_data)
    zip_buffer.seek(0)
    return zip_buffer.getvalue()

def main():
    """Aplicación principal"""
    init_session()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎵 Disband</h1>
        <h3>Separador de Stems Profesional</h3>
        <p>Por @jeysshon - Rápido, Simple, Efectivo</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Verificar estado
    if not check_ready():
        st.markdown("""
        <div class="status-box">
            <h4>⏳ Preparando la aplicación...</h4>
            <p>Streamlit está instalando las dependencias. Esto toma unos minutos la primera vez.</p>
            <p><strong>Refresca la página en 2-3 minutos.</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Verificar"):
            st.rerun()
        return
    
    # Interface principal
    if not st.session_state.completed:
        st.markdown("""
        <div class="upload-section">
            <h3>📁 Sube tu música</h3>
            <p>Formatos: MP3, WAV, FLAC, M4A</p>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Selecciona tu archivo",
            type=['mp3', 'wav', 'flac', 'm4a'],
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            # Info del archivo
            file_size = len(uploaded_file.getbuffer()) / (1024 * 1024)
            
            st.markdown(f"""
            <div class="success-box">
                <strong>📄 {uploaded_file.name}</strong><br>
                📏 Tamaño: {file_size:.1f} MB<br>
                🎵 Tipo: {uploaded_file.type}
            </div>
            """, unsafe_allow_html=True)
            
            # Configuración
            st.markdown("### ⚙️ Configuración")
            col1, col2 = st.columns(2)
            with col1:
                st.info("🎯 **Modelo:** htdemucs (Balanceado)")
            with col2:
                st.info("💾 **Formato:** MP3 320kbps")
            
            # Botón procesar
            if not st.session_state.processing:
                if st.button("🚀 Separar Stems", type="primary", use_container_width=True):
                    st.session_state.processing = True
                    st.rerun()
            else:
                # Procesar archivo
                success, stems = process_audio(uploaded_file)
                
                if success and stems:
                    st.session_state.stems = stems
                    st.session_state.completed = True
                    st.session_state.processing = False
                    st.rerun()
                else:
                    st.session_state.processing = False
    
    # Mostrar resultados
    if st.session_state.completed and st.session_state.stems:
        st.markdown("""
        <div class="success-box">
            <h3>🎉 ¡Separación completada!</h3>
            <p>Tus stems están listos para descargar</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Lista de stems
        st.markdown("### 🎵 Archivos separados:")
        
        stem_icons = {
            "drums": "🥁",
            "bass": "🎸",
            "vocals": "🎤", 
            "other": "🎹"
        }
        
        for stem_name in st.session_state.stems.keys():
            stem_type = stem_name.split('.')[0]
            icon = stem_icons.get(stem_type, "🎵")
            
            st.markdown(f"""
            <div class="stem-file">
                <span style="font-size: 1.5em; margin-right: 10px;">{icon}</span>
                <strong>{stem_name}</strong>
            </div>
            """, unsafe_allow_html=True)
        
        # Descargas
        st.markdown("### 💾 Descargar:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Archivos individuales:**")
            for stem_name, stem_data in st.session_state.stems.items():
                st.download_button(
                    f"⬇️ {stem_name}",
                    data=stem_data,
                    file_name=stem_name,
                    mime="audio/mpeg"
                )
        
        with col2:
            st.markdown("**Todo junto:**")
            if uploaded_file:
                zip_data = create_download_zip(st.session_state.stems, uploaded_file.name)
                st.download_button(
                    "📦 Descargar ZIP",
                    data=zip_data,
                    file_name=f"{Path(uploaded_file.name).stem}_stems.zip",
                    mime="application/zip"
                )
        
        # Botón para nueva separación
        if st.button("🔄 Separar otra canción"):
            st.session_state.processing = False
            st.session_state.completed = False
            st.session_state.stems = {}
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p><strong>Disband</strong> - Creado por @jeysshon</p>
        <p>Gratis • Rápido • Sin límites</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
