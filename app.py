"""
Gradio App for GaitLab - Clinical Gait Analysis
Deployed on Hugging Face Spaces
"""
import gradio as gr
import torch
import tempfile
import os
from pathlib import Path

from utils.video_utils import process_video
from utils.clinical_utils import ClinicalEmbedder
from models.load_model import load_student_model
from models.class_mapping import class_mapping, clinical_descriptions

# Configuration
NUM_FRAMES = 8
FRAME_SIZE = 224
CHUNK_SIZE = 2
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
MODEL_PATH = 'models/gait_predict_model_v_1.pth'

print(f"Loading model on device: {DEVICE}")

# Initialize model and embedder
embedder = ClinicalEmbedder()
model = load_student_model(num_classes=len(class_mapping))
model.to(DEVICE)
model.eval()

print("✓ Model and embedder loaded successfully")


def predict_gait(video_file, clinical_condition):
    """
    Predict gait condition from video and clinical description.
    
    Args:
        video_file: Uploaded video file
        clinical_condition: Clinical condition description
    
    Returns:
        Prediction results as formatted text
    """
    if video_file is None:
        return "❌ Please upload a video file"
    
    if not clinical_condition or not clinical_condition.strip():
        return "❌ Please provide a clinical condition description"
    
    try:
        # Save uploaded file to temp location
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
            tmp.write(video_file)
            video_path = tmp.name
        
        # Process video
        video_tensor = process_video(
            video_path,
            num_frames=NUM_FRAMES,
            frame_size=FRAME_SIZE,
            chunk_size=CHUNK_SIZE
        ).to(DEVICE)
        
        # Get clinical embedding
        clinical_embed = embedder.get_embedding(clinical_condition).to(DEVICE)
        
        # Run inference
        with torch.no_grad():
            logits = model(video_tensor, clinical_embed)
            probs = torch.softmax(logits, dim=1)
            pred_idx = torch.argmax(probs, dim=1).item()
            pred_class = list(class_mapping.keys())[pred_idx]
        
        # Format results
        result = f"## 🎯 Prediction: **{pred_class}**\n\n"
        result += f"### Description:\n{clinical_descriptions.get(pred_class, 'N/A')}\n\n"
        result += "### Class Probabilities:\n\n"
        
        # Sort probabilities
        prob_dict = {k: float(probs[0, v]) for k, v in class_mapping.items()}
        sorted_probs = sorted(prob_dict.items(), key=lambda x: x[1], reverse=True)
        
        for class_name, prob in sorted_probs:
            bar = "█" * int(prob * 50)
            result += f"**{class_name}**: {prob:.2%} {bar}\n\n"
        
        # Cleanup
        os.unlink(video_path)
        del video_tensor, clinical_embed, logits, probs
        torch.cuda.empty_cache() if torch.cuda.is_available() else None
        
        return result
    
    except Exception as e:
        return f"❌ Error during prediction: {str(e)}"


# Create Gradio interface
with gr.Blocks(title="GaitLab - Clinical Gait Analysis", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🚶 GaitLab: Clinical Gait Analysis
    
    Upload a gait video and provide a clinical description to get AI-powered gait analysis predictions.
    
    **Available Conditions:**
    - Normal gait
    - Knee Osteoarthritis (Early, Mild, Severe)
    - Parkinson's Disease (Early, Mild, Severe)
    - Disabled gait (with/without assistive devices)
    """)
    
    with gr.Row():
        with gr.Column():
            video_input = gr.Video(
                label="Upload Gait Video",
                sources=["upload"],
                format="mp4"
            )
            
            clinical_input = gr.Textbox(
                label="Clinical Condition Description",
                placeholder="e.g., Mild knee osteoarthritis with asymmetric gait pattern",
                lines=3
            )
            
            # Example conditions dropdown
            gr.Examples(
                examples=[
                    ["Mild knee osteoarthritis showing limping gait"],
                    ["Early Parkinson's disease with reduced arm swing"],
                    ["Normal symmetrical gait pattern"],
                    ["Severe knee pain with antalgic gait"],
                ],
                inputs=clinical_input,
                label="Example Descriptions"
            )
            
            predict_btn = gr.Button("🔍 Analyze Gait", variant="primary", size="lg")
        
        with gr.Column():
            output = gr.Markdown(label="Analysis Results")
    
    predict_btn.click(
        fn=predict_gait,
        inputs=[video_input, clinical_input],
        outputs=output
    )
    
    gr.Markdown("""
    ---
    ### 📊 About
    
    This app uses a knowledge-distilled deep learning model to analyze gait patterns from video.
    The model was trained on clinical gait data and can identify various gait abnormalities.
    
    **Model Details:**
    - Architecture: Clinical-Enhanced Student Model (3D CNN)
    - Input: Video frames + clinical text embedding
    - Output: 9 gait condition classes with confidence scores
    """)

# Launch
if __name__ == "__main__":
    demo.launch()
