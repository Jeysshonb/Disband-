# 🎵 Disband - Separador de Stems Profesional

**Creado por [@jeysshon](https://github.com/jeysshon)**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://disband.streamlit.app)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Demucs](https://img.shields.io/badge/AI-Demucs-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

Separa cualquier canción en stems individuales usando inteligencia artificial de última generación. Rápido, simple y completamente gratis.

## ✨ Características

- 🚀 **Súper rápido** - Interfaz optimizada sin complicaciones
- 🧠 **IA avanzada** - Powered by Demucs de Meta AI
- 🎵 **4 stems** - Batería, bajo, voces e instrumentos
- 💾 **Múltiples formatos** - MP3, WAV, FLAC, M4A
- 📱 **Responsive** - Funciona en cualquier dispositivo
- 🆓 **Completamente gratis** - Sin límites ni suscripciones
- 🔒 **Privacidad total** - Todo se procesa en la nube, nada se guarda

## 🎯 Cómo usar

1. **📁 Sube tu archivo** - Arrastra o selecciona tu música
2. **🚀 Click "Separar"** - El proceso comienza automáticamente  
3. **⏱️ Espera 5-15 min** - Ve el progreso en tiempo real
4. **💾 Descarga** - Stems individuales o ZIP completo

## 🎼 Qué obtienes

| Stem | Descripción | Uso ideal |
|------|-------------|-----------|
| 🥁 **Drums** | Batería aislada | Backing tracks, practice |
| 🎸 **Bass** | Bajo limpio | Análisis, covers |
| 🎤 **Vocals** | Voces sin música | Karaoke, remixes |
| 🎹 **Other** | Instrumentos/guitarras | Covers, análisis |

## 🚀 Pruébalo ahora

**[🌟 Ir a Disband](https://disband.streamlit.app)**

No requiere instalación, registro ni pagos. ¡Solo sube tu música y listo!

## 🛠️ Tecnología

- **Frontend:** Streamlit (Python)
- **IA:** Demucs v4 (Meta AI Research)
- **Audio:** PyTorch + torchaudio
- **Deploy:** Streamlit Cloud
- **Formato:** MP3 320kbps de salida

## 📊 Rendimiento

| Duración canción | Tiempo proceso | Calidad |
|------------------|----------------|---------|
| 3-4 minutos | 5-10 min | ⭐⭐⭐⭐ |
| 5-6 minutos | 10-15 min | ⭐⭐⭐⭐ |
| 7+ minutos | 15-25 min | ⭐⭐⭐⭐ |

## 🔧 Para desarrolladores

### Estructura del proyecto
```
disband/
├── app.py              # Aplicación principal
├── requirements.txt    # Dependencias Python
├── packages.txt       # Dependencias sistema (ffmpeg)
└── README.md          # Este archivo
```

### Instalación local
```bash
# Clonar repositorio
git clone https://github.com/jeysshon/disband.git
cd disband

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar localmente
streamlit run app.py
```

### Deploy en Streamlit Cloud
1. Fork este repositorio
2. Conecta tu GitHub a [Streamlit Cloud](https://streamlit.io/cloud)
3. Selecciona `app.py` como archivo principal
4. ¡Deploy automático!

## 🎸 Casos de uso

### Para músicos
- **Covers de guitarra** - Backing tracks perfectos
- **Análisis de técnicas** - Aislar instrumentos específicos
- **Practice** - Tocar sobre stems profesionales
- **Karaoke** - Tracks sin voces

### Para productores
- **Remixes** - Stems de alta calidad
- **Sampling** - Aislar elementos específicos
- **Mashups** - Combinar diferentes tracks
- **Análisis** - Estudiar arreglos profesionales

### Para educadores
- **Enseñanza** - Mostrar instrumentos aislados
- **Transcripción** - Facilitar análisis musical
- **Composición** - Referencias y ejemplos
- **Teoría musical** - Demostrar conceptos

## 📈 Comparación

| Característica | Disband | Moises.ai | Spleeter | LALAL.AI |
|----------------|---------|-----------|----------|----------|
| **Precio** | 🆓 Gratis | 💰 $4/mes | 🆓 Gratis | 💰 Freemium |
| **Calidad** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Velocidad** | ⚡ Rápido | ⚡ Rápido | ⚡⚡ Muy rápido | ⚡ Medio |
| **Facilidad** | ✅ Muy fácil | ✅ Fácil | ❌ Técnico | ✅ Fácil |
| **Límites** | ✅ Sin límites | ❌ 5 tracks/mes | ✅ Sin límites | ❌ 10 min/mes |
| **Privacidad** | ✅ Total | ⚠️ Cloud | ✅ Local | ⚠️ Cloud |

## 🤝 Contribuir

¿Tienes ideas para mejorar Disband? ¡Contribuciones bienvenidas!

### Reportar bugs
1. Ve a [Issues](https://github.com/jeysshon/disband/issues)
2. Describe el problema claramente
3. Incluye pasos para reproducir
4. Adjunta screenshots si es útil

### Sugerir características
1. Abre un [Issue](https://github.com/jeysshon/disband/issues) con etiqueta "enhancement"
2. Explica la funcionalidad deseada
3. Describe el caso de uso
4. ¡Discutamos la implementación!

### Pull Requests
1. Fork el repositorio
2. Crea una rama: `git checkout -b mi-feature`
3. Commit cambios: `git commit -m 'Añadir feature'`
4. Push: `git push origin mi-feature`
5. Abre un Pull Request

## 📜 Licencia

MIT License - Libre para uso personal y comercial.

## 🙏 Agradecimientos

- **[Demucs](https://github.com/facebookresearch/demucs)** - Meta AI Research por el modelo de IA
- **[Streamlit](https://streamlit.io)** - Framework web increíble
- **[PyTorch](https://pytorch.org)** - Motor de deep learning
- **Comunidad open source** - Por hacer esto posible

## 📞 Contacto

**Creado por [@jeysshon](https://github.com/jeysshon)**

- 🐙 **GitHub:** [@jeysshon](https://github.com/jeysshon)
- 🌐 **App:** [disband.streamlit.app](https://disband.streamlit.app)
- 📧 **Issues:** [GitHub Issues](https://github.com/jeysshon/disband/issues)

## ⭐ Apoya el proyecto

Si Disband te fue útil:
- ⭐ **Dale una estrella** a este repositorio
- 🍴 **Comparte** con tus amigos músicos
- 🐛 **Reporta bugs** para mejorar la app
- 💡 **Sugiere ideas** para nuevas características

---

<div align="center">

**🎵 Separa cualquier canción en stems perfectos**

[![Usar Disband](https://img.shields.io/badge/🚀_Usar_Disband-Gratis-success?style=for-the-badge)](https://disband.streamlit.app)

*Hecho con ❤️ por [@jeysshon](https://github.com/jeysshon)*

</div>
