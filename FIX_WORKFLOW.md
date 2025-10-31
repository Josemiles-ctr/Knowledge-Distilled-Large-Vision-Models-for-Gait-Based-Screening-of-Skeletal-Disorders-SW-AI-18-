# ⚠️ GitHub Actions Workflow Failed - Fix Guide

## Why It Failed

The workflow needs **GitHub Secrets** to log into Docker Hub and push the image. Without these secrets, the build is blocked.

---

## ✅ **EXACT STEPS TO FIX (Copy-Paste Ready)**

### **Step 1: Open GitHub Secrets Page**

Click this link (or navigate manually):
```
https://github.com/josemiles/gaitanalysis/settings/secrets/actions
```

### **Step 2: Add First Secret (DOCKERHUB_USERNAME)**

1. Click **"New repository secret"** button (top right)
2. In "Name" field type:
   ```
   DOCKERHUB_USERNAME
   ```
3. In "Value" field type:
   ```
   josemiles
   ```
4. Click **"Add secret"**

### **Step 3: Add Second Secret (DOCKERHUB_TOKEN)**

1. Click **"New repository secret"** button again
2. In "Name" field type:
   ```
   DOCKERHUB_TOKEN
   ```
3. In "Value" field paste your Docker Hub access token (from Docker Hub Account Settings → Security)
   - **⚠️ Important**: Create a token if you don't have one:
     - Go to: https://hub.docker.com/settings/security
     - Click "New Access Token"
     - Give it a name (e.g., "github-actions")
     - Click "Generate"
     - Copy the token (you won't see it again!)
     - Paste it here in GitHub

4. Click **"Add secret"**

### **Step 4: Verify Both Secrets Are Added**

Your **Actions secrets** page should now show:
```
DOCKERHUB_USERNAME = ****** (hidden)
DOCKERHUB_TOKEN = ****** (hidden)
```

---

## 🚀 **Step 5: Trigger Workflow Again**

Now that secrets are added, trigger the workflow:

**Option A (Automatic)**: Just push any change:
```bash
cd /home/otaijoseph/Desktop/GaitLab
git commit --allow-empty -m "Trigger workflow after adding secrets"
git push origin main
```

**Option B (Manual)**: Go to GitHub Actions tab:
1. Click the **"Build and push Docker image to Docker Hub"** workflow
2. Click **"Run workflow"**
3. Select branch **main**
4. Click **"Run workflow"**

---

## 📊 **Step 6: Monitor the Build**

Go to: `https://github.com/josemiles/gaitanalysis/actions`

Watch the workflow:
- ✅ **"Check secrets are configured"** - Should now pass (secrets found)
- ✅ **"Checkout repository"** - Should pass
- ✅ **"Set up Docker Buildx"** - Should pass
- ✅ **"Login to Docker Hub"** - Should pass (with your token)
- ✅ **"Build and push to Docker Hub"** - Should pass (~5-10 min)

If any step fails, click it to see the error logs.

---

## ✅ **Step 7: Verify Image on Docker Hub**

Once workflow completes successfully:

1. Go to: `https://hub.docker.com/r/josemiles/gaitanalysis`
2. You should see:
   - Repository: `josemiles/gaitanalysis`
   - Tags: `latest` (and short commit SHA)
   - Last pushed: just now

---

## 🧪 **Step 8: Test the Image Locally**

```bash
# Pull the image from Docker Hub
docker pull docker.io/josemiles/gaitanalysis:latest

# Run it locally
docker run -d -p 8000:8000 docker.io/josemiles/gaitanalysis:latest

# Test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/ready

# View logs
docker logs <container-id>

# Stop when done
docker stop <container-id>
```

---

## 🆘 **If It Still Fails**

Click the failed workflow run and check the logs for:

1. **"Invalid authentication scope"** → Token doesn't have write permission (create new token with broader scope)
2. **"Authentication failed"** → Username/token incorrect (verify in Docker Hub Account Settings)
3. **"Repository not found"** → Repository doesn't exist on Docker Hub (create it via web UI)
4. **"Disk space"** → GitHub runner out of space (rarely happens; try again)
5. **Pip install errors** → Dependency issue (check requirements.txt compatibility)

---

## 📝 **Quick Reference**

| Item | Value |
|------|-------|
| **GitHub Repo** | https://github.com/josemiles/gaitanalysis |
| **GitHub Actions** | https://github.com/josemiles/gaitanalysis/actions |
| **GitHub Secrets** | https://github.com/josemiles/gaitanalysis/settings/secrets/actions |
| **Docker Hub Repo** | https://hub.docker.com/r/josemiles/gaitanalysis |
| **Docker Hub Token** | https://hub.docker.com/settings/security |

---

## ✨ Done!

Once the workflow succeeds, you have:
- ✅ Fully automated CI/CD
- ✅ Docker image auto-built on every push
- ✅ Image auto-pushed to Docker Hub
- ✅ Production-ready containerized app
- ✅ Easy deployment to Render, Kubernetes, or anywhere

**Every future `git push origin main` will automatically rebuild and push a new image!** 🚀
