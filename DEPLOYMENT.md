# 🚀 Deployment Guide for Disband

## 📁 Repository Structure

Make sure your GitHub repository has this exact structure:

```
disband/
├── app.py                    # Main Streamlit app
├── requirements.txt          # Python dependencies
├── packages.txt             # System packages (ffmpeg)
├── README.md                # Project documentation
├── DEPLOYMENT.md            # This file
├── .streamlit/
│   └── config.toml          # Streamlit configuration
└── .gitignore               # Git ignore file
```

## 🌐 Deploy to Streamlit Cloud (Recommended)

### Step 1: Prepare Your Repository
1. Create a new GitHub repository named `disband`
2. Upload all the files with the exact structure shown above
3. Make sure the main app file is named `app.py`

### Step 2: Connect to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository: `yourusername/disband`
5. Main file path: `app.py`
6. App URL: `disband` (or custom name)

### Step 3: Deploy
1. Click "Deploy!"
2. Wait 5-10 minutes for initial deployment
3. Your app will be available at: `https://disband.streamlit.app`

## ⚙️ Configuration Files Explained

### requirements.txt
```txt
streamlit>=1.28.0      # Web framework
torch>=2.0.0           # PyTorch for AI
torchaudio>=2.0.0      # Audio processing
demucs>=4.0.0          # AI model
numpy>=1.21.0          # Numerical computing
scipy>=1.7.0           # Scientific computing
librosa>=0.9.0         # Audio analysis
soundfile>=0.12.0      # Audio file I/O
pathlib2>=2.3.0        # Path utilities
```

### packages.txt
```txt
ffmpeg                 # Audio processing system dependency
```

### .streamlit/config.toml
```toml
[browser]
gatherUsageStats = false    # Privacy

[server]
maxUploadSize = 200         # 200MB max file size
maxMessageSize = 200        # 200MB max message size

[theme]
primaryColor = "#667eea"    # Brand colors
backgroundColor = "#f8faff"
secondaryBackgroundColor = "#f0f4ff"
textColor = "#262730"
```

## 🔧 Troubleshooting Deployment

### Common Issues

#### 1. "Module not found" errors
**Solution:** Check that all dependencies are in `requirements.txt` with correct versions

#### 2. "FFmpeg not found" errors
**Solution:** Make sure `packages.txt` contains `ffmpeg`

#### 3. Large file upload failures
**Solution:** File size is limited to 200MB. Users should compress audio or use shorter clips.

#### 4. Memory errors during processing
**Solution:** This is expected for very large files. The app will automatically handle this.

### Logs and Debugging
- View logs in Streamlit Cloud dashboard
- Check the "Logs" tab for detailed error messages
- Most issues are dependency-related

## 🚀 Alternative Deployment Options

### Docker Deployment

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app files
COPY . .

# Expose port
EXPOSE 8501

# Run the app
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

Build and run:
```bash
docker build -t disband .
docker run -p 8501:8501 disband
```

### Heroku Deployment

1. Create `Procfile`:
```
web: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

2. Create `Aptfile`:
```
ffmpeg
```

3. Deploy:
```bash
heroku create your-app-name
git push heroku main
```

### Railway Deployment

1. Connect your GitHub repository to Railway
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `streamlit run app.py --server.address 0.0.0.0`

## 🔒 Environment Variables

For production deployments, you might want to set:

```bash
# Optional: Analytics and tracking
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Optional: Custom themes
STREAMLIT_THEME_PRIMARY_COLOR="#667eea"
STREAMLIT_THEME_BACKGROUND_COLOR="#f8faff"
```

## 📊 Performance Optimization

### For Large Scale Usage

1. **CDN Integration:** Serve static assets via CDN
2. **Load Balancing:** Use multiple instances for high traffic
3. **Caching:** Implement model caching for faster loading
4. **GPU Support:** Use GPU-enabled instances for faster processing

### Memory Management

The app is designed to handle:
- Files up to 200MB
- Automatic cleanup of temporary files
- Memory-efficient processing

## 🛡️ Security Considerations

### Production Deployment
- Enable HTTPS (handled by Streamlit Cloud)
- Set appropriate file size limits
- Monitor usage and implement rate limiting if needed
- Regular dependency updates

### Privacy
- No user data is stored
- Processing happens in memory only
- Temporary files are automatically cleaned
- No analytics by default

## 📈 Monitoring and Analytics

### Built-in Metrics
- Streamlit Cloud provides basic analytics
- View app usage in the dashboard
- Monitor errors and performance

### Custom Analytics (Optional)
Add to your app if needed:
```python
# Add to app.py for custom tracking
import streamlit as st

# Track usage (optional)
def track_usage(action):
    # Your analytics code here
    pass
```

## 🔄 Updates and Maintenance

### Updating the App
1. Push changes to your GitHub repository
2. Streamlit Cloud will automatically redeploy
3. Check the logs for any deployment issues

### Dependency Updates
Regularly update `requirements.txt`:
```bash
pip list --outdated
# Update versions in requirements.txt
```

### Model Updates
When new Demucs models are released:
1. Update the model list in `app.py`
2. Test with the new models
3. Update documentation

## 🎯 Custom Domain (Optional)

To use a custom domain with Streamlit Cloud:
1. Go to your app settings
2. Add your custom domain
3. Configure DNS settings with your provider
4. Enable HTTPS (automatic)

Example: `https://yourapp.yourdomian.com`

## 📞 Support

If you encounter deployment issues:
1. Check the [Streamlit Community Forum](https://discuss.streamlit.io)
2. Review [Streamlit Cloud documentation](https://docs.streamlit.io/streamlit-community-cloud)
3. Open an issue in your GitHub repository

## ✅ Deployment Checklist

Before deploying, ensure:
- [ ] All files are in the correct repository structure
- [ ] `app.py` is the main file name
- [ ] `requirements.txt` has all dependencies
- [ ] `packages.txt` includes `ffmpeg`
- [ ] `.streamlit/config.toml` is configured
- [ ] Repository is public (for free Streamlit Cloud)
- [ ] You have a Streamlit Cloud account linked to GitHub

## 🎉 Post-Deployment

After successful deployment:
1. Test all features thoroughly
2. Update your README with the live app URL
3. Share your creation with the community!
4. Monitor usage and gather feedback

Your Disband app should now be live and accessible to users worldwide! 🌍