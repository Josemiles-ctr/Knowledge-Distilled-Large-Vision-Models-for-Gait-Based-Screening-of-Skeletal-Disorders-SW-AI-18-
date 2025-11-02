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
    """
    Load student model with memory optimization.
    Keeps model on CPU by default unless GPU is explicitly enabled.
    
    Args:
        num_classes: Number of output classes
    
    Returns:
        Model in eval mode on appropriate device
    """
    # Use CPU if DISABLE_GPU is set (default: true for memory efficiency)
    device = 'cpu' if DISABLE_GPU else DEVICE
    
    model = ClinicalEnhancedStudent(num_classes=num_classes)
    
    # Load with map_location to control memory placement
    state_dict = torch.load(MODEL_PATH, map_location='cpu')
    model.load_state_dict(state_dict)
    model.to(device)
    model.eval()
    
    logger.info(f"Model loaded on {device} (GPU disabled: {DISABLE_GPU})")
    
    # Enable gradient checkpointing if available to save memory during inference
    if hasattr(model, 'enable_gradient_checkpointing'):
        try:
            model.enable_gradient_checkpointing()
            logger.info("Gradient checkpointing enabled")
        except Exception as e:
            logger.warning(f"Could not enable gradient checkpointing: {e}")
    
    return model
