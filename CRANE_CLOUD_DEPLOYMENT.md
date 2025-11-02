# 🚀 Crane Cloud Deployment Guide

Crane Cloud is a Kubernetes-based platform. This guide explains how to deploy GaitLab independently to Crane Cloud without affecting your Render deployment.

## ⚡ Quick Start

Crane Cloud can use:
- **Option A**: Docker image from Docker Hub (recommended)
- **Option B**: Direct GitHub repo with buildpack
- **Option C**: Custom Dockerfile

---

## 🎯 Option A: Deploy from Docker Hub (Easiest)

### Prerequisites
1. Build and push image to Docker Hub (via GitHub Actions)
2. Crane Cloud account: https://app.cranecloud.io

### Steps

#### Step 1: Build Image
Trigger GitHub Actions workflow to build image:
```bash
git commit --allow-empty -m "Trigger Docker Hub build"
git push origin main
```
Wait ~20 minutes for build to complete on Docker Hub.

#### Step 2: Get Image URL
Once built, your image is at:
```
docker.io/josemiles/gaitanalysis:latest
```

#### Step 3: Deploy to Crane Cloud
1. Log in to Crane Cloud: https://app.cranecloud.io
2. Click **"New Project"** or **"Deploy Application"**
3. Choose **"Docker Image"**
4. Enter image URL: `docker.io/josemiles/gaitanalysis:latest`
5. Configure:
   - **Name**: `gaitlab-api`
   - **Container Port**: `8000`
   - **Replicas**: `1`
6. Click **"Deploy"**
7. Set environment variables (see below)
8. Wait for deployment (~5-10 minutes)

---

## ⚙️ Environment Variables for Crane Cloud

Set these in Crane Cloud console:

| Variable | Value |
|----------|-------|
| `CORS_ORIGINS` | `https://gait-ui.vercel.app` |
| `PORT` | `8000` |
| `PYTHONUNBUFFERED` | `1` |
| `PYTHONDONTWRITEBYTECODE` | `1` |

---

## 📊 Crane Cloud vs Render

| Feature | Render | Crane Cloud |
|---------|--------|-------------|
| **Ease** | Very easy | Moderate |
| **Cost** | $12/month | Pay-per-use (typically $5-10/month) |
| **Scaling** | Auto-scaling | Manual or auto (configurable) |
| **Support** | Great | Good |
| **Container Tech** | Docker | Kubernetes |

---

## 🔍 Deployment Details

### Health Check Configuration
Crane Cloud typically auto-discovers health checks. Configure:
- **Health Check Path**: `/health`
- **Timeout**: `10s`
- **Interval**: `30s`

### Resource Limits (Recommended)
- **CPU**: `500m` (0.5 CPU)
- **Memory**: `512Mi`
- **Disk**: As needed (model: ~50MB)

### Networking
- **Port**: `8000`
- **Protocol**: `HTTP`
- **Load Balancer**: Auto-assigned public URL

---

## 🧪 Testing After Deployment

Once deployed on Crane Cloud:

```bash
# Get your Crane Cloud URL (shown in dashboard)
export CRANE_URL="https://your-app.cranecloud.io"

# Test health endpoint
curl $CRANE_URL/health
# Expected: {"status":"ok"}

# Test ready endpoint
curl $CRANE_URL/ready
# Expected: {"ready":true}

# Test from frontend
# Update frontend API_BASE to point to Crane Cloud URL
```

---

## 🔐 Security Considerations

1. **CORS_ORIGINS**: Set to your frontend URL only
   - ✅ `https://gait-ui.vercel.app`
   - ❌ NOT `*`

2. **Docker Hub Image**: Public (anyone can pull)
   - OK for public API
   - Consider private repo if sensitive

3. **API Key**: None configured (public endpoint)
   - Add authentication if needed in future

---

## 📋 Troubleshooting

### Container Won't Start
- Check logs in Crane Cloud dashboard
- Verify CORS_ORIGINS is set
- Check PORT is 8000

### High Memory Usage
- Model uses ~500MB
- Increase memory limit if needed
- Or use Render's Standard tier instead

### Slow First Request
- Expected! Model loads on first request
- Subsequent requests: <500ms

---

## 🚀 Comparing Both Deployments

### Render
- Easier setup
- Built-in GitHub integration
- Great for quick deployment

### Crane Cloud
- More control (Kubernetes)
- Potentially cheaper
- Better for learning cloud deployment

---

## 💡 Pro Tips

1. **Test Locally First**
   ```bash
   docker run -p 8000:8000 \
     -e CORS_ORIGINS=http://localhost:3000 \
     docker.io/josemiles/gaitanalysis:latest
   ```

2. **Monitor Logs**
   - Crane Cloud dashboard has live logs
   - Check for model loading issues

3. **Scale if Needed**
   - Increase replicas in Crane Cloud for higher traffic
   - Or upgrade to Render Standard tier

---

## ✅ Crane Cloud Deployment Checklist

Before deploying:
- [ ] Docker Hub image built and available
- [ ] Crane Cloud account created
- [ ] Know your frontend URL
- [ ] CORS_ORIGINS env var ready
- [ ] Understand cost structure

After deploying:
- [ ] Service shows "Running"
- [ ] Health check passes
- [ ] Frontend can connect
- [ ] Monitor logs for errors

---

## 📚 Resources

- **Crane Cloud Docs**: https://docs.cranecloud.io
- **Kubernetes Basics**: https://kubernetes.io/docs/concepts/overview/
- **Docker Image Guide**: https://docs.docker.com/engine/reference/commandline/pull/

---

## 🎯 Summary

GaitLab can run on **both Render AND Crane Cloud independently**:
- Render: Already configured, almost live
- Crane Cloud: New option, uses Docker Hub image
- **No conflicts** - they operate independently

**Your Render deployment is untouched and continues to work.**

---

**Ready to try Crane Cloud?** Follow the steps above, or let me know if you need help!

