# 🎵 Disband - Beautiful AI Stem Separator

**Created by [@jeysshon](https://github.com/jeysshon)**

Beautiful, fast, and professional stem separation powered by state-of-the-art AI. Transform any song into high-quality stems with just a few clicks.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://disband.streamlit.app)

![Disband Preview](https://via.placeholder.com/800x400/667eea/ffffff?text=Disband+AI+Stem+Separator)

## ✨ Features

- 🎨 **Beautiful Interface** - Modern, responsive design that's a joy to use
- 🧠 **State-of-the-Art AI** - Powered by Demucs v4 Hybrid Transformer
- ⚡ **Multiple Models** - Choose from 5 different AI models for various needs
- 🎵 **High Quality** - Professional-grade stem separation
- 💾 **Multiple Formats** - Export as MP3, WAV, or FLAC
- 📱 **Responsive** - Works perfectly on desktop, tablet, and mobile
- 🔒 **Privacy First** - All processing happens in the cloud, no data stored
- 🆓 **Completely Free** - No limits, no subscriptions

## 🚀 Try It Now

**[🌟 Launch Disband](https://disband.streamlit.app)**

No installation required! Just click the link above and start separating stems immediately.

## 🎵 What Can You Do?

### 🎸 For Musicians
- **Learn techniques** from your favorite artists
- **Create backing tracks** for practice and covers
- **Isolate instruments** for detailed study
- **Remove vocals** for karaoke tracks

### 🎛️ For Producers
- **Extract stems** for remixing
- **Analyze arrangements** and production techniques
- **Create sample libraries** from existing tracks
- **Reference mixing** decisions

### 🎓 For Educators
- **Demonstrate arrangement** concepts
- **Isolate parts** for student practice
- **Analyze composition** techniques
- **Create teaching materials**

## 🤖 Available AI Models

| Model | Quality | Speed | Best For |
|-------|---------|-------|----------|
| 🏆 **htdemucs_ft** | ⭐⭐⭐⭐⭐ | Slow | Professional results |
| 🎯 **htdemucs** | ⭐⭐⭐⭐ | Medium | Balanced quality/speed |
| 🎼 **htdemucs_6s** | ⭐⭐⭐⭐ | Medium | 6 stems (piano + guitar) |
| ⚡ **hdemucs_mmi** | ⭐⭐⭐ | Fast | Quick processing |
| 🚀 **mdx_extra** | ⭐⭐⭐ | Very Fast | Rapid testing |

## 📱 How to Use

1. **🌐 Visit** [disband.streamlit.app](https://disband.streamlit.app)
2. **📁 Upload** your audio file (MP3, WAV, FLAC, M4A, AAC)
3. **🤖 Choose** your AI model based on quality vs speed preference
4. **💾 Select** output format (MP3 for smaller files, WAV for best quality)
5. **🎯 Click** "Separate Stems" and let the AI work its magic
6. **⬇️ Download** individual stems or everything as a ZIP

## 🛠️ Local Development

Want to run Disband locally or contribute? Here's how:

### Prerequisites
- Python 3.8 or higher
- Git

### Setup
```bash
# Clone the repository
git clone https://github.com/jeysshon/disband.git
cd disband

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 🏗️ Tech Stack

- **Frontend:** Streamlit with custom CSS
- **AI Model:** Demucs v4 (Meta AI Research)
- **Audio Processing:** PyTorch, torchaudio, librosa
- **Deployment:** Streamlit Cloud
- **Language:** Python 3.8+

## 📋 Supported Formats

### Input Formats
- 🎵 **MP3** - Most common format
- 🎵 **WAV** - Uncompressed audio
- 🎵 **FLAC** - Lossless compression
- 🎵 **M4A** - Apple format
- 🎵 **AAC** - Advanced Audio Coding

### Output Formats
- 🎵 **MP3 320kbps** - Good quality, smaller files
- 🎵 **WAV 32-bit float** - Maximum quality, larger files
- 🎵 **FLAC** - Lossless compression

## 🎯 Use Cases & Examples

### 🎸 Guitar Cover Artists
```
Input: "Master of Puppets.mp3"
Model: htdemucs_ft (best quality)
Output: drums.wav + bass.wav + other.wav + vocals.wav
Result: Perfect backing track for guitar covers
```

### 🎤 Vocal Removal
```
Input: Any song
Model: htdemucs (balanced)
Output: vocals.wav + instrumental stems
Result: Instant karaoke track
```

### 🎛️ Remix Producers
```
Input: Popular track
Model: htdemucs_6s (6 stems)
Output: drums + bass + vocals + other + piano + guitar
Result: Full stem pack for remixing
```

## 🌟 Why Disband?

### vs Other Tools

| Feature | Disband | Competitor A | Competitor B |
|---------|---------|-------------|-------------|
| **Interface** | 🎨 Beautiful & Modern | 😐 Basic | 😐 Outdated |
| **Quality** | 🏆 State-of-the-art | 🥈 Good | 🥉 Basic |
| **Price** | 🆓 Free | 💰 $10/month | 💰 $5/month |
| **Privacy** | 🔒 Secure | ⚠️ Data collection | ⚠️ Unknown |
| **Speed** | ⚡ Multiple options | 🐌 Fixed | 🐌 Slow |
| **Formats** | 📁 Multiple | 📁 Limited | 📁 MP3 only |

### Key Advantages
- ✅ **No Registration** - Start using immediately
- ✅ **No Limits** - Process unlimited files
- ✅ **Best AI Models** - Latest Demucs v4 technology
- ✅ **Beautiful Design** - Actually enjoyable to use
- ✅ **Mobile Friendly** - Works on any device
- ✅ **Open Source** - Transparent and trustworthy

## 🚀 Deploy Your Own

Want to deploy your own instance? Easy!

### Streamlit Cloud (Recommended)
1. Fork this repository
2. Connect your GitHub to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy from your fork
4. Share your custom instance!

### Docker
```bash
# Build the image
docker build -t disband .

# Run the container
docker run -p 8501:8501 disband
```

### Manual Deployment
Follow the Streamlit deployment guides for your preferred platform:
- [Streamlit Cloud](https://docs.streamlit.io/streamlit-community-cloud)
- [Heroku](https://docs.streamlit.io/knowledge-base/tutorials/deploy/heroku)
- [AWS](https://docs.streamlit.io/knowledge-base/tutorials/deploy/aws)

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### 🐛 Bug Reports
Found a bug? [Open an issue](https://github.com/jeysshon/disband/issues) with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable

### 💡 Feature Requests
Have an idea? [Open an issue](https://github.com/jeysshon/disband/issues) with:
- Clear description of the feature
- Use case and benefits
- Mockups or examples if applicable

### 🔧 Pull Requests
Ready to code? 
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[Demucs](https://github.com/facebookresearch/demucs)** - Amazing AI model by Meta AI Research
- **[Streamlit](https://streamlit.io)** - Beautiful web framework for ML apps
- **[PyTorch](https://pytorch.org)** - Deep learning framework
- **Open Source Community** - For making projects like this possible

## 📞 Contact

**Created by [@jeysshon](https://github.com/jeysshon)**

- 🐙 **GitHub:** [@jeysshon](https://github.com/jeysshon)
- 🌐 **Website:** [Coming Soon]
- 📧 **Email:** [Contact via GitHub]

## ⭐ Show Your Support

If you found Disband useful, please consider:
- ⭐ **Starring** this repository
- 🍴 **Forking** to create your own version
- 📢 **Sharing** with your friends and colleagues
- 🐛 **Contributing** bug reports and features

---

<div align="center">

**🎵 Transform Any Song Into Perfect Stems**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://disband.streamlit.app)

*Made with ❤️ by [@jeysshon](https://github.com/jeysshon)*

</div>