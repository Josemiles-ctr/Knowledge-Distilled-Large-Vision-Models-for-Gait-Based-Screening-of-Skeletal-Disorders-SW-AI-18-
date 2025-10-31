# Docker Hub Configuration Checklist

## Phase 1: Prepare Docker Hub Account
- [ ] Log in to Docker Hub at https://hub.docker.com
- [ ] Navigate to Account Settings → Security
- [ ] Create new Access Token named `"github-gaitanalysis-ci"`
- [ ] Set permissions to **"Read & Write"**
- [ ] **Copy the token** and save it temporarily

## Phase 2: Configure GitHub Secrets
- [ ] Go to GitHub repo: https://github.com/Josemiles-ctr/Knowledge-Distilled-Large-Vision-Models-for-Gait-Based-Screening-of-Skeletal-Disorders-SW-AI-18-
- [ ] Click **Settings** → **Secrets and variables** → **Actions**
- [ ] Create secret `DOCKERHUB_USERNAME` = `josemiles`
- [ ] Create secret `DOCKERHUB_TOKEN` = (paste your Docker Hub token)
- [ ] Verify both secrets appear in the list (values hidden as ***)

## Phase 3: Trigger Workflow

### Option A: Automatic (Git Push)
```bash
cd /home/otaijoseph/Desktop/GaitLab
git add .
git commit -m "chore: setup docker hub pipeline"
git push origin main
```
- [ ] Commit pushed successfully
- [ ] GitHub Actions workflow triggered automatically

### Option B: Manual Trigger
- [ ] Go to GitHub Actions tab: https://github.com/Josemiles-ctr/.../actions
- [ ] Select "Build and push Docker image to Docker Hub"
- [ ] Click "Run workflow" → "Run workflow"
- [ ] Workflow starts (status shows "Queued" then "In Progress")

## Phase 4: Monitor Build
- [ ] Watch workflow status change from 🟡 to 🟢
- [ ] **First build:** ~5-10 minutes
- [ ] **Cached builds:** ~1-3 minutes
- [ ] Check logs for any errors:
  - [ ] "Check secrets are configured" passes ✅
  - [ ] "Login to Docker Hub" succeeds ✅
  - [ ] "Build and push to Docker Hub" completes ✅

## Phase 5: Verify Docker Hub Image
- [ ] Visit: https://hub.docker.com/r/josemiles/gaitanalysis
- [ ] Confirm image exists and is public
- [ ] Check **Tags** section shows:
  - [ ] `latest` tag
  - [ ] Commit SHA tag (e.g., `abc1234567...`)
- [ ] View image size and last updated timestamp

## Phase 6: Test the Image
```bash
# Pull from Docker Hub
podman pull docker.io/josemiles/gaitanalysis:latest

# Run container
podman run -p 8000:8000 docker.io/josemiles/gaitanalysis:latest

# In another terminal, test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/ready
curl http://localhost:8000/conditions
```
- [ ] Container starts successfully
- [ ] Model loads and initializes
- [ ] `/health` returns `{"status":"ok"}`
- [ ] `/ready` returns `{"ready":true}`
- [ ] `/conditions` returns available clinical conditions

## Summary

✅ **When all checkboxes are complete:**
- GitHub Actions workflow is configured
- Docker images are automatically built on every push to `main`
- Images are pushed to Docker Hub with proper tags
- Pipeline is ready for production deployments

---

## Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| Workflow won't run | Check secrets are configured in GitHub |
| Login fails | Verify Docker Hub token has "Read & Write" permissions |
| Build takes too long | First build is slow; subsequent builds use cache |
| Large image size | Review `.dockerignore` and Python cache settings |
| Can't pull image | Ensure Docker Hub repo is public; check network/credentials |

---

## Quick Links
- Docker Hub Account: https://hub.docker.com/settings/general
- Docker Hub Security: https://hub.docker.com/settings/security
- GitHub Secrets: https://github.com/Josemiles-ctr/.../settings/secrets/actions
- GitHub Actions: https://github.com/Josemiles-ctr/.../actions

