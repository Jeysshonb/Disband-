import streamlit as st
import subprocess
import sys
import os
import tempfile
import zipfile
from pathlib import Path
from io import BytesIO

st.set_page_config(
    page_title="🎵 Disband Simple",
    page_icon="🎵",
    layout="centered"
)

# CSS simple
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #667eea, #764ba2);
    padding: 2rem; border-radius: 12px; color: white;
    text-align: center; margin-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)

def install_if_missing():
    """Instalar solo lo que falta, versión por versión"""
    
    # Verificar qué falta
    missing = []
    
    try:
        import torch
        st.success(f"✅ PyTorch {torch.__version__}")
    except ImportError:
        missing.append("torch")
    
    try:
        import demucs
        st.success(f"✅ Demucs disponible")
    except ImportError:
        missing.append("demucs")
    
    if not missing:
        return True, "✅ Todo instalado"
    
    st.info(f"Instalando: {', '.join(missing)}")
    
    # Instalar uno por uno con configuración específica
    for package in missing:
        try:
            if package == "torch":
                # PyTorch versión compatible con Python 3.13
                cmd = [sys.executable, "-m", "pip", "install", 
                      "torch>=2.5.0", "torchaudio>=2.5.0", 
                      "--index-url", "https://download.pytorch.org/whl/cpu",
                      "--no-cache-dir"]
            elif package == "demucs":
                cmd = [sys.executable, "-m", "pip", "install", 
                      "demucs", "--no-cache-dir"]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            if result.returncode != 0:
                st.error(f"Error instalando {package}: {result.stderr}")
                return False, f"Error en {package}"
            else:
                st.success(f"✅ {package} instalado")
                
        except Exception as e:
            st.error(f"Excepción instalando {package}: {e}")
            return False, f"Excepción en {package}"
    
    return True, "✅ Instalación completada"

def check_everything():
    """Verificar que todo esté funcionando"""
    try:
        import demucs
        import torch
        import torchaudio
        
        # Verificar que demucs funcione
        from demucs.pretrained import get_model_from_args
        
        return True, "✅ Demucs funcionando correctamente"
    except Exception as e:
        return False, f"❌ Error: {e}"

def separate_audio(uploaded_file):
    """Separar audio con configuración mínima"""
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Guardar archivo
            input_file = temp_path / uploaded_file.name
            with open(input_file, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            output_dir = temp_path / "output"
            
            # Comando más simple posible
            cmd = [
                sys.executable, "-c", f"""
import sys
sys.path.insert(0, '/home/adminuser/venv/lib/python3.13/site-packages')
from demucs.separate import main
main([
    '--model', 'mdx_extra',
    '--out', '{output_dir}',
    '--mp3',
    '--device', 'cpu',
    '{input_file}'
])
"""
            ]
            
            process = subprocess.run(cmd, capture_output=True, text=True, timeout=1200)
            
            if process.returncode == 0:
                # Buscar archivos
                for model_dir in output_dir.rglob("*"):
                    if model_dir.is_dir() and model_dir.name == input_file.stem:
                        files = {}
                        for mp3_file in model_dir.glob("*.mp3"):
                            with open(mp3_file, "rb") as f:
                                files[mp3_file.name] = f.read()
                        
                        if files:
                            return True, files
                
            return False, f"Error: {process.stderr}"
                
    except Exception as e:
        return False, f"Excepción: {e}"

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎵 Disband Simple</h1>
        <p>Versión que funciona sin requirements.txt</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mostrar info del sistema
    st.info(f"Python: {sys.version.split()[0]} | Streamlit: {st.__version__}")
    
    # Verificar estado
    is_ready, message = check_everything()
    
    if not is_ready:
        st.warning(message)
        
        if st.button("🔧 Instalar Dependencias Manualmente"):
            with st.spinner("Instalando..."):
                success, install_msg = install_if_missing()
            
            if success:
                st.success(install_msg)
                st.rerun()
            else:
                st.error(install_msg)
                
                # Mostrar información de debug
                st.markdown("### 🔍 Debug Info")
                st.code(f"""
Sistema: {os.name}
Python: {sys.version}
Executable: {sys.executable}
Path: {sys.path[0]}
                """)
        
        return
    
    # Si todo está bien
    st.success(message)
    
    # Interfaz principal
    uploaded_file = st.file_uploader(
        "📁 Sube tu archivo MP3",
        type=['mp3'],
        help="Solo MP3 por ahora para simplificar"
    )
    
    if uploaded_file:
        size_mb = len(uploaded_file.getbuffer()) / (1024 * 1024)
        st.info(f"📄 {uploaded_file.name} ({size_mb:.1f} MB)")
        
        if st.button("🚀 Separar (Modelo Rápido)", type="primary"):
            st.warning("⏳ Procesando... Esto toma 3-5 minutos")
            
            with st.spinner("Separando stems..."):
                success, result = separate_audio(uploaded_file)
            
            if success:
                st.success(f"✅ ¡{len(result)} stems generados!")
                
                # Downloads
                col1, col2 = st.columns(2)
                
                with col1:
                    for filename, data in result.items():
                        st.download_button(
                            f"⬇️ {filename}",
                            data=data,
                            file_name=filename,
                            mime="audio/mpeg"
                        )
                
                with col2:
                    # ZIP
                    zip_buffer = BytesIO()
                    with zipfile.ZipFile(zip_buffer, 'w') as zf:
                        for filename, data in result.items():
                            zf.writestr(filename, data)
                    
                    zip_buffer.seek(0)
                    st.download_button(
                        "📦 Descargar ZIP",
                        data=zip_buffer.getvalue(),
                        file_name=f"{Path(uploaded_file.name).stem}_stems.zip",
                        mime="application/zip"
                    )
            else:
                st.error(f"❌ {result}")
    
    # Footer
    st.markdown("---")
    st.markdown("🎵 **Disband Simple** - Sin requirements.txt, instalación manual")

if __name__ == "__main__":
    main()    
