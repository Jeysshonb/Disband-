import os
import platform
import subprocess
import shutil
import torch

def find_ffmpeg() -> str | None:
    """Busca ffmpeg en el PATH del sistema o en la carpeta bin local."""
    # 1. En el PATH
    path_ffmpeg = shutil.which("ffmpeg")
    if path_ffmpeg:
        return path_ffmpeg
    
    # 2. En carpeta local bin/ffmpeg
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    local_bin = os.path.join(base_dir, "bin", "ffmpeg", "ffmpeg.exe")
    if os.path.exists(local_bin):
        return local_bin

    # 3. Rutas habituales de winget / scoop / chocolatey en Windows
    import glob
    possible_paths = [
        os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg*\ffmpeg*\bin\ffmpeg.exe"),
        r"C:\ffmpeg\bin\ffmpeg.exe",
        os.path.expandvars(r"%USERPROFILE%\scoop\shims\ffmpeg.exe"),
    ]
    for pattern in possible_paths:
        matches = glob.glob(pattern)
        if matches and os.path.exists(matches[0]):
            return matches[0]
            
    return None

def get_system_hardware_info() -> dict:
    """Detecta GPU, CPU, núcleos, RAM y aceleración disponible."""
    cpu_name = platform.processor() or "AMD/Intel x86_64"
    threads = os.cpu_count() or 4
    cores = threads // 2

    ram_gb = 16.0
    try:
        import psutil
        ram_gb = round(psutil.virtual_memory().total / (1024 ** 3), 1)
        cores = psutil.cpu_count(logical=False) or (threads // 2)
    except ImportError:
        pass

    gpu_name = "No detectada"
    acceleration = "CPU Multithread (Optimizado)"
    device_str = "cpu"

    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        acceleration = "NVIDIA CUDA (Aceleración Máxima)"
        device_str = "cuda"
    else:
        try:
            cmd = "powershell -Command \"Get-CimInstance Win32_VideoController | Select-Object -ExpandProperty Name\""
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=4)
            if res.returncode == 0 and res.stdout.strip():
                gpus = [g.strip() for g in res.stdout.strip().splitlines() if g.strip()]
                gpu_name = ", ".join(gpus)
                if "Radeon" in gpu_name or "AMD" in gpu_name:
                    acceleration = f"CPU {threads}-Hilos + GPU AMD ({gpu_name})"
                elif "Intel" in gpu_name:
                    acceleration = f"CPU {threads}-Hilos + GPU Intel ({gpu_name})"
        except Exception:
            pass

    ffmpeg_bin = find_ffmpeg()

    return {
        "device": device_str,
        "acceleration": acceleration,
        "gpu_name": gpu_name,
        "cpu_name": cpu_name,
        "threads": threads,
        "cores": cores,
        "ram_gb": ram_gb,
        "ffmpeg_installed": ffmpeg_bin is not None,
        "ffmpeg_path": ffmpeg_bin or "No encontrado"
    }
