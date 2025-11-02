# 🔗 Frontend Communication - Environment Variables Guide

## Overview

Your GaitLab API uses environment variables to configure CORS (Cross-Origin Resource Sharing), which controls which frontend domains can access your API.

---

## 🎯 Quick Start

### For Local Development (Default)
Your API allows requests from:
- `http://localhost:5173` (Svelte default)
- `http://localhost:3000` (React default)

**No configuration needed** - just works!

### For Production / Render Deployment
You **must set the `CORS_ORIGINS` environment variable** to your frontend URL.

---

## 📋 All Environment Variables

### CORS Configuration (Frontend Communication)

| Variable | Default | Example | Purpose |
|----------|---------|---------|---------|
| `CORS_ORIGINS` | `http://localhost:5173,http://localhost:3000` | `https://myapp.com,https://app.myapp.com` | Frontend domains allowed to call your API |
| `CORS_METHODS` | `GET,POST,PUT,DELETE,OPTIONS` | (usually same) | HTTP methods allowed |
| `CORS_HEADERS` | `Content-Type,Authorization,Accept` | (usually same) | HTTP headers allowed |

### Server Configuration

| Variable | Default | Example | Purpose |
|----------|---------|---------|---------|
| `PORT` | `8000` | `8000` or `3000` | API port (Render: keep 8000) |
| `HOST` | `0.0.0.0` | `0.0.0.0` | Listen on all interfaces |
| `WORKERS` | `8` | `4` or `8` | Uvicorn worker processes |
| `TIMEOUT` | `300` | `300` | Request timeout in seconds (5 min for model inference) |

### Model Configuration

| Variable | Default | Example | Purpose |
|----------|---------|---------|---------|
| `MODEL_PATH` | `models/gait_predict_model_v_1.pth` | (usually same) | Path to model weights file |
| `NUM_FRAMES` | `16` | `16` or `32` | Video frames to analyze |
| `FRAME_SIZE` | `224` | `224` or `256` | Video frame resolution |

### Storage Configuration

| Variable | Default | Example | Purpose |
|----------|---------|---------|---------|
| `TEMP_UPLOAD_DIR` | `/tmp` | `/tmp` or `/var/tmp` | Temporary file storage |
| `MAX_UPLOAD_SIZE` | `104857600` | `104857600` (100MB) | Max video file size in bytes |

---

## 🚀 Setup for Your Frontend

### Step 1: Know Your Frontend URL

**Local Development:**
- Svelte: `http://localhost:5173`
- React: `http://localhost:3000`
- Vue: `http://localhost:5174`

**Production:**
- If deployed to Vercel: `https://yourapp.vercel.app`
- If deployed to Netlify: `https://yourapp.netlify.app`
- If self-hosted: `https://yourdomain.com`

### Step 2: Set CORS_ORIGINS Environment Variable

#### Local Development (No Action Needed!)
Default settings already allow:
```
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

#### Render Deployment

**Option A: Render Dashboard (Easiest)**
1. Go to your service in Render dashboard
2. Click **"Environment"** tab
3. Click **"Add Environment Variable"**
4. Name: `CORS_ORIGINS`
5. Value: `https://yourfrontend.vercel.app` (or your domain)
6. Click **"Save"**
7. Service redeploys automatically

**Option B: Multiple Frontend Domains**
If your frontend is deployed in multiple places:
```
CORS_ORIGINS=https://yourapp.vercel.app,https://yourapp.netlify.app,https://yourdomain.com
```

**Option C: Allow All (Development Only!)**
```
CORS_ORIGINS=*
```
⚠️ Not recommended for production - use specific domains!

#### Local Docker

```bash
docker run -e CORS_ORIGINS=http://localhost:3000 \
  -p 8000:8000 \
  docker.io/josemiles/gaitanalysis:latest
```

#### Docker Compose

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  api:
    image: docker.io/josemiles/gaitanalysis:latest
    ports:
      - "8000:8000"
    environment:
      PORT: 8000
      CORS_ORIGINS: http://localhost:3000
      CORS_METHODS: GET,POST,PUT,DELETE,OPTIONS
      CORS_HEADERS: Content-Type,Authorization,Accept
```

Then run:
```bash
docker-compose up
```

#### Environment File (.env)

Create `.env`:
```
PORT=8000
CORS_ORIGINS=http://localhost:3000,https://myapp.com
CORS_METHODS=GET,POST,PUT,DELETE,OPTIONS
CORS_HEADERS=Content-Type,Authorization,Accept
```

Then in your shell:
```bash
export $(cat .env | xargs)
python -m uvicorn main:app
```

---

## 🧪 Testing Frontend Communication

### Test 1: Local Development
```bash
# Terminal 1: Start API
cd /home/otaijoseph/Desktop/GaitLab
source envir/bin/activate
uvicorn main:app --reload

# Terminal 2: Call from frontend (localhost:3000)
curl -X GET http://localhost:8000/health
# Expected: {"status":"ok"}
```

### Test 2: CORS Check
```bash
# Test if your frontend domain is allowed
curl -X OPTIONS http://localhost:8000/health \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  -v

# Look for response headers:
# Access-Control-Allow-Origin: http://localhost:3000
# Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
# Access-Control-Allow-Headers: Content-Type, Authorization, Accept
```

### Test 3: Frontend Code
```javascript
// In your React/Vue/Svelte component
fetch('http://localhost:8000/health', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json',
  }
})
.then(r => r.json())
.then(data => console.log(data))
.catch(err => console.error('CORS error:', err))
```

---

## ⚙️ Recommended Settings

### For Local Development
```
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
PORT=8000
TIMEOUT=300
```

### For Render Production
```
CORS_ORIGINS=https://your-frontend.vercel.app
PORT=8000
TIMEOUT=300
MAX_UPLOAD_SIZE=104857600
```

### For Multiple Environments
```
CORS_ORIGINS=http://localhost:3000,https://your-frontend.vercel.app,https://yourdomain.com
```

---

## 🔍 Troubleshooting

### Frontend Can't Call API

**Error**: `Access to XMLHttpRequest blocked by CORS policy`

**Solution**:
1. Check frontend URL exactly (protocol, domain, port)
2. Add to `CORS_ORIGINS` environment variable
3. Restart the API service

**Example**: If frontend is at `https://app.example.com`, set:
```
CORS_ORIGINS=https://app.example.com
```

### OPTIONS Request Fails

**Error**: `Method not allowed`

**Solution**:
- Ensure `CORS_METHODS` includes `OPTIONS`
- Default includes it, so usually not needed to change

### Header Not Allowed

**Error**: `Missing or invalid Access-Control-Allow-Headers`

**Solution**:
- Add header to `CORS_HEADERS` environment variable
- Example: `CORS_HEADERS=Content-Type,Authorization,Accept,X-Custom-Header`

---

## 📝 Common Use Cases

### Use Case 1: Vercel Frontend + Render Backend
```
CORS_ORIGINS=https://myapp.vercel.app
```

### Use Case 2: Netlify Frontend + Render Backend
```
CORS_ORIGINS=https://myapp.netlify.app
```

### Use Case 3: Multiple Frontends
```
CORS_ORIGINS=https://myapp.vercel.app,https://admin.myapp.com,https://yourdomain.com
```

### Use Case 4: Development + Production
```
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,https://myapp.vercel.app
```

---

## 🔐 Security Best Practices

1. **Never use `*` in production**
   - ❌ `CORS_ORIGINS=*` (allows anyone)
   - ✅ `CORS_ORIGINS=https://myapp.com` (specific domain)

2. **Use HTTPS in production**
   - ❌ `http://myapp.com`
   - ✅ `https://myapp.com`

3. **Include exact ports if needed**
   - ❌ `https://myapp.com` (if deployed on non-standard port)
   - ✅ `https://myapp.com:3000`

4. **Don't put secrets in CORS_ORIGINS**
   - This is meant for domain allowlisting only

---

## 📚 API Endpoints for Frontend

Once CORS is configured, your frontend can call:

```javascript
const API_BASE = 'http://localhost:8000'; // or https://your-deployed-api.com

// Health check
GET /health
// Response: {"status":"ok"}

// Ready check (model loaded?)
GET /ready
// Response: {"ready":true}

// Get available conditions
GET /conditions
// Response: {"conditions": {...}}

// Predict gait analysis
POST /predict
// Body: FormData with video + clinical_condition
// Response: {"predicted_class": "Normal", "probabilities": {...}}
```

---

## 📋 Render Deployment Checklist

Before deploying to Render:

- [ ] Know your frontend URL
- [ ] Set `CORS_ORIGINS` in Render dashboard
- [ ] Test with `curl -X OPTIONS` command
- [ ] Test from frontend with `fetch()`
- [ ] Check browser console for errors
- [ ] Monitor API logs for CORS issues

---

## 💡 Quick Reference

```bash
# List current environment variables
env | grep -E 'CORS|PORT|MODEL|TIMEOUT'

# Set variable locally
export CORS_ORIGINS="https://myapp.com"

# Start API with custom CORS
CORS_ORIGINS=https://myapp.com uvicorn main:app --host 0.0.0.0 --port 8000

# Docker with environment
docker run -e CORS_ORIGINS=https://myapp.com -p 8000:8000 gaitlab:latest
```

---

## 🎯 Summary

Your API is **already configured** to communicate with:
- Local frontends (localhost:3000, localhost:5173)
- Your own frontend (set `CORS_ORIGINS` env var)
- Production deployments (set `CORS_ORIGINS` to your domain)

**Just set one environment variable: `CORS_ORIGINS`**

That's it! Your frontend and API will communicate seamlessly.

