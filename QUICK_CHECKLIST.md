# 🚀 QUICK ACTION CHECKLIST

## Get Docker Image to Docker Hub (5 steps)

### Step 1: Get Docker Hub Token ⏱️ 2 min
- [ ] Go to: https://hub.docker.com/settings/security
- [ ] Click "New Access Token"
- [ ] Name it: `github-gaitlab`
- [ ] Click "Create"
- [ ] Copy the token (you'll use it in Step 3)

### Step 2: Add GitHub Secrets ⏱️ 2 min
- [ ] Go to your GitHub repo
- [ ] Settings → Secrets and variables → Actions
- [ ] Click "New repository secret"
- [ ] Add Secret 1:
  - Name: `DOCKERHUB_USERNAME`
  - Value: `josemiles`
- [ ] Add Secret 2:
  - Name: `DOCKERHUB_TOKEN`
  - Value: (paste the token from Step 1)

### Step 3: Already Done! ⏱️ 0 min
- [x] GitHub Actions workflow updated ✓
- [x] Changes pushed to GitHub ✓

### Step 4: Trigger Build ⏱️ Auto
- [ ] Go to: https://github.com/Josemiles-ctr/Knowledge-Distilled-Large-Vision-Models-for-Gait-Based-Screening-of-Skeletal-Disorders-SW-AI-18-/actions
- [ ] Click "Build and push Docker image to Docker Hub"
- [ ] Click "Run workflow" → "Run workflow" again
- [ ] Wait 10-15 minutes while it builds

### Step 5: Verify ⏱️ 1 min
- [ ] Go to: https://hub.docker.com/repository/docker/josemiles/gaitanalysis
- [ ] Confirm `latest` tag appears
- [ ] Image size should be ~953 MB

---

## Then Deploy to Crane Cloud

Once Step 5 completes ✓

### Crane Cloud Setup ⏱️ 5 min
- [ ] Go to: https://dashboard.cranecloud.io
- [ ] Click: New Service → Container Image
- [ ] Image URL: `docker.io/josemiles/gaitanalysis:latest`
- [ ] Port: `8000`
- [ ] Add Environment Variables:
  - [ ] `CORS_ORIGINS` = `https://gait-ui.vercel.app`
  - [ ] `PORT` = `8000`
- [ ] Enable Health Check: `/ready`
- [ ] Click "Deploy"

### Wait for Deployment ⏱️ 10-15 min
- [ ] Watch logs in Crane Cloud dashboard
- [ ] Confirm service is "Running"
- [ ] Get public URL

### Test It ⏱️ 2 min
```bash
# Replace with your Crane Cloud URL
curl https://your-crane-service.com/health
# Should return: {"status":"ok"}
```

---

## Timeline

| Task | Duration | Start | End |
|------|----------|-------|-----|
| Get Docker Hub Token | 2 min | Now | +2 min |
| Add GitHub Secrets | 2 min | +2 min | +4 min |
| GitHub Actions builds | 15 min | +4 min | +19 min |
| Deploy to Crane Cloud | 5 min | +19 min | +24 min |
| **TOTAL** | **~25 min** | Now | **Ready!** |

---

## Questions?

- **GitHub Actions failing?** → Check: https://github.com/.../actions
- **Docker Hub token issues?** → Create new one: https://hub.docker.com/settings/security
- **Crane Cloud deployment issues?** → Follow: `CRANE_CLOUD_DEPLOYMENT.md`

