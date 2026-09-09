"""
Script para verificar y descargar automáticamente FFmpeg estático para Windows.
Garantiza que Disband AI funcione sin necesidad de configurar variables de entorno manualmente.
"""
import os
import sys
import shutil
import urllib.request
import zipfile

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FFMPEG_DIR = os.path.join(BASE_DIR, "bin", "ffmpeg")

def is_ffmpeg_available():
    if shutil.which("ffmpeg"):
        return True
    if os.path.exists(os.path.join(FFMPEG_DIR, "ffmpeg.exe")):
        return True
    return False

def download_and_extract_ffmpeg():
    os.makedirs(FFMPEG_DIR, exist_ok=True)
    target_exe = os.path.join(FFMPEG_DIR, "ffmpeg.exe")
    target_probe = os.path.join(FFMPEG_DIR, "ffprobe.exe")

    if os.path.exists(target_exe) and os.path.exists(target_probe):
        print("[OK] FFmpeg ya esta instalado en bin/ffmpeg/")
        return True

    print("[*] Descargando FFmpeg estatico para Windows (Gyan.dev essentials)...")
    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    zip_path = os.path.join(BASE_DIR, "bin", "ffmpeg.zip")

    try:
        def reporthook(block_num, block_size, total_size):
            downloaded = block_num * block_size
            if total_size > 0:
                percent = min(100.0, (downloaded / total_size) * 100.0)
                sys.stdout.write(f"\rDescargando: {percent:.1f}% ({downloaded // (1024*1024)}MB / {total_size // (1024*1024)}MB)")
                sys.stdout.flush()

        urllib.request.urlretrieve(url, zip_path, reporthook)
        print("\n📦 Extrayendo ffmpeg.exe y ffprobe.exe...")

        with zipfile.ZipFile(zip_path, 'r') as zf:
            for member in zf.namelist():
                if member.endswith("ffmpeg.exe"):
                    with zf.open(member) as source, open(target_exe, "wb") as target:
                        shutil.copyfileobj(source, target)
                elif member.endswith("ffprobe.exe"):
                    with zf.open(member) as source, open(target_probe, "wb") as target:
                        shutil.copyfileobj(source, target)

        if os.path.exists(zip_path):
            os.remove(zip_path)

        print("[OK] FFmpeg instalado correctamente en:", FFMPEG_DIR)
        return True
    except Exception as e:
        print(f"[ERROR] Error al descargar FFmpeg: {e}")
        return False

if __name__ == "__main__":
    if not is_ffmpeg_available():
        download_and_extract_ffmpeg()
    else:
        print("[OK] FFmpeg ya esta listo en el sistema.")
