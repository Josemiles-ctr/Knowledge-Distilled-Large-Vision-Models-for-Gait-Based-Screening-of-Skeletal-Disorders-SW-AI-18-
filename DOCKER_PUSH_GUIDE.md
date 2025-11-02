# Docker Hub Push Guide - GitHub Actions Approach

## Problem with Local Podman Push

When trying to push locally with Podman to Docker Hub, you get:
```
Error: requested access to the resource is denied
```

This is due to Podman/Docker Hub authentication issues. **The solution: Use GitHub Actions instead!**

---

## ✅ Recommended Solution: GitHub Actions (Automatic)

GitHub Actions will **automatically** build and push your image to Docker Hub whenever you push to GitHub.

### Step 1: Set GitHub Secrets

1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add these two secrets:

**Secret 1: DOCKERHUB_USERNAME**
- Name: `DOCKERHUB_USERNAME`
- Value: `josemiles` (your Docker Hub username)

**Secret 2: DOCKERHUB_TOKEN**
- Name: `DOCKERHUB_TOKEN`
- Value: Your Docker Hub access token (get it from Docker Hub settings)

#### How to Get Docker Hub Token:
1. Go to https://hub.docker.com/settings/security
2. Click "New Access Token"
3. Name it: `github-gaitlab`
4. Click "Create"
5. Copy the token and paste it in GitHub Secrets

### Step 2: Push to GitHub

```bash
cd /home/otaijoseph/Desktop/GaitLab
git add .
git commit -m "fix: update Docker image name in GitHub Actions workflow"
git push origin main
```

### Step 3: GitHub Actions Automatically Builds & Pushes

1. Go to your GitHub repo
2. Click "Actions" tab
3. Watch "Build and push Docker image to Docker Hub" run
4. Wait ~10-15 minutes
5. Image appears on Docker Hub automatically!

---

## 🎯 After GitHub Actions Completes

Your image will be available at:
```
docker.io/josemiles/gaitanalysis:latest
```

Then you can use it anywhere:

### For Crane Cloud:
```
Image URL: docker.io/josemiles/gaitanalysis:latest
Port: 8000
Environment Variables:
  CORS_ORIGINS: https://gait-ui.vercel.app
  PORT: 8000
```

### For Local Testing:
```bash
podman pull docker.io/josemiles/gaitanalysis:latest
podman run -p 8000:8000 -e CORS_ORIGINS=http://localhost:3000 docker.io/josemiles/gaitanalysis:latest
```

---

## ⚠️ Troubleshooting GitHub Actions

### If Workflow Fails:

1. **Secrets not set**: Check GitHub → Settings → Secrets
2. **Token expired**: Generate a new Docker Hub token
3. **Image size too large**: Already optimized to ~953 MB
4. **Build fails**: Check error logs in Actions tab

### Check Workflow Status:

1. Go to: https://github.com/Josemiles-ctr/Knowledge-Distilled-Large-Vision-Models-for-Gait-Based-Screening-of-Skeletal-Disorders-SW-AI-18-/actions
2. Look for "Build and push Docker image to Docker Hub"
3. Click on latest run to see logs

---

## 📊 Comparison: Local vs GitHub Actions

| Aspect | Local Podman | GitHub Actions |
|--------|-------------|-----------------|
| **Complexity** | Medium (auth issues) | Simple (automated) |
| **Speed** | Fast (your machine) | Slower (cloud build) |
| **Reliability** | Problems with Docker Hub | Reliable, battle-tested |
| **When runs** | Whenever you want | Auto on each push |
| **Best for** | Quick testing | Production deployments |

**Recommendation**: Use GitHub Actions ✅

---

## 🎁 What You Get

Once GitHub Actions completes successfully:

✅ Image automatically built from latest GitHub code
✅ Image pushed to Docker Hub
✅ Available at `docker.io/josemiles/gaitanalysis:latest`
✅ Works with Render, Crane Cloud, local deployment
✅ Automatic updates on each GitHub push

---

## Next Steps

1. Create/get Docker Hub access token
2. Add DOCKERHUB_USERNAME secret to GitHub
3. Add DOCKERHUB_TOKEN secret to GitHub
4. Push this guide to GitHub
5. Watch GitHub Actions build and push automatically
6. Use image in Crane Cloud/Render

**Total time**: ~5 minutes setup + 15 minutes for first build

