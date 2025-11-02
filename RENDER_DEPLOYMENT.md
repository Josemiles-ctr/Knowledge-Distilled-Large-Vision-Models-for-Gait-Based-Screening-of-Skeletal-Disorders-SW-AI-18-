# Render Deployment Guide

## 🚀 Deploy GaitLab to Render in 5 Steps

Render is a modern cloud platform perfect for deploying FastAPI apps. This guide walks you through the entire process.

---

## Prerequisites

- ✅ GitHub account (code pushed to GitHub)
- ✅ Render account (free tier available: https://render.com)
- ✅ Docker image available (either locally tested or from Docker Hub)

---

## Step 1: Connect GitHub to Render

1. Go to https://dashboard.render.com
2. Sign up or log in
3. Click **"New +"** → **"Web Service"**
4. Select **"Deploy an existing repository"**
5. Authorize Render to access your GitHub account
6. Search for your repository: `Knowledge-Distilled-Large-Vision-Models-for-Gait-Based-Screening-of-Skeletal-Disorders-SW-AI-18-`
7. Select it and click **"Connect"**

---

## Step 2: Configure Web Service

### Basic Settings
- **Name**: `gaitlab-api` (or your preferred name)
- **Environment**: `Docker`
- **Region**: Choose closest to you (e.g., `us-east-1`)
- **Branch**: `main`

### Build Settings
- **Dockerfile path**: `Dockerfile` (default)
- **Docker context**: `.` (default)

### Deployment Settings
- **Auto-deploy**: ✅ Check this box (auto-deploy on push to main)

---

## Step 3: Set Environment Variables

Click **"Advanced"** and add these environment variables:

```
PORT=8000
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1
```

**Optional - if downloading model at runtime:**
```
MODEL_URL=https://your-presigned-url-to-model.pth
```
(If model is already in repo, this is optional)

---

## Step 4: Choose Pricing Tier

### Recommended for GaitLab:
- **Starter** ($7/month): 0.5 CPU, 512 MB RAM
  - Good for light testing
  - May timeout on first model load

- **Standard** ($12/month): 1 CPU, 2.5 GB RAM  
  - **Recommended** for production
  - Handles model loading well
  - Better performance

### First Deploy (Free Tier)
Render offers 750 free compute hours/month. You can:
- Deploy for free (if under 750 hours/month)
- Upgrade anytime if needed

---

## Step 5: Deploy!

1. Click **"Create Web Service"**
2. Render starts building (watch the logs in the dashboard)
3. Build takes ~8-15 minutes (first time)
4. Once deployed, you get a URL like: `https://gaitlab-api.onrender.com`

---

## 🔍 Monitor Build & Deployment

### Build Phase (5-10 min)
- You'll see Docker build logs
- Look for: "Model and embedder initialized successfully"
- Check for any errors

### Deployment Phase (1-2 min)
- Service spins up
- Uvicorn starts
- Ready to receive requests

### Health Checks
- Render automatically calls `/health` endpoint
- Must return `200 OK` for service to be considered "Live"
- Current setup: `{"status":"ok"}` ✅

---

## 🧪 Test Your Deployment

Once the service shows as "Live":

```bash
# Test health endpoint
curl https://gaitlab-api.onrender.com/health
# Expected: {"status":"ok"}

# Test ready endpoint
curl https://gaitlab-api.onrender.com/ready
# Expected: {"ready":true}

# Test conditions endpoint
curl https://gaitlab-api.onrender.com/conditions
# Expected: JSON with clinical conditions

# Test predict endpoint (requires video file)
curl -X POST https://gaitlab-api.onrender.com/predict \
  -F "video=@path/to/video.mp4" \
  -F "clinical_condition=Normal"
```

---

## ⚙️ Troubleshooting

### Service Won't Start
**Error**: "Service is restarting"
- Likely memory/timeout issue
- **Solution**: Upgrade to Standard tier (2.5 GB RAM)

### Build Timeout
**Error**: "Build exceeded time limit"
- Dependencies taking too long to install
- **Solution**: 
  - Build locally first: `docker build -t gaitlab .`
  - Or wait: Render will retry

### Health Check Failing
**Error**: "Service unhealthy"
- `/health` endpoint not returning 200
- **Check**:
  - App logs in Render dashboard
  - Ensure `main.py` has `/health` endpoint
  - Verify `MODEL_PATH` is correct

### Model File Not Found
**Error**: "Model file not found at /app/models/gait_predict_model_v_1.pth"
- Model weights not in Docker image
- **Solutions**:
  - Option A: Ensure model file is committed to git
  - Option B: Set `MODEL_URL` env var to download at startup
  - Option C: Ensure `.dockerignore` doesn't exclude models/

---

## 📊 Performance Tips

### Optimize for Render
1. **Use Standard tier** for production (~$12/month)
2. **Enable auto-scaling** if traffic expected to vary
3. **Use Redis cache** for repeated predictions (optional)
4. **Monitor logs** for errors and slow queries

### Model Loading
- First request after deploy: ~2-5 seconds (model loads)
- Subsequent requests: <1 second

### Scaling
- Render auto-scales horizontally (more instances)
- Current setup handles ~100 concurrent requests

---

## 🔐 Security

### Environment Variables
- Never put secrets in code
- Use Render's environment variable interface
- Sensitive data is encrypted at rest

### CORS Settings
Currently set to allow:
- `http://localhost:5173` (Svelte frontend)
- `http://localhost:3000` (React frontend)

**For production**, update `app/config.py`:
```python
CORS_ORIGINS = ["https://yourdomain.com"]
```

---

## 💾 Persistent Storage

Render provides:
- **Temporary disk** (/tmp, /app): Cleared on restart
- **Persistent disk** (optional): $4/month, survives restarts

Current setup doesn't need persistent storage (model is in image).

---

## 📝 Deployment Checklist

Before deploying:
- [ ] Code pushed to GitHub `main` branch
- [ ] `Dockerfile` exists and builds locally
- [ ] `main.py` has `/health` endpoint
- [ ] Model file included in image
- [ ] Environment variables documented
- [ ] No secrets in code
- [ ] `.gitignore` properly configured

---

## 🎯 What Happens on Deploy

1. **GitHub Webhook** → Render notified of push to main
2. **Docker Build** → Dockerfile executed in Render's builder
3. **Install Dependencies** → pip install -r requirements.txt
4. **Copy Code** → All source files copied to /app
5. **Model Download** → scripts/download_model.sh runs (if MODEL_URL set)
6. **Start Service** → uvicorn main:app --host 0.0.0.0 --port 8000
7. **Health Check** → Render polls /health endpoint
8. **Live** → Service is ready to receive traffic!

---

## 📚 Additional Resources

- **Render Docs**: https://render.com/docs
- **FastAPI on Render**: https://render.com/docs/deploy-fastapi
- **Docker on Render**: https://render.com/docs/docker
- **Troubleshooting**: https://render.com/docs/troubleshooting

---

## 💬 Support

If issues arise:
1. Check Render dashboard logs (Events tab)
2. Check build logs (Build & Deploys tab)
3. Test locally with Docker: `docker build -t gaitlab . && docker run -p 8000:8000 gaitlab`
4. Check GitHub for code issues

---

**Ready to deploy? Go to https://dashboard.render.com and follow Steps 1-5 above!**

