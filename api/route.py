from fastapi import APIRouter, UploadFile, Form
from utils.video_utils import process_video
from utils.clinical_utils import ClinicalEmbedder
from model.load_model import load_student_model
from app.config import DEVICE, NUM_FRAMES, FRAME_SIZE
from model.class_mapping import class_mapping, clinical_descriptions

router = APIRouter()
embedder = ClinicalEmbedder()
model = load_student_model(num_classes=len(class_mapping))

@router.post("/predict")
async def predict(video: UploadFile, clinical_condition: str = Form(...)):
    # Validate clinical condition
    if clinical_condition not in clinical_descriptions:
        return {"error": f"Unknown clinical condition: {clinical_condition}"}

    # Save uploaded video temporarily
    video_path = f"/tmp/{video.filename}"
    with open(video_path, "wb") as f:
        f.write(await video.read())

    # Preprocess video
    video_tensor = process_video(video_path, num_frames=NUM_FRAMES, frame_size=FRAME_SIZE).to(DEVICE)

    # Get clinical embedding from description
    clinical_embed = embedder.get_embedding(clinical_descriptions[clinical_condition]).to(DEVICE)

    # Inference
    with torch.no_grad():
        logits = model(video_tensor, clinical_embed)
        probs = torch.softmax(logits, dim=1)
        pred_idx = torch.argmax(probs, dim=1).item()
        pred_class = list(class_mapping.keys())[pred_idx]

    return {
        "predicted_class": pred_class,
        "probabilities": {k: float(probs[0, v]) for k, v in class_mapping.items()}
    }
