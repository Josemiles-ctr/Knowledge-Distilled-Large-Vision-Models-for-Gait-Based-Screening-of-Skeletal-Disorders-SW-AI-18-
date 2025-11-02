from typing import Dict, Optional
from fastapi import APIRouter, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
import os
import logging
import gc

# Lazy imports: defer heavy dependencies (torch, transformers) until actually needed
try:
    import torch
    _TORCH_AVAILABLE = True
except ImportError:
    torch = None
    _TORCH_AVAILABLE = False

from utils.video_utils import process_video
from utils.clinical_utils import ClinicalEmbedder
from models.load_model import load_student_model
from app.config import DEVICE, NUM_FRAMES, FRAME_SIZE, CHUNK_SIZE
from models.class_mapping import class_mapping, clinical_descriptions

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize model and embedder (set MODEL_READY flag)
# Deferred to first-use pattern: don't initialize at import time to allow
# the module to be imported during build-time checks without expensive model loads.
MODEL_READY = False
embedder = None
model = None

def _ensure_model_loaded():
    """Lazy-load model and embedder on first use."""
    global MODEL_READY, embedder, model
    if MODEL_READY or (embedder is not None and model is not None):
        return
    try:
        logger.info("Initializing embedder...")
        embedder = ClinicalEmbedder()
        logger.info("Embedder initialized. Loading model...")
        model = load_student_model(num_classes=len(class_mapping))
        logger.info("Model loaded successfully")
        MODEL_READY = True
        logger.info("Model and embedder initialized successfully")
    except Exception as e:
        MODEL_READY = False
        logger.error(f"Error initializing model: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Model initialization failed: {str(e)}")

@router.post("/predict", response_model=Dict[str, Optional[Dict[str, float] | str]])
async def predict(video: UploadFile, clinical_condition: str = Form(...)):
    """
    Endpoint for gait analysis prediction.
    Args:
        video: Uploaded video file
        clinical_condition: Clinical condition for analysis
    Returns:
        Dictionary containing prediction results and probabilities
    """
    try:
        # Ensure model is loaded on first use
        _ensure_model_loaded()
        
        # Ensure model is ready
        if not MODEL_READY:
            raise HTTPException(status_code=503, detail="Model not ready")
        # Validate video file
        if not video.filename or not video.content_type:
            raise HTTPException(status_code=400, detail="Invalid video file")
        
        # Accept common video content-types, but also tolerate application/octet-stream
        content_type = (video.content_type or '').lower()
        filename = (video.filename or '').lower()
        is_video = (
            content_type.startswith('video/') or
            content_type == 'application/octet-stream' or
            filename.endswith(('.mp4', '.mov', '.avi', '.mkv', '.webm'))
        )
        if not is_video:
            raise HTTPException(status_code=400, detail="File must be a video")

        # Validate clinical condition text
        if not clinical_condition.strip():
            raise HTTPException(status_code=400, detail="Clinical description cannot be empty")

        # Create temp directory if it doesn't exist
        os.makedirs("/tmp", exist_ok=True)

        # Save uploaded video temporarily with a unique name
        video_path = f"/tmp/{hash(video.filename)}_{video.filename}"
        try:
            contents = await video.read()
            with open(video_path, "wb") as f:
                f.write(contents)
        except Exception as e:
            logger.error(f"Error saving video: {str(e)}")
            raise HTTPException(status_code=500, detail="Error processing video upload")

        try:
            logger.info("Processing video...")
            # Preprocess video with chunked processing for memory efficiency
            video_tensor = process_video(
                video_path, 
                num_frames=NUM_FRAMES, 
                frame_size=FRAME_SIZE,
                chunk_size=CHUNK_SIZE
            ).to(DEVICE)
            logger.info(f"Video tensor shape: {video_tensor.shape}")

            logger.info("Generating clinical embedding...")
            # Get clinical embedding from user's description
            clinical_embed = embedder.get_embedding(clinical_condition).to(DEVICE)
            logger.info(f"Clinical embedding shape: {clinical_embed.shape}")

            logger.info("Running inference...")
            # Run inference
            with torch.no_grad():
                logits = model(video_tensor, clinical_embed)
                probs = torch.softmax(logits, dim=1)
                pred_idx = torch.argmax(probs, dim=1).item()
                pred_class = list(class_mapping.keys())[pred_idx]
            
            logger.info(f"Prediction: {pred_class}")

            # Prepare response
            response = {
                "predicted_class": pred_class,
                "probabilities": {
                    k: float(probs[0, v]) for k, v in class_mapping.items()
                }
            }
            
            # Aggressive memory cleanup
            del video_tensor, clinical_embed, logits, probs
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
            # Clean up temp file
            if os.path.exists(video_path):
                os.remove(video_path)
            
            return response

        except MemoryError as e:
            logger.error(f"Memory error during inference: {str(e)}", exc_info=True)
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            raise HTTPException(status_code=500, detail="Insufficient memory for prediction")
        except Exception as e:
            logger.error(f"Error during inference: {str(e)}", exc_info=True)
            # Cleanup on error
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        # Ensure temp file is cleaned up
        if 'video_path' in locals() and os.path.exists(video_path):
            os.remove(video_path)

@router.get("/conditions")
async def get_conditions():
    """Get available clinical conditions and their descriptions."""
    return JSONResponse({
        "conditions": clinical_descriptions
    })


@router.get("/test-model-load")
async def test_model_load():
    """Test endpoint: attempt to load model and return status."""
    try:
        logger.info("Test: Attempting to load model...")
        _ensure_model_loaded()
        logger.info("Test: Model loaded successfully")
        return JSONResponse({"status": "model loaded", "ready": MODEL_READY})
    except Exception as e:
        logger.error(f"Test: Model load failed: {str(e)}", exc_info=True)
        return JSONResponse(
            {"status": "model load failed", "error": str(e)},
            status_code=500
        )


@router.get("/health")
async def health_check():
    """Simple health check to indicate app is running."""
    return JSONResponse({"status": "ok"})


@router.get("/ready")
async def readiness_check():
    """Readiness probe: returns 200 when model is loaded, 503 otherwise."""
    if MODEL_READY:
        return JSONResponse({"ready": True})
    else:
        return JSONResponse({"ready": False, "reason": "model not loaded"}, status_code=503)