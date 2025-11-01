# GitHub Secrets Setup for Docker Hub Push

## ❌ Why Workflows Are Failing

All workflow runs are failing because **GitHub Secrets are not configured**. The workflow needs:
- `DOCKERHUB_USERNAME` - Your Docker Hub username
- `DOCKERHUB_TOKEN` - Your Docker Hub access token

## ✅ Step-by-Step Setup

### Step 1: Create Docker Hub Access Token

1. Go to https://hub.docker.com/settings/security
2. Click **"New Access Token"**
3. Fill in:
   - **Access Token Description**: `GitHub Actions` (or similar)
   - **Access Permissions**: Select `Read, Write, Delete`
4. Click **"Generate"**
5. **Copy the token** (you won't see it again!)
6. Save it somewhere safe (clipboard for now)

### Step 2: Add Secrets to GitHub Repository

1. Go to your GitHub repository: 
   ```
   https://github.com/Josemiles-ctr/Knowledge-Distilled-Large-Vision-Models-for-Gait-Based-Screening-of-Skeletal-Disorders-SW-AI-18-
   ```

2. Click **Settings** tab → **Secrets and variables** → **Actions**

3. Click **"New repository secret"**

4. **First Secret - Username**:
   - Name: `DOCKERHUB_USERNAME`
   - Secret: `josemiles` (your Docker Hub username)
   - Click **"Add secret"**

5. Click **"New repository secret"** again

6. **Second Secret - Token**:
   - Name: `DOCKERHUB_TOKEN`
   - Secret: (paste the token you copied in Step 1)
   - Click **"Add secret"**

### Step 3: Verify Secrets Are Set

After adding both secrets, you should see:
- ✅ `DOCKERHUB_USERNAME` (value hidden)
- ✅ `DOCKERHUB_TOKEN` (value hidden)

## 🚀 Step 4: Trigger Workflow

Now that secrets are configured, the workflow will work. Trigger it by:

### Option A: Push a commit
```bash
git commit --allow-empty -m "Trigger workflow after adding secrets"
git push origin main
```

### Option B: Manual trigger
1. Go to **Actions** tab
2. Select **"Build and push Docker image to Docker Hub"**
3. Click **"Run workflow"** → **"Run workflow"**

## 📊 Workflow Steps Explained

When the workflow runs, it will:

1. **Checkout code** - Get latest code from main branch
2. **Check secrets** - Verify DOCKERHUB_USERNAME and DOCKERHUB_TOKEN exist
3. **Setup Buildx** - Prepare Docker build system
4. **Login to Docker Hub** - Authenticate using your token
5. **Build and push** - Build image and push to `docker.io/josemiles/gaitanalysis:latest`

## ⏱️ Build Time

- **First build**: ~8-12 minutes (builds all layers)
- **Subsequent builds**: ~3-5 minutes (uses cache)

## ✅ Verify Success

After workflow completes:

1. Check Docker Hub: https://hub.docker.com/r/josemiles/gaitanalysis
2. Should see tags: `latest` and short commit SHA
3. Test locally:
   ```bash
   docker pull docker.io/josemiles/gaitanalysis:latest
   docker run -p 8000:8000 docker.io/josemiles/gaitanalysis:latest
   ```

## 🔐 Security Notes

- **Never share your Docker Hub token** - It's like a password
- GitHub keeps secrets encrypted
- Secrets are never printed in workflow logs (shown as `***`)
- Delete old tokens you no longer use on Docker Hub

## ❓ Troubleshooting

### "requested access to the resource is denied"
- Token was created without correct permissions
- Create new token with `Read, Write, Delete` permissions

### "repository name must be lowercase"
- Use `docker.io/josemiles/gaitanalysis` (lowercase)
- Already correct in workflow

### "Secret not found"
- Make sure you added BOTH secrets (username AND token)
- Secret names must match exactly (case-sensitive)

