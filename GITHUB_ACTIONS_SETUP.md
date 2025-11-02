# 🔐 GitHub Secrets Setup for Docker Hub

## ⚠️ REQUIRED BEFORE WORKFLOW RUNS

Your GitHub Actions workflow will **automatically build and push** Docker images to Docker Hub, but you need to set up 2 secrets first.

---

## 📋 Step 1: Get Docker Hub Access Token

1. Go to: https://hub.docker.com/settings/security
2. Click **"New Access Token"**
3. Name it: `github-gaitlab` (or any name)
4. Click **"Create"**
5. **COPY** the token (you won't see it again!)
6. Keep it safe - you'll use it next

---

## 🔑 Step 2: Add GitHub Secrets

1. Go to your GitHub repo
2. Click **Settings** (top right)
3. Left sidebar → **Secrets and variables** → **Actions**
4. Click **"New repository secret"**

### Secret 1: DOCKERHUB_USERNAME
```
Name: DOCKERHUB_USERNAME
Value: josemiles
```
Click "Add secret"

### Secret 2: DOCKERHUB_TOKEN
```
Name: DOCKERHUB_TOKEN
Value: (paste the token from Step 1)
```
Click "Add secret"

---

## ✅ Verify Secrets Are Set

After adding both secrets, you should see:
```
✓ DOCKERHUB_USERNAME
✓ DOCKERHUB_TOKEN
```

---

## 🚀 What Happens Next

Once secrets are set, any push to GitHub will **automatically**:

1. Trigger GitHub Actions workflow
2. Build Docker image from your code
3. Push to Docker Hub as `docker.io/josemiles/gaitanalysis:latest`
4. Takes ~15-20 minutes

---

## 🎯 Trigger First Build

After secrets are configured, do this:

```bash
cd /home/otaijoseph/Desktop/GaitLab
git add .
git commit -m "chore: enable GitHub Actions workflow"
git push origin main
```

Then watch: https://github.com/Josemiles-ctr/Knowledge-Distilled-Large-Vision-Models-for-Gait-Based-Screening-of-Skeletal-Disorders-SW-AI-18-/actions

---

## ✨ After First Successful Build

Your image will be available at:
```
docker.io/josemiles/gaitanalysis:latest
```

Then you can:
- Deploy to Crane Cloud
- Deploy to Render
- Use locally with `docker pull`

---

## 🆘 If Workflow Fails

1. Go to **Actions** tab
2. Click the failed workflow
3. Check the error message
4. Common issues:
   - Secrets not set → Follow Step 1 & 2 again
   - Token expired → Create new token on Docker Hub
   - Image size too large → Already optimized ✅

---

## ⏱️ Timeline

| Action | Time |
|--------|------|
| Add secrets | 2 min |
| Push code | 1 min |
| GitHub Actions builds | 15 min |
| **Total** | **~18 min** |

