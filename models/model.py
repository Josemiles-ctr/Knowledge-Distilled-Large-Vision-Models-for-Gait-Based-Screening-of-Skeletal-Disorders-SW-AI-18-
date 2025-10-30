import torch
import numpy as np
import cv2
from decord import VideoReader, cpu
import torch.nn.functional as F
from typing import Optional, Callable, Dict

class GaitLabModel:
    def __init__(self,
                 model_path: str = "gait_analysis_model_v_1.pth",
                 model_class: Optional[Callable] = None,
                 class_mapping: Optional[Dict[str, int]] = None,
                 device: Optional[str] = None):
        self.model_path = model_path
        self.model_class = model_class
        self.class_mapping = class_mapping or {}
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu") if device is None else torch.device(device)
        self.model = None

    def __call__(self, video_tensor, clinical_embed):
        if self.model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        return self.model(video_tensor, clinical_embed)

    def load_model(self):
        if self.model_class is None:
            from models.student_model import ClinicalEnhancedStudent
            self.model_class = ClinicalEnhancedStudent

        num_classes = len(self.class_mapping)
        self.model = self.model_class(num_classes=num_classes)
        self.model.to(self.device)
        
        state = torch.load(self.model_path, map_location=self.device)
        if isinstance(state, dict) and "state_dict" in state:
            state = state["state_dict"]
            
        # Strip "module." prefix if present (from DataParallel)
        if isinstance(state, dict):
            state = {k.replace("module.", ""): v for k, v in state.items()}
            
        self.model.load_state_dict(state)
        self.model.eval()
        return self