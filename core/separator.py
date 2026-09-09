import os
import sys
import subprocess
import zipfile
import re
import numpy as np
from scipy.io import wavfile
from typing import Callable, Optional
from core.hardware import find_ffmpeg, get_system_hardware_info

def create_karaoke_track(stems_dir: str) -> Optional[str]:
    """Combina batería, bajo y otros para crear la pista instrumental / karaoke."""
    drums_p = os.path.join(stems_dir, "drums.wav")
    bass_p = os.path.join(stems_dir, "bass.wav")
    other_p = os.path.join(stems_dir, "other.wav")
    karaoke_p = os.path.join(stems_dir, "karaoke.wav")

    parts = []
    sr = None

    for p in [drums_p, bass_p, other_p]:
        if os.path.exists(p):
            rate, data = wavfile.read(p)
            sr = rate
            parts.append(data.astype(np.float32))

    if parts and sr is not None:
        # Sumar las pistas instrumentales
        combined = sum(parts)
        # Evitar clipping / saturación digital
        max_val = np.max(np.abs(combined))
        if max_val > 32767.0:
            combined = (combined / max_val) * 32700.0
        
        wavfile.write(karaoke_p, sr, combined.astype(np.int16))
        return karaoke_p
    
    return None

def build_stems_zip(stems_dir: str, title: str, output_zip_path: str) -> str:
    """Empaqueta todos los stems generados en un archivo ZIP con metadatos."""
    stem_files = {
        "vocals.wav": "01_Vocales_Aisladas.wav",
        "karaoke.wav": "02_Karaoke_Instrumental.wav",
        "drums.wav": "03_Bateria.wav",
        "bass.wav": "04_Bajo.wav",
        "other.wav": "05_Otros_Instrumentos.wav"
    }

    info_content = f"""==================================================
🎵 DISBAND AI - PISTAS SEPARADAS PROFESIONALES
==================================================
Canción / Video: {title}
Motor de IA: Demucs v4 (Meta AI Research)
Calidad: Audio Estudio PCM Lossless (16-bit 44.1kHz)

PISTAS INCLUIDAS:
- 01_Vocales_Aisladas.wav   : Voz principal y coros aislados
- 02_Karaoke_Instrumental.wav: Pista completa sin voz (lista para cantar/tocar)
- 03_Bateria.wav            : Solo percusión y ritmo
- 04_Bajo.wav               : Línea de bajo aislada
- 05_Otros_Instrumentos.wav : Guitarras, teclados, sintetizadores y arreglos

Generado localmente y 100% privado con Disband AI.
==================================================
"""

    with zipfile.ZipFile(output_zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("INFORMACION_PISTAS.txt", info_content)
        for orig_name, clean_name in stem_files.items():
            fpath = os.path.join(stems_dir, orig_name)
            if os.path.exists(fpath):
                zf.write(fpath, arcname=clean_name)

    return output_zip_path

def separate_stems(
    input_audio_path: str,
    output_dir: str,
    progress_callback: Optional[Callable[[float, str], None]] = None
) -> dict:
    """
    Ejecuta el modelo Demucs v4 real sobre el archivo de audio.
    Retorna un diccionario con las rutas de los stems generados.
    """
    os.makedirs(output_dir, exist_ok=True)
    hw = get_system_hardware_info()
    device = hw["device"] # 'cuda' o 'cpu'

    # Agregar scripts de Python al PATH para encontrar demucs
    scripts_dir = os.path.join(
        os.environ.get("LOCALAPPDATA", ""),
        r"Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\Scripts"
    )
    if os.path.exists(scripts_dir) and scripts_dir not in os.environ["PATH"]:
        os.environ["PATH"] = scripts_dir + os.pathsep + os.environ["PATH"]

    ffmpeg_bin = find_ffmpeg()
    if ffmpeg_bin:
        ffmpeg_dir = os.path.dirname(ffmpeg_bin)
        if ffmpeg_dir not in os.environ["PATH"]:
            os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ["PATH"]

    if progress_callback:
        progress_callback(10.0, f"Iniciando Demucs v4 en {hw['acceleration']}...")

    cmd = [
        sys.executable,
        "-m", "demucs.separate",
        "-n", "htdemucs",
        "-d", device,
        "-o", output_dir,
        input_audio_path
    ]

    if progress_callback:
        progress_callback(20.0, "Cargando pesos de la red neuronal Demucs v4...")

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    percent_pattern = re.compile(r'(\d+)%')
    current_progress = 25.0

    while True:
        line = process.stdout.readline()
        if not line and process.poll() is not None:
            break
        if line:
            line_str = line.strip()
            # Buscar avance en porcentaje del progreso de separación
            match = percent_pattern.search(line_str)
            if match:
                val = int(match.group(1))
                # Escalar de 25% a 85%
                scaled = 25.0 + (val * 0.60)
                current_progress = max(current_progress, scaled)
                if progress_callback:
                    progress_callback(current_progress, f"Separando frecuencias con IA: {val}%")
            elif "Selected model" in line_str:
                if progress_callback:
                    progress_callback(25.0, "Modelo HTDemucs cargado en memoria...")
            elif "Separating track" in line_str:
                if progress_callback:
                    progress_callback(30.0, "Procesando ondas de audio por capas...")

    ret_code = process.wait()
    if ret_code != 0:
        raise RuntimeError(f"Error al ejecutar Demucs (código {ret_code}).")

    if progress_callback:
        progress_callback(88.0, "Generando pista instrumental Karaoke...")

    # Los stems quedan en output_dir/htdemucs/<nombre_cancion>/
    input_basename = os.path.splitext(os.path.basename(input_audio_path))[0]
    expected_stems_dir = os.path.join(output_dir, "htdemucs", input_basename)
    
    # En caso de que demucs haya cambiado espacios o caracteres en la carpeta
    if not os.path.exists(expected_stems_dir):
        htdemucs_dir = os.path.join(output_dir, "htdemucs")
        if os.path.exists(htdemucs_dir):
            subdirs = [os.path.join(htdemucs_dir, d) for d in os.listdir(htdemucs_dir) if os.path.isdir(os.path.join(htdemucs_dir, d))]
            if subdirs:
                expected_stems_dir = subdirs[0]

    if not os.path.exists(expected_stems_dir):
        raise FileNotFoundError(f"No se encontró la carpeta de resultados en {expected_stems_dir}")

    # Crear la pista de Karaoke combinando batería, bajo y otros
    create_karaoke_track(expected_stems_dir)

    if progress_callback:
        progress_callback(95.0, "Empaquetando pistas en archivo ZIP...")

    zip_path = os.path.join(output_dir, f"{input_basename}_stems.zip")
    build_stems_zip(expected_stems_dir, input_basename, zip_path)

    if progress_callback:
        progress_callback(100.0, "¡Separación profesional completada!")

    return {
        "stems_dir": expected_stems_dir,
        "zip_path": zip_path,
        "files": {
            "vocals": os.path.join(expected_stems_dir, "vocals.wav"),
            "drums": os.path.join(expected_stems_dir, "drums.wav"),
            "bass": os.path.join(expected_stems_dir, "bass.wav"),
            "other": os.path.join(expected_stems_dir, "other.wav"),
            "karaoke": os.path.join(expected_stems_dir, "karaoke.wav"),
        }
    }
