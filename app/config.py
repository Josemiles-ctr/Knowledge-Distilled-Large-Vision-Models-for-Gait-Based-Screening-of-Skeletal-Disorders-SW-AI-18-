import torch
import os

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../model/gait_predict_model_v_1.pth")
NUM_FRAMES = 16
FRAME_SIZE = 224
