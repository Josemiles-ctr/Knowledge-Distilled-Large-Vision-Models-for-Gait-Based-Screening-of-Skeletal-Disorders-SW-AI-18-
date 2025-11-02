# Production Dockerfile - CPU Optimized
# Ensures all imports and dependencies are present
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Install system dependencies (ffmpeg for video processing, libgl1 for OpenCV)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first (layer caching)
COPY requirements.txt .

# Install CPU-only PyTorch from official index (avoids CUDA/GPU wheels)
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir \
        --index-url https://download.pytorch.org/whl/cpu \
        torch==2.5.1 torchvision==0.20.1 && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app/

# Verify critical imports work
RUN python -c "from app.config import DEVICE, NUM_FRAMES, FRAME_SIZE, CHUNK_SIZE, MODEL_PATH, DISABLE_GPU; print('✓ All config exports loaded successfully')" && \
    python -c "from api.routes import router; print('✓ Router imported successfully')" && \
    python -c "from models.load_model import load_student_model; print('✓ Model loader imported successfully')"

EXPOSE 8000

# Health check - verify app is responding
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=5)" || exit 1

# Start application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
