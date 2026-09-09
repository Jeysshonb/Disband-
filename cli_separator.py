#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Disband AI - Separador Rápido por Consola
Permite pegar un enlace o arrastrar un archivo para procesarlo de inmediato.
"""
import os
import sys
import subprocess
import shutil

# Configurar salida UTF-8 en consola de Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Asegurar que Scripts de Python y FFmpeg estén en el PATH
scripts_dir = os.path.join(
    os.environ.get("LOCALAPPDATA", ""),
    r"Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\Scripts"
)
if os.path.exists(scripts_dir) and scripts_dir not in os.environ["PATH"]:
    os.environ["PATH"] = scripts_dir + os.pathsep + os.environ["PATH"]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FFMPEG_BIN = os.path.join(BASE_DIR, "bin", "ffmpeg")
if os.path.exists(FFMPEG_BIN) and FFMPEG_BIN not in os.environ["PATH"]:
    os.environ["PATH"] = FFMPEG_BIN + os.pathsep + os.environ["PATH"]

from core.hardware import get_system_hardware_info
from core.downloader import get_media_info, download_best_audio, sanitize_filename
from core.separator import separate_stems

def main():
    print("=" * 60)
    print("   DISBAND AI - SEPARADOR ULTRA RAPIDO DE PISTAS")
    print("=" * 60)

    # 1. Hardware
    hw = get_system_hardware_info()
    print(f"\n[*] CPU Detectado: {hw['cpu_name']}")
    print(f"[*] Hilos / Núcleos: {hw['threads']} hilos lógicos ({hw['cores']} núcleos físicos)")
    print(f"[*] Memoria RAM: {hw['ram_gb']} GB")
    print(f"[*] GPU: {hw['gpu_name']}")
    print(f"[*] Modo de Aceleración: {hw['acceleration']}")
    print(f"[*] FFmpeg: {'Listo en ' + hw['ffmpeg_path'] if hw['ffmpeg_installed'] else 'No detectado'}")
    print("=" * 60)

    # 2. Solicitar Link o Archivo
    target = ""
    if len(sys.argv) > 1:
        target = " ".join(sys.argv[1:]).strip('"')
    else:
        print("\nPuedes:")
        print("  1. Pegar un link de YouTube, TikTok, SoundCloud, Instagram...")
        print("  2. O arrastrar directamente un archivo de video/audio a esta ventana\n")
        try:
            target = input(">> Ingresa el enlace o arrastra tu archivo: ").strip().strip('"')
        except (KeyboardInterrupt, EOFError):
            print("\nOperación cancelada.")
            return

    if not target:
        print("[!] No ingresaste ningún enlace o archivo.")
        return

    out_base = os.path.join(BASE_DIR, "salida_stems")
    os.makedirs(out_base, exist_ok=True)

    def print_progress(percent, msg):
        bar_len = 30
        filled = int(bar_len * (percent / 100.0))
        bar = "█" * filled + "-" * (bar_len - filled)
        sys.stdout.write(f"\r[{bar}] {percent:5.1f}% | {msg[:45]:<45}")
        sys.stdout.flush()

    audio_file = ""
    song_title = "Pista"

    try:
        # Caso A: Es un enlace web
        if target.startswith("http://") or target.startswith("https://"):
            print(f"\n[1/3] Obteniendo información del video...")
            try:
                info = get_media_info(target)
                song_title = sanitize_filename(info.get("title", "audio_web"))
                print(f"      Título: {info.get('title')}")
                print(f"      Canal:  {info.get('uploader')}")
            except Exception:
                song_title = "audio_descargado"

            temp_dl = os.path.join(out_base, "_temp_download")
            if os.path.exists(temp_dl):
                shutil.rmtree(temp_dl, ignore_errors=True)
            os.makedirs(temp_dl, exist_ok=True)

            print(f"\n[2/3] Descargando la mejor calidad de audio stream...")
            audio_file = download_best_audio(target, temp_dl, print_progress)
            print("\n      [OK] Audio descargado y convertido a PCM HQ.")

        # Caso B: Es un archivo local
        else:
            if not os.path.exists(target):
                print(f"\n[ERROR] El archivo '{target}' no existe.")
                return
            audio_file = target
            song_title = sanitize_filename(os.path.splitext(os.path.basename(target))[0])
            print(f"\n[1/3] Archivo local detectado: {song_title}")

        # 3. Separación con Demucs v4
        folder_name = song_title if song_title else "audio_procesado"
        final_song_dir = os.path.join(out_base, folder_name)
        os.makedirs(final_song_dir, exist_ok=True)

        print(f"\n[3/3] Separando pistas con IA Demucs v4 ({hw['acceleration']})...")
        print("      (Voz, Batería, Bajo, Otros Instrumentos y Karaoke)")

        result = separate_stems(audio_file, final_song_dir, print_progress)
        print("\n\n" + "=" * 60)
        print("  ¡SEPARACIÓN COMPLETADA CON ÉXITO!")
        print("=" * 60)
        print(f"\nPistas generadas en:\n{result['stems_dir']}")
        print(f"\nArchivo ZIP listo en:\n{result['zip_path']}")

        # Abrir la carpeta en el explorador de Windows
        try:
            if sys.platform == "win32":
                os.startfile(result["stems_dir"])
        except Exception:
            pass

    except Exception as e:
        print(f"\n\n[ERROR]: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
    print("\nPresiona ENTER para salir...")
    try:
        input()
    except Exception:
        pass
