from typing import Dict, Optional
from fastapi import APIRouter, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
import torch
import os
import logging
from utils.video_utils import process_video
from utils.clinical_utils import ClinicalEmbedder
from models.load_model import load_student_model
from app.config import DEVICE, NUM_FRAMES, FRAME_SIZE
from models.class_mapping import class_mapping, clinical_descriptions

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize model and embedder
try:
    embedder = ClinicalEmbedder()
    model = load_student_model(num_classes=len(class_mapping))
    logger.info("Model and embedder initialized successfully")
except Exception as e:
    logger.error(f"Error initializing model: {str(e)}")
    raise

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
        # Validate video file
        if not video.filename or not video.content_type:
            raise HTTPException(status_code=400, detail="Invalid video file")
        
        if not video.content_type.startswith('video/'):
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
            # Preprocess video
            video_tensor = process_video(
                video_path, 
                num_frames=NUM_FRAMES, 
                frame_size=FRAME_SIZE
            ).to(DEVICE)

            # Get clinical embedding from user's description
            clinical_embed = embedder.get_embedding(clinical_condition).to(DEVICE)

            # Run inference
            with torch.no_grad():
                logits = model(video_tensor, clinical_embed)
                probs = torch.softmax(logits, dim=1)
                pred_idx = torch.argmax(probs, dim=1).item()
                pred_class = list(class_mapping.keys())[pred_idx]

            # Clean up
            if os.path.exists(video_path):
                os.remove(video_path)

            # Prepare response
            return {
                "predicted_class": pred_class,
                "probabilities": {
                    k: float(probs[0, v]) for k, v in class_mapping.items()
                }
            }

        except Exception as e:
            logger.error(f"Error during inference: {str(e)}")
            raise HTTPException(status_code=500, detail="Error during analysis")

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