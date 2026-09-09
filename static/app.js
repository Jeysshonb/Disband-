// Disband AI - Client Logic
document.addEventListener("DOMContentLoaded", () => {
  // Elementos DOM
  const hwBadge = document.getElementById("hwBadge");
  const hwText = document.getElementById("hwText");
  const ffmpegAlert = document.getElementById("ffmpegAlert");
  const tabs = document.querySelectorAll(".tab-btn");
  const tabContents = document.querySelectorAll(".tab-content");

  // Tab URL
  const urlInput = document.getElementById("urlInput");
  const btnPaste = document.getElementById("btnPaste");
  const btnProcessUrl = document.getElementById("btnProcessUrl");
  const urlPreviewCard = document.getElementById("urlPreviewCard");
  const previewThumb = document.getElementById("previewThumb");
  const previewTitle = document.getElementById("previewTitle");
  const previewAuthor = document.getElementById("previewAuthor");

  // Tab Archivo
  const dropzone = document.getElementById("dropzone");
  const fileInput = document.getElementById("fileInput");
  const selectedFileCard = document.getElementById("selectedFileCard");
  const selectedFileName = document.getElementById("selectedFileName");
  const selectedFileSize = document.getElementById("selectedFileSize");
  const btnProcessFile = document.getElementById("btnProcessFile");
  let currentSelectedFile = null;

  // Progreso
  const progressSection = document.getElementById("progressSection");
  const progressTitle = document.getElementById("progressTitle");
  const progressMessage = document.getElementById("progressMessage");
  const progressPercentage = document.getElementById("progressPercentage");
  const progressBarFill = document.getElementById("progressBarFill");
  const stepItems = [
    document.getElementById("step1"),
    document.getElementById("step2"),
    document.getElementById("step3"),
    document.getElementById("step4")
  ];

  // Resultados y Reproductor
  const resultsSection = document.getElementById("resultsSection");
  const resultSongTitle = document.getElementById("resultSongTitle");
  const btnDownloadZip = document.getElementById("btnDownloadZip");
  const btnMasterPlay = document.getElementById("btnMasterPlay");
  const masterPlayIcon = document.getElementById("masterPlayIcon");
  const currentTimeEl = document.getElementById("currentTime");
  const totalTimeEl = document.getElementById("totalTime");
  const masterTimeline = document.getElementById("masterTimeline");
  const btnResetMix = document.getElementById("btnResetMix");
  const btnNewConversion = document.getElementById("btnNewConversion");
  const stemRows = document.querySelectorAll(".stem-row");

  let currentJobId = null;
  let eventSource = null;
  let audioTracks = {}; // { 'vocals': Audio, 'drums': Audio, ... }
  let isPlaying = false;
  let isSoloActive = null;

  // 1. Cargar Estado de Hardware
  async function loadSystemHardware() {
    try {
      const res = await fetch("/api/system");
      const data = await res.json();

      let badgeMsg = `${data.acceleration} • ${data.ram_gb} GB RAM`;
      hwText.textContent = badgeMsg;

      if (!data.ffmpeg_installed) {
        ffmpegAlert.classList.remove("hidden");
      } else {
        ffmpegAlert.classList.add("hidden");
      }
    } catch (err) {
      hwText.textContent = "Hardware Local Activo";
    }
  }
  loadSystemHardware();

  // 2. Manejo de Pestañas
  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => t.classList.remove("active"));
      tabContents.forEach(c => c.classList.remove("active"));
      tab.classList.add("active");
      const targetId = tab.dataset.tab;
      document.getElementById(targetId).classList.add("active");
    });
  });

  // 3. Pegar desde portapapeles
  btnPaste.addEventListener("click", async () => {
    try {
      const text = await navigator.clipboard.readText();
      urlInput.value = text.trim();
      fetchUrlPreview(urlInput.value);
    } catch (e) {
      alert("No se pudo acceder al portapapeles automáticamente. Pega el enlace manualmente.");
    }
  });

  urlInput.addEventListener("change", () => {
    if (urlInput.value.trim().startsWith("http")) {
      fetchUrlPreview(urlInput.value.trim());
    }
  });

  urlInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      btnProcessUrl.click();
    }
  });

  async function fetchUrlPreview(url) {
    if (!url.startsWith("http")) return;
    try {
      const res = await fetch("/api/extract-info", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url })
      });
      const resData = await res.json();
      if (resData.success) {
        const d = resData.data;
        previewTitle.textContent = d.title;
        previewAuthor.textContent = d.uploader;
        if (d.thumbnail) {
          previewThumb.src = d.thumbnail;
          urlPreviewCard.classList.remove("hidden");
        }
      }
    } catch (err) {
      // Ignorar error silencioso de preview
    }
  }

  // 4. Drag & Drop y Subida de Archivos
  dropzone.addEventListener("click", () => fileInput.click());

  dropzone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropzone.classList.add("dragover");
  });

  dropzone.addEventListener("dragleave", () => {
    dropzone.classList.remove("dragover");
  });

  dropzone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropzone.classList.remove("dragover");
    if (e.dataTransfer.files.length > 0) {
      handleFileSelection(e.dataTransfer.files[0]);
    }
  });

  fileInput.addEventListener("change", () => {
    if (fileInput.files.length > 0) {
      handleFileSelection(fileInput.files[0]);
    }
  });

  function handleFileSelection(file) {
    currentSelectedFile = file;
    selectedFileName.textContent = file.name;
    const mb = (file.size / (1024 * 1024)).toFixed(2);
    selectedFileSize.textContent = `${mb} MB`;
    selectedFileCard.classList.remove("hidden");
  }

  // 5. Iniciar Procesamiento (URL)
  btnProcessUrl.addEventListener("click", async () => {
    const url = urlInput.value.trim();
    if (!url) {
      alert("Por favor introduce un enlace de video o canción válido.");
      return;
    }

    try {
      btnProcessUrl.disabled = true;
      btnProcessUrl.textContent = "Iniciando...";

      const res = await fetch("/api/process/url", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url })
      });

      const data = await res.json();
      if (data.success) {
        startProgressTracking(data.job_id, data.title);
      } else {
        alert("Error al iniciar tarea: " + (data.error || "Desconocido"));
      }
    } catch (err) {
      alert("Error al conectar con el servidor: " + err.message);
    } finally {
      btnProcessUrl.disabled = false;
      btnProcessUrl.innerHTML = `<span>Extraer & Separar</span><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>`;
    }
  });

  // 6. Iniciar Procesamiento (Archivo Local)
  btnProcessFile.addEventListener("click", async () => {
    if (!currentSelectedFile) return;

    try {
      btnProcessFile.disabled = true;
      btnProcessFile.textContent = "Subiendo...";

      const formData = new FormData();
      formData.append("file", currentSelectedFile);

      const res = await fetch("/api/process/upload", {
        method: "POST",
        body: formData
      });

      const data = await res.json();
      if (data.success) {
        startProgressTracking(data.job_id, data.title);
      } else {
        alert("Error al subir archivo");
      }
    } catch (err) {
      alert("Error de conexión: " + err.message);
    } finally {
      btnProcessFile.disabled = false;
      btnProcessFile.textContent = "Iniciar Separación IA";
    }
  });

  // 7. Seguimiento de Progreso en Vivo con SSE (Server-Sent Events)
  function startProgressTracking(jobId, title) {
    currentJobId = jobId;
    document.querySelector(".tabs").classList.add("hidden");
    tabContents.forEach(c => c.classList.add("hidden"));
    progressSection.classList.remove("hidden");
    resultsSection.classList.add("hidden");

    progressTitle.textContent = `Procesando: ${title}`;
    updateStepper(0);

    if (eventSource) {
      eventSource.close();
    }

    eventSource = new EventSource(`/api/progress-stream/${jobId}`);

    eventSource.onmessage = (event) => {
      try {
        const job = JSON.parse(event.data);
        const percent = Math.min(100, Math.max(0, job.progress || 0));

        progressBarFill.style.width = `${percent}%`;
        progressPercentage.textContent = `${Math.round(percent)}%`;
        progressMessage.textContent = job.message || "Procesando...";

        updateStepper(percent);

        if (job.status === "completed") {
          eventSource.close();
          setTimeout(() => showResults(job), 600);
        } else if (job.status === "error") {
          eventSource.close();
          alert("Ocurrió un error en el procesamiento: " + job.message);
          resetToNew();
        }
      } catch (err) {
        console.error("Error al parsear progreso SSE:", err);
      }
    };

    eventSource.onerror = () => {
      // Fallback a polling si SSE se interrumpe
      pollJobStatus(jobId);
    };
  }

  async function pollJobStatus(jobId) {
    const interval = setInterval(async () => {
      try {
        const res = await fetch(`/api/jobs/${jobId}`);
        const job = await res.json();
        const percent = job.progress || 0;

        progressBarFill.style.width = `${percent}%`;
        progressPercentage.textContent = `${Math.round(percent)}%`;
        progressMessage.textContent = job.message;
        updateStepper(percent);

        if (job.status === "completed") {
          clearInterval(interval);
          showResults(job);
        } else if (job.status === "error") {
          clearInterval(interval);
          alert("Error: " + job.message);
          resetToNew();
        }
      } catch (e) {
        clearInterval(interval);
      }
    }, 1500);
  }

  function updateStepper(percent) {
    stepItems.forEach(s => s.classList.remove("active"));
    if (percent >= 0) stepItems[0].classList.add("active");
    if (percent >= 20) stepItems[1].classList.add("active");
    if (percent >= 30) stepItems[2].classList.add("active");
    if (percent >= 85) stepItems[3].classList.add("active");
  }

  // 8. Mostrar Resultados y Configurar Reproductor Multipista
  function showResults(job) {
    progressSection.classList.add("hidden");
    resultsSection.classList.remove("hidden");

    resultSongTitle.textContent = job.title;
    btnDownloadZip.href = `/api/download/zip/${currentJobId}`;

    const btnOpenFolder = document.getElementById("btnOpenFolder");
    if (btnOpenFolder) {
      btnOpenFolder.onclick = async () => {
        try {
          await fetch(`/api/open-folder/${currentJobId}`, { method: "POST" });
        } catch (e) {
          console.error("Error abriendo carpeta:", e);
        }
      };
    }

    initMultiTrackPlayer(currentJobId);
  }

  function initMultiTrackPlayer(jobId) {
    // Detener pistas previas
    stopAllAudio();
    audioTracks = {};

    stemRows.forEach(row => {
      const stem = row.dataset.stem;
      const audioUrl = `/api/audio/${jobId}/${stem}`;
      const audio = new Audio(audioUrl);
      audio.preload = "auto";
      audioTracks[stem] = audio;

      // Botón de descarga directa WAV
      const downloadBtn = row.querySelector(".btn-stem-download");
      downloadBtn.href = audioUrl;
      downloadBtn.setAttribute("download", `${stem}.wav`);

      // Slider de volumen
      const volSlider = row.querySelector(".vol-slider");
      volSlider.value = 1;
      volSlider.oninput = () => {
        audio.volume = parseFloat(volSlider.value);
      };

      // Botón MUTE
      const btnMute = row.querySelector(".btn-mute");
      btnMute.classList.remove("active");
      btnMute.onclick = () => {
        audio.muted = !audio.muted;
        btnMute.classList.toggle("active", audio.muted);
      };

      // Botón SOLO
      const btnSolo = row.querySelector(".btn-solo");
      btnSolo.classList.remove("active");
      btnSolo.onclick = () => {
        if (isSoloActive === stem) {
          // Desactivar solo
          isSoloActive = null;
          stemRows.forEach(r => {
            const s = r.dataset.stem;
            r.querySelector(".btn-solo").classList.remove("active");
            audioTracks[s].muted = r.querySelector(".btn-mute").classList.contains("active");
          });
        } else {
          // Activar solo en esta pista
          isSoloActive = stem;
          stemRows.forEach(r => {
            const s = r.dataset.stem;
            const rSolo = r.querySelector(".btn-solo");
            if (s === stem) {
              rSolo.classList.add("active");
              audioTracks[s].muted = false;
            } else {
              rSolo.classList.remove("active");
              audioTracks[s].muted = true;
            }
          });
        }
      };
    });

    // Sincronizar duración y tiempo con la primera pista
    const primaryAudio = audioTracks["vocals"] || Object.values(audioTracks)[0];
    if (primaryAudio) {
      primaryAudio.addEventListener("loadedmetadata", () => {
        masterTimeline.max = primaryAudio.duration || 100;
        totalTimeEl.textContent = formatTime(primaryAudio.duration || 0);
      });

      primaryAudio.addEventListener("timeupdate", () => {
        if (!masterTimeline.matches(":active")) {
          masterTimeline.value = primaryAudio.currentTime;
        }
        currentTimeEl.textContent = formatTime(primaryAudio.currentTime);
      });

      primaryAudio.addEventListener("ended", () => {
        stopAllAudio();
      });
    }

    // Control Master de Línea de Tiempo (Scrubber)
    masterTimeline.addEventListener("input", () => {
      const seekTime = parseFloat(masterTimeline.value);
      for (const track of Object.values(audioTracks)) {
        track.currentTime = seekTime;
      }
      currentTimeEl.textContent = formatTime(seekTime);
    });

    // Control Master Play/Pause
    btnMasterPlay.onclick = toggleMasterPlay;

    // Reiniciar mezcla
    btnResetMix.onclick = () => {
      isSoloActive = null;
      stemRows.forEach(r => {
        const s = r.dataset.stem;
        r.querySelector(".btn-mute").classList.remove("active");
        r.querySelector(".btn-solo").classList.remove("active");
        const vol = r.querySelector(".vol-slider");
        vol.value = 1;
        if (audioTracks[s]) {
          audioTracks[s].muted = false;
          audioTracks[s].volume = 1;
        }
      });
    };
  }

  function toggleMasterPlay() {
    if (isPlaying) {
      for (const track of Object.values(audioTracks)) {
        track.pause();
      }
      masterPlayIcon.innerHTML = `<polygon points="5 3 19 12 5 21 5 3"></polygon>`;
      isPlaying = false;
    } else {
      for (const track of Object.values(audioTracks)) {
        track.play().catch(() => {});
      }
      masterPlayIcon.innerHTML = `<rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect>`;
      isPlaying = true;
    }
  }

  function stopAllAudio() {
    isPlaying = false;
    masterPlayIcon.innerHTML = `<polygon points="5 3 19 12 5 21 5 3"></polygon>`;
    for (const track of Object.values(audioTracks)) {
      track.pause();
      track.currentTime = 0;
    }
    masterTimeline.value = 0;
    currentTimeEl.textContent = "00:00";
  }

  function formatTime(seconds) {
    const min = Math.floor(seconds / 60);
    const sec = Math.floor(seconds % 60);
    return `${min.toString().padStart(2, "0")}:${sec.toString().padStart(2, "0")}`;
  }

  // 9. Reiniciar / Nueva Conversión
  btnNewConversion.addEventListener("click", resetToNew);

  function resetToNew() {
    stopAllAudio();
    if (eventSource) eventSource.close();
    currentJobId = null;
    currentSelectedFile = null;
    urlInput.value = "";
    urlPreviewCard.classList.add("hidden");
    selectedFileCard.classList.add("hidden");
    document.querySelector(".tabs").classList.remove("hidden");
    document.querySelector(".tab-content.active").classList.remove("hidden");
    progressSection.classList.add("hidden");
    resultsSection.classList.add("hidden");
  }
});
