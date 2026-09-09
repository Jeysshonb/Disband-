import os
import re
from typing import Callable, Optional
from core.hardware import find_ffmpeg

def sanitize_filename(name: str) -> str:
    """Limpia caracteres especiales para nombres de archivo válidos en Windows."""
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()

def get_media_info(url: str) -> dict:
    """Extrae título, duración, autor y miniatura sin descargar el video."""
    import yt_dlp

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
        'extract_flat': False
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            "title": info.get("title", "Audio Desconocido"),
            "uploader": info.get("uploader") or info.get("channel") or "Desconocido",
            "duration": info.get("duration", 0),
            "thumbnail": info.get("thumbnail") or "",
            "id": info.get("id", "media"),
            "url": url
        }

def download_best_audio(
    url: str,
    output_dir: str,
    progress_callback: Optional[Callable[[float, str], None]] = None
) -> str:
    """
    Descarga la mejor calidad de audio disponible de cualquier URL compatible
    (YouTube, TikTok, Instagram, SoundCloud, etc.) y lo convierte a WAV HQ.
    """
    import yt_dlp

    os.makedirs(output_dir, exist_ok=True)
    ffmpeg_location = find_ffmpeg()

    def _hook(d):
        if progress_callback and d.get('status') == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate') or 1
            downloaded = d.get('downloaded_bytes', 0)
            percent = min(100.0, max(0.0, (downloaded / total) * 100.0))
            speed = d.get('_speed_str', '')
            eta = d.get('_eta_str', '')
            msg = f"Descargando audio stream... {percent:.1f}% ({speed} ETA: {eta})"
            progress_callback(percent, msg)
        elif progress_callback and d.get('status') == 'finished':
            progress_callback(100.0, "Audio descargado. Procesando formato con FFmpeg...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, 'source_audio.%(ext)s'),
        'progress_hooks': [_hook],
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '0', # máxima calidad PCM
        }],
    }

    if ffmpeg_location:
        ydl_opts['ffmpeg_location'] = os.path.dirname(ffmpeg_location)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    expected_wav = os.path.join(output_dir, 'source_audio.wav')
    if os.path.exists(expected_wav):
        return expected_wav

    # Fallback si se guardó con otra extensión
    for f in os.listdir(output_dir):
        if f.startswith('source_audio'):
            return os.path.join(output_dir, f)

    raise FileNotFoundError("No se encontró el archivo de audio descargado.")
