# Deploying GaitLab to Render (step-by-step)

This document contains copy-paste-ready instructions and a small `render.yaml` blueprint template to deploy this repository to Render (free web service). It assumes your repository already contains a working `Dockerfile`, `scripts/download_model.sh`, a `/ready` readiness endpoint and a model download flow using `MODEL_URL` / `MODEL_PATH`.

If you want, you can paste the `render.yaml` template into your repo and then import it from the Render dashboard, or follow the UI steps below.

---

## Quick checklist (before you start)

- Ensure your repo is pushed to GitHub/GitLab/Bitbucket and the `Dockerfile` is at the repository root.
- Confirm the repository contains `scripts/download_model.sh` (this repo does) and that it will download the model when `MODEL_URL` is set.
- Verify your `Dockerfile` starts uvicorn using the `PORT` environment variable (this repo's Dockerfile already uses `${PORT}`).
- Prepare a model URL (S3 presigned link or other public HTTPS link) if you want Render to download the model at startup. Treat presigned URLs as secrets.

---

## Render Dashboard steps (exact values to copy)

1. Log in to https://dashboard.render.com and click New → Web Service.
2. Choose "Build and deploy from a Git repository" and connect your Git provider.
3. Select your repository and branch (e.g., `main`).
4. Fill the service form using the fields below (copy/paste):

- Name: `gaitlab` (or any unique name)
- Region: _pick nearest region_
- Branch: `main`
- Environment: `Docker` (Render will detect your `Dockerfile`)
- Build Command: (leave blank — Dockerfile handles build)
- Start Command: (leave blank — Dockerfile CMD handles startup). If Render requires one, use:
  `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Instance Type: `Free` (for no-cost testing; switch to paid if you need more RAM/CPU)

Under Advanced:

- Health Check Path: `/ready`
- Persistent Disk: Optional, recommended if your model is large and you want it cached between restarts. (e.g., 5 or 10 GB)
- Environment variables / Secrets (click Add):
  - `MODEL_PATH` = `/app/models/gait_predict_model_v_1.pth` (optional; the Dockerfile uses this default)
  - `MODEL_URL` = `<YOUR_PRESIGNED_MODEL_URL>` (set this as a secret value; do not commit it to Git)

5. Click Create Web Service. Render will queue a build.

6. Open the service page and watch Logs / Events for the following sequence:
  - Docker image build completes.
  - Container starts and runs `/app/scripts/download_model.sh` (if `MODEL_URL` set) — look for "Model downloaded to" message.
  - Uvicorn starts and listens on the port Render assigns (your Dockerfile uses `${PORT}`).
  - `/ready` returns HTTP 200 once model initialization is complete.

7. Test your endpoints once `/ready` returns 200 (see curl commands below).

---

## Example curl commands (replace `<your-service>` with your Render service domain)

Health check:

```bash
curl -i https://<your-service>.onrender.com/health
```

Readiness:

```bash
curl -i https://<your-service>.onrender.com/ready
```

Predict (send a small test video from your local machine):

```bash
curl -X POST \
  -F "video=@test_video.mp4;type=video/mp4" \
  -F "clinical_condition=patient with slight gait instability" \
  https://<your-service>.onrender.com/predict
```

If your Render service is `gaitlab`, the URL will be `https://gaitlab.onrender.com`.

---

## Sample `render.yaml` blueprint (template)

This blueprint is a template you can adapt and then import into Render's Blueprints (Infrastructure-as-Code). Replace placeholder values (the `<>` parts) before using.

```yaml
# render.yaml - Render blueprint template (edit placeholders before use)
services:
  - type: web
    name: gaitlab
    env: docker
    repo: <GIT_REPO_URL_OR_OWNER/REPO>
    branch: main
    buildCommand: ''
    startCommand: ''
    healthCheckPath: /ready
    instanceType: free
    disk:
      sizeGb: 5
    envVars:
      - key: MODEL_PATH
        value: /app/models/gait_predict_model_v_1.pth
      - key: MODEL_URL
        from: secret

# Note: This is a minimal template. Adjust disk.sizeGb or instanceType if you need more resources.
```

Important: Render's blueprint schema has additional fields and variants (e.g., `secrets`, `databases`). Use the Render docs if you want to expand this into a full project-level blueprint.

---

## Troubleshooting & notes (most common issues)

- Build failures during pip installs: check Docker build logs — add system packages to `apt-get install` in `Dockerfile` for missing libs (your `Dockerfile` already includes `build-essential`, `gcc`, `ffmpeg`, `libgl1`, `libglib2.0-0`, and `libsndfile1`).
- Model download errors (403/404): verify the `MODEL_URL` is valid and not expired. Use a presigned URL with sufficient TTL.
- OOM / Killed process: the free instance may not have enough RAM for large PyTorch models. Options:
  - Use a smaller / quantized model.
  - Bake the model into a prebuilt Docker image and deploy from a container registry (avoids download step and runtime memory spikes during build).
  - Use persistent disk and populate with model via a separate one-off job.
- Health check failing: confirm `/ready` returns 200. If model failed to load, logs will show the Python exception and stack trace.

---

If you'd like, I can:

- Create this `render.yaml` in your repo (with placeholders) so you can edit it and import; or
- Create a small `DEPLOY_RENDER.md` in your repo (I added this file) and also add a short `README` snippet into the repo's main `README.md` for team members.

If you want me to commit `render.yaml` with your repo name and the repo URL already filled in, paste the repo remote URL here (or confirm the exact name) and I'll add it.

## Prebuilt image (recommended for large models)

If your PyTorch model is large (tens or hundreds of MBs), I recommend building a prebuilt Docker image that includes the model artifact. This avoids model download during startup (which can fail due to timeouts or memory constraints on Render free instances).

I added `Dockerfile.baked` and `scripts/build_and_push_image.sh` to this repository. Quick summary of how to use them locally:

1. Place your model file at `./models/gait_predict_model_v_1.pth` (create `models/` if needed).
2. Build the image locally and tag it:

```bash
DOCKER_REPO=yourdockerhubuser/gaitlab TAG=latest MODEL_LOCAL_PATH=./models/gait_predict_model_v_1.pth \
  ./scripts/build_and_push_image.sh
```

3. To push to a remote registry (Docker Hub) you must first `docker login` and then run with `--push`:

```bash
DOCKER_REPO=yourdockerhubuser/gaitlab TAG=latest MODEL_LOCAL_PATH=./models/gait_predict_model_v_1.pth \
  ./scripts/build_and_push_image.sh --push
```

4. In Render choose "Deploy from a container registry" and point to `docker.io/yourdockerhubuser/gaitlab:latest` (replace with your registry and tag). Set the same environment variables in Render if needed (MODEL_PATH can remain the default).

This approach is the most reliable for large models on Render free instances.

---

End of guide.
