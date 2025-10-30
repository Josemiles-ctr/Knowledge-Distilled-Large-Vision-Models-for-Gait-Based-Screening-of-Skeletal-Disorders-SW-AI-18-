# Minimal Dockerfile for deploying the FastAPI app on Render (CPU)
# Uses Python 3.11 slim and installs system deps required by some ML packages

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system packages needed for some Python wheels (ffmpeg, build tools, libs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    git \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements
COPY requirements.txt /app/requirements.txt

# Install pip, wheel, setuptools then requirements
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools wheel
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application code
COPY . /app

# Set env defaults (can be overridden in Render dashboard)
ENV PORT=8000
ENV MODEL_PATH=/app/models/gait_predict_model_v_1.pth

# Make the startup script executable
RUN chmod +x /app/scripts/download_model.sh

EXPOSE 8000

# Run model download script before starting uvicorn
CMD ["/bin/bash", "-lc", "/app/scripts/download_model.sh && uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
