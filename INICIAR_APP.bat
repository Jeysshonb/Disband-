@echo off
title DISBAND AI - Separador Profesional de Audio y Stems
chcp 65001 > nul
cd /d "%~dp0"

echo ========================================================
echo    🎵 DISBAND AI - Servidor Local con IA (Demucs v4)
echo ========================================================
echo.
echo [1/2] Abriendo la pagina web en tu navegador...
start "" http://127.0.0.1:8000

echo [2/2] Iniciando motor de procesamiento local...
echo.
echo  * Pega cualquier link de YouTube, TikTok, SoundCloud, etc.
echo  * O arrastra tus archivos de video/audio directamente.
echo  * Reproductor multipista y descargas integradas.
echo.
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
pause
