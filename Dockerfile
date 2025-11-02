# Production Dockerfile - Simplified for Render
# Uses Python 3.11-slim base and installs dependencies directly
# Base: Python 3.11-slim (~129 MB)

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    MODEL_PATH=/app/models/gait_predict_model_v_1.pth

# Install system dependencies AND build tools (pip needs them for wheels)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip first
RUN pip install --upgrade pip setuptools wheel

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies directly (not in venv, which can cause PATH issues)
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

# Make startup script executable
RUN chmod +x /app/scripts/download_model.sh

# Expose port
EXPOSE 8000

# Health check - Render will use this
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=5)" || exit 1

# Startup command - download model (if needed) then run uvicorn
CMD ["/bin/bash", "-lc", "/app/scripts/download_model.sh && exec uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
