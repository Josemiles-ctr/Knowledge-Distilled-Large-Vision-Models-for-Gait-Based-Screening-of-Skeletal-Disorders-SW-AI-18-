# Docker Hub CI/CD Setup Guide

## Overview
This guide walks you through setting up automated Docker image builds and pushes to Docker Hub using GitHub Actions.

**Current Status:**
- ✅ Dockerfile: Ready (optimized Python 3.11-slim)
- ✅ GitHub Actions Workflow: Ready (`.github/workflows/docker-publish.yml`)
- ⏳ GitHub Secrets: **REQUIRED - Follow steps below**

---

## Step 1: Create Docker Hub Access Token

### 1.1 Log in to Docker Hub
Visit: https://hub.docker.com/login

### 1.2 Navigate to Account Settings
1. Click your profile icon (top-right)
2. Select **"Account Settings"**
3. Click **"Security"** in the left sidebar
4. Click **"New Access Token"**

### 1.3 Create the Token
1. **Token name:** Enter something descriptive like `"github-gaitanalysis-ci"`
2. **Access permissions:** Select **"Read & Write"**
3. Click **"Generate"**
4. **Copy the token** and save it somewhere safe (you won't see it again!)

---

## Step 2: Add Secrets to GitHub Repository

### 2.1 Navigate to GitHub Secrets
1. Go to your repository: https://github.com/Josemiles-ctr/Knowledge-Distilled-Large-Vision-Models-for-Gait-Based-Screening-of-Skeletal-Disorders-SW-AI-18-
2. Click **Settings** (top-right, gear icon)
3. In left sidebar, click **Secrets and variables** → **Actions**

### 2.2 Add Secret #1: Docker Hub Username
1. Click **"New repository secret"**
2. **Name:** `DOCKERHUB_USERNAME`
3. **Value:** Your Docker Hub username (e.g., `josemiles`)
4. Click **"Add secret"**

### 2.3 Add Secret #2: Docker Hub Token
1. Click **"New repository secret"** again
2. **Name:** `DOCKERHUB_TOKEN`
3. **Value:** Paste the token you copied from Docker Hub (Step 1.3)
4. Click **"Add secret"**

✅ You should now see both secrets listed (values shown as `***`)

---

## Step 3: Verify GitHub Actions Workflow

### 3.1 Check Workflow File
The workflow is located at: `.github/workflows/docker-publish.yml`

**What it does:**
1. ✅ Checks out your code
2. ✅ Verifies GitHub Secrets are configured
3. ✅ Sets up Docker Buildx (multi-arch support)
4. ✅ Logs into Docker Hub
5. ✅ Builds Docker image
6. ✅ Pushes to Docker Hub with tags:
   - `docker.io/josemiles/gaitanalysis:latest`
   - `docker.io/josemiles/gaitanalysis:<commit-sha>`

### 3.2 Trigger Events
The workflow runs automatically on:
- ✅ Push to `main` branch
- ✅ Manual trigger via GitHub UI (`workflow_dispatch`)

---

## Step 4: Trigger the Workflow

### Option A: Automatic (Recommended)
Push a commit to the `main` branch:
```bash
cd /home/otaijoseph/Desktop/GaitLab
git add .
git commit -m "chore: configure docker hub pipeline" 
git push origin main
```

### Option B: Manual Trigger
1. Go to: https://github.com/Josemiles-ctr/.../actions
2. Select **"Build and push Docker image to Docker Hub"** workflow
3. Click **"Run workflow"** (top-right)
4. Confirm the branch is `main`
5. Click **"Run workflow"**

---

## Step 5: Monitor the Workflow

### 5.1 Watch the Build
1. Go to: https://github.com/Josemiles-ctr/.../actions
2. Click the latest workflow run
3. Watch the status:
   - 🟡 **Queued** → Starting
   - 🟡 **In Progress** → Building
   - 🟢 **Completed** → Success!
   - 🔴 **Failed** → Check logs for errors

**Build time:** ~5-10 minutes (first time), ~1-3 minutes (with cache)

### 5.2 View Workflow Logs
Click on each step to expand and see details:
- **Checkout repository** - Should complete instantly
- **Check secrets are configured** - Should show ✅
- **Set up Docker Buildx** - Prepares build environment
- **Login to Docker Hub** - Authenticates with token
- **Build and push to Docker Hub** - Main build step (takes longest)

---

## Step 6: Verify Image on Docker Hub

### 6.1 Check Repository
Visit: https://hub.docker.com/r/josemiles/gaitanalysis

You should see:
- 📦 **Tags** tab showing `latest` and commit SHA
- 📊 **Image layers** (Python, dependencies, your code)
- 📝 **Repo description** (optional to update)

### 6.2 Pull and Test Locally
```bash
# Pull the image
podman pull docker.io/josemiles/gaitanalysis:latest

# Run it
podman run -p 8000:8000 \
  -e MODEL_PATH=/app/models/gait_predict_model_v_1.pth \
  docker.io/josemiles/gaitanalysis:latest

# In another terminal, test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/ready
```

---

## Troubleshooting

### ❌ Workflow fails with "secrets not configured"
- Go to **Settings → Secrets and variables → Actions**
- Ensure both secrets exist:
  - `DOCKERHUB_USERNAME`
  - `DOCKERHUB_TOKEN`

### ❌ Login fails (Invalid credentials)
- Verify token copied correctly from Docker Hub (Step 1.3)
- Ensure token has "Read & Write" permissions
- Try generating a new token

### ❌ Build fails with "permission denied"
- Check if repository is set to private
- Ensure Docker Hub account is not out of free tier limits

### ❌ Image is very large (>1GB)
- Check `.dockerignore` excludes unnecessary files
- Verify `pip install --no-cache-dir` is used
- Consider multi-stage builds if needed

---

## Next Steps

After successful push:

1. **Update Deployment Configs:**
   - Update `render.yaml` to pull from Docker Hub
   - Update Kubernetes manifests if using K8s

2. **Automate Deployments:**
   - Configure Render to auto-deploy on image push
   - Set up CD pipeline for deployments

3. **Monitor Production:**
   - Set up health checks
   - Enable image scanning for vulnerabilities
   - Configure auto-rollback on failures

---

## Quick Reference

| Item | Value |
|------|-------|
| **Docker Hub Repo** | `docker.io/josemiles/gaitanalysis` |
| **Workflow File** | `.github/workflows/docker-publish.yml` |
| **GitHub Secrets URL** | `https://github.com/Josemiles-ctr/.../settings/secrets/actions` |
| **Docker Hub Security** | `https://hub.docker.com/settings/security` |
| **GitHub Actions** | `https://github.com/Josemiles-ctr/.../actions` |

---

## Testing the Pipeline Locally (Optional)

To test the Docker build before pushing:

```bash
cd /home/otaijoseph/Desktop/GaitLab

# Build locally
podman build -t gaitanalysis:test .

# Run and test
podman run -p 8000:8000 gaitanalysis:test

# Test endpoints in another terminal
curl http://localhost:8000/health
```

---

## Support
If you encounter issues:
1. Check GitHub Actions logs: https://github.com/Josemiles-ctr/.../actions
2. Review Dockerfile syntax
3. Verify all environment variables are set
4. Check Docker Hub account status

