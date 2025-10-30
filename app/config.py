import os
from pathlib import Path
import torch


class Settings:
    """Simple settings loader that reads environment variables directly.

    This avoids relying on pydantic_settings which can attempt to JSON-decode
    environment variables and fail when .env contains comma-separated lists.
    """

    # Server Configuration
    PORT: int = int(os.getenv('PORT', 8000))
    HOST: str = os.getenv('HOST', '0.0.0.0')
    WORKERS: int = int(os.getenv('WORKERS', 8))
    TIMEOUT: int = int(os.getenv('TIMEOUT', 300))

    # Model Configuration
    MODEL_PATH: str = os.getenv('MODEL_PATH', 'models/gait_predict_model_v_1.pth')
    NUM_FRAMES: int = int(os.getenv('NUM_FRAMES', 16))
    FRAME_SIZE: int = int(os.getenv('FRAME_SIZE', 224))
    DEVICE: str = 'cuda' if torch.cuda.is_available() else 'cpu'

    # CORS Configuration: accept comma separated values in .env
    CORS_ORIGINS = [s.strip() for s in os.getenv('CORS_ORIGINS', 'http://localhost:5173,http://localhost:3000').split(',') if s.strip()]
    CORS_METHODS = [s.strip() for s in os.getenv('CORS_METHODS', 'GET,POST,PUT,DELETE,OPTIONS').split(',') if s.strip()]
    CORS_HEADERS = [s.strip() for s in os.getenv('CORS_HEADERS', 'Content-Type,Authorization,Accept').split(',') if s.strip()]

    # Storage Configuration
    TEMP_UPLOAD_DIR: str = os.getenv('TEMP_UPLOAD_DIR', '/tmp')
    MAX_UPLOAD_SIZE: int = int(os.getenv('MAX_UPLOAD_SIZE', 104857600))  # 100MB


# Create global settings instance
settings = Settings()

# Ensure temp directory exists
os.makedirs(settings.TEMP_UPLOAD_DIR, exist_ok=True)

# Ensure model path is absolute
if not os.path.isabs(settings.MODEL_PATH):
    settings.MODEL_PATH = str(Path(__file__).parent.parent / settings.MODEL_PATH)

# Backwards-compatible top-level names used by other modules
MODEL_PATH = settings.MODEL_PATH
DEVICE = settings.DEVICE
NUM_FRAMES = settings.NUM_FRAMES
FRAME_SIZE = settings.FRAME_SIZE
CORS_ORIGINS = settings.CORS_ORIGINS
CORS_METHODS = settings.CORS_METHODS
CORS_HEADERS = settings.CORS_HEADERS
