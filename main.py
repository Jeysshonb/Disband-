import os
import sys
import uuid
import asyncio
import threading
from typing import Dict, Any, Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Asegurar que el directorio de scripts de Python esté en PATH
scripts_dir = os.path.join(
    os.environ.get("LOCALAPPDATA", ""),
    r"Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\Scripts"
)
if os.path.exists(scripts_dir) and scripts_dir not in os.environ["PATH"]:
    os.environ["PATH"] = scripts_dir + os.pathsep + os.environ["PATH"]

from core.hardware import get_system_hardware_info, find_ffmpeg
from core.downloader import get_media_info, download_best_audio, sanitize_filename
from core.separator import separate_stems

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_DIR = os.path.join(BASE_DIR, "storage")
STATIC_DIR = os.path.join(BASE_DIR, "static")

os.makedirs(STORAGE_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

app = FastAPI(
    title="Disband AI",
    description="Separador de stems con IA (Demucs v4) y extractor de audio HQ"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Estado de tareas en memoria
JOBS: Dict[str, Dict[str, Any]] = {}

class UrlRequest(BaseModel):
    url: str

@app.get("/api/system")
def api_system_info():
    """Retorna información del hardware local (GPU, CPU, núcleos, RAM y FFmpeg)."""
    return get_system_hardware_info()

@app.post("/api/extract-info")
def api_extract_info(req: UrlRequest):
    """Obtiene vista previa y metadatos de un enlace sin descargarlo."""
    try:
        info = get_media_info(req.url)
        return {"success": True, "data": info}
    except Exception as e:
        return {"success": False, "error": str(e)}

def _run_processing_pipeline(job_id: str, source_type: str, source_data: str, title: str):
    """Pipeline en hilo secundario: descarga -> extracción -> separación con IA -> ZIP."""
    job_dir = os.path.join(STORAGE_DIR, job_id)
    os.makedirs(job_dir, exist_ok=True)

    def _update_progress(percent: float, msg: str):
        if job_id in JOBS:
            JOBS[job_id]["progress"] = round(percent, 1)
            JOBS[job_id]["message"] = msg

    try:
        audio_path = None
        if source_type == "url":
            _update_progress(5.0, "Conectando al servidor y analizando stream...")
            audio_path = download_best_audio(
                source_data,
                output_dir=job_dir,
                progress_callback=_update_progress
            )
        else: # local upload
            audio_path = source_data
            _update_progress(10.0, "Archivo listo para procesar...")

        _update_progress(20.0, "Iniciando motor de separación Demucs v4...")
        result = separate_stems(
            input_audio_path=audio_path,
            output_dir=job_dir,
            progress_callback=_update_progress
        )

        JOBS[job_id]["status"] = "completed"
        JOBS[job_id]["progress"] = 100.0
        JOBS[job_id]["message"] = "¡Proceso terminado exitosamente!"
        JOBS[job_id]["title"] = title
        JOBS[job_id]["result"] = {
            "zip_filename": os.path.basename(result["zip_path"]),
            "stems": ["vocals", "karaoke", "drums", "bass", "other"]
        }

    except Exception as e:
        JOBS[job_id]["status"] = "error"
        JOBS[job_id]["message"] = f"Error: {str(e)}"

@app.post("/api/process/url")
def api_process_url(req: UrlRequest, background_tasks: BackgroundTasks):
    """Inicia la descarga y separación desde un link."""
    job_id = uuid.uuid4().hex
    try:
        info = get_media_info(req.url)
        title = info.get("title", "Audio")
    except Exception:
        title = "Audio Web"

    JOBS[job_id] = {
        "id": job_id,
        "status": "processing",
        "progress": 2.0,
        "message": "Iniciando tarea...",
        "title": title,
        "source": req.url,
        "result": None
    }

    threading.Thread(
        target=_run_processing_pipeline,
        args=(job_id, "url", req.url, title),
        daemon=True
    ).start()

    return {"success": True, "job_id": job_id, "title": title}

@app.post("/api/process/upload")
async def api_process_upload(file: UploadFile = File(...)):
    """Inicia la separación desde un archivo subido (video o audio)."""
    job_id = uuid.uuid4().hex
    job_dir = os.path.join(STORAGE_DIR, job_id)
    os.makedirs(job_dir, exist_ok=True)

    safe_name = sanitize_filename(file.filename or "uploaded_media")
    saved_path = os.path.join(job_dir, safe_name)

    with open(saved_path, "wb") as f:
        content = await file.read()
        f.write(content)

    title = os.path.splitext(safe_name)[0]

    JOBS[job_id] = {
        "id": job_id,
        "status": "processing",
        "progress": 5.0,
        "message": "Archivo recibido. Preparando separación...",
        "title": title,
        "source": "upload",
        "result": None
    }

    threading.Thread(
        target=_run_processing_pipeline,
        args=(job_id, "upload", saved_path, title),
        daemon=True
    ).start()

    return {"success": True, "job_id": job_id, "title": title}

@app.get("/api/jobs/{job_id}")
def api_get_job_status(job_id: str):
    """Consulta el estado y avance de una tarea."""
    if job_id not in JOBS:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return JOBS[job_id]

@app.get("/api/progress-stream/{job_id}")
async def api_progress_stream(job_id: str):
    """Transmite el progreso en tiempo real usando Server-Sent Events (SSE)."""
    if job_id not in JOBS:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    async def event_generator():
        while True:
            job = JOBS.get(job_id)
            if not job:
                break
            import json
            yield f"data: {json.dumps(job)}\n\n"
            if job["status"] in ("completed", "error"):
                break
            await asyncio.sleep(0.8)

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("/api/audio/{job_id}/{stem}")
def api_stream_audio(job_id: str, stem: str):
    """Sirve la pista individual solicitada para reproducir en el navegador."""
    job_dir = os.path.join(STORAGE_DIR, job_id)
    # Buscar en htdemucs o directamente
    stem_file = f"{stem}.wav"
    
    # 1. Buscar en subcarpetas de htdemucs
    htdemucs_dir = os.path.join(job_dir, "htdemucs")
    if os.path.exists(htdemucs_dir):
        for root, _, files in os.walk(htdemucs_dir):
            if stem_file in files:
                return FileResponse(
                    path=os.path.join(root, stem_file),
                    media_type="audio/wav",
                    filename=stem_file
                )

    raise HTTPException(status_code=404, detail=f"Pista '{stem}' no encontrada.")

@app.get("/api/download/zip/{job_id}")
def api_download_zip(job_id: str):
    """Descarga el paquete completo ZIP con todos los stems."""
    job_dir = os.path.join(STORAGE_DIR, job_id)
    if os.path.exists(job_dir):
        for f in os.listdir(job_dir):
            if f.endswith(".zip"):
                title = JOBS.get(job_id, {}).get("title", "stems")
                clean_title = sanitize_filename(title)
                return FileResponse(
                    path=os.path.join(job_dir, f),
                    media_type="application/zip",
                    filename=f"{clean_title}_stems.zip"
                )

    raise HTTPException(status_code=404, detail="Archivo ZIP no encontrado.")

@app.post("/api/open-folder/{job_id}")
def api_open_folder(job_id: str):
    """Abre la carpeta con las pistas directamente en el Explorador de Windows."""
    job_dir = os.path.join(STORAGE_DIR, job_id)
    htdemucs_dir = os.path.join(job_dir, "htdemucs")
    target_dir = htdemucs_dir if os.path.exists(htdemucs_dir) else job_dir

    # Buscar si hay una subcarpeta dentro de htdemucs
    if os.path.exists(htdemucs_dir):
        subdirs = [os.path.join(htdemucs_dir, d) for d in os.listdir(htdemucs_dir) if os.path.isdir(os.path.join(htdemucs_dir, d))]
        if subdirs:
            target_dir = subdirs[0]

    if os.path.exists(target_dir):
        try:
            if sys.platform == "win32":
                os.startfile(target_dir)
                return {"success": True}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
            
    raise HTTPException(status_code=404, detail="Carpeta de pistas no encontrada.")

# Servir frontend estático
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def serve_index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
