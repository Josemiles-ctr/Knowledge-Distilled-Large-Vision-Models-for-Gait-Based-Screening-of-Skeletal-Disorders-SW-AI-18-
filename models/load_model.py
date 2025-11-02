import logging

# Defensive torch import
try:
    import torch
    _TORCH_AVAILABLE = True
except ImportError:
    torch = None
    _TORCH_AVAILABLE = False

from .student_model import ClinicalEnhancedStudent
from app.config import MODEL_PATH, DEVICE, DISABLE_GPU

logger = logging.getLogger(__name__)

def load_student_model(num_classes):
    """Load student model for inference only (CPU, no gradients)."""
    if not _TORCH_AVAILABLE:
        raise RuntimeError("PyTorch is required")
    
    device = 'cpu'  # Always CPU for low memory
    
    try:
        model = ClinicalEnhancedStudent(num_classes=num_classes)
        
        # Load weights
        state_dict = torch.load(MODEL_PATH, map_location='cpu', weights_only=False)
        model.load_state_dict(state_dict)
        model.to(device)
        model.eval()
        
        # Disable gradients entirely for inference
        for param in model.parameters():
            param.requires_grad = False
        
        logger.info(f"Model loaded on {device} (inference mode)")
        return model
    except Exception as e:
        logger.error(f"Failed to load model: {e}", exc_info=True)
        raise
