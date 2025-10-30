import torch
from .student_model import ClinicalEnhancedStudent
from app.config import MODEL_PATH, DEVICE

def load_student_model(num_classes):
    model = ClinicalEnhancedStudent(num_classes=num_classes)
    state_dict = torch.load(MODEL_PATH, map_location=DEVICE)
    model.to(DEVICE)
    model.eval()
    return model
