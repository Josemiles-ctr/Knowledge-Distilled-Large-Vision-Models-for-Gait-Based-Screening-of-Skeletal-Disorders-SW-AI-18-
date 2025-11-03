---
title: GaitLab - Clinical Gait Analysis
emoji: 🚶
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
license: mit
---

# 🚶 GaitLab: AI-Powered Clinical Gait Analysis

An AI-powered system for analyzing gait patterns from video to detect various clinical conditions including knee osteoarthritis, Parkinson's disease, and other mobility disorders.

## 🎯 Features

- **Video-based Analysis**: Upload gait videos for automated analysis
- **Multi-condition Detection**: Identifies 9 different gait patterns
- **Clinical Context**: Incorporates clinical descriptions for more accurate predictions
- **Real-time Inference**: Fast predictions using optimized deep learning model

## 🏥 Supported Conditions

1. **Normal Gait**: Symmetrical, balanced walking pattern
2. **Knee Osteoarthritis** (KOA):
   - Early stage with mild gait modifications
   - Mild stage with asymmetric weight bearing
   - Severe stage with significant antalgic gait
3. **Parkinson's Disease** (PD):
   - Early stage with subtle gait changes
   - Mild stage with festinating gait
   - Severe stage with freezing of gait
4. **Disabled Gait**:
   - With assistive devices
   - Without assistive devices

## 🔬 Model Architecture

- **Type**: Knowledge-distilled 3D CNN with clinical text fusion
- **Input**: 8 video frames (224×224) + 384-dim clinical embedding
- **Output**: 9-class probability distribution
- **Parameters**: ~50M (student model)
- **Inference**: CPU/GPU optimized

## 📊 Performance

The model was trained using knowledge distillation from a larger vision-language model and achieves competitive accuracy on clinical gait datasets.

## 🚀 Usage

1. Upload a gait video (MP4 format recommended)
2. Provide a clinical description of the observed gait pattern
3. Click "Analyze Gait" to get predictions
4. Review the predicted condition and confidence scores

## 🛠️ Technical Details

### Model Components

- **Visual Encoder**: 3D CNN for spatiotemporal feature extraction
- **Clinical Embedder**: Hash-based text embedding (384-dim)
- **Fusion Network**: Concatenation + MLP classifier

### Video Processing

- Samples 8 frames uniformly from input video
- Resizes to 224×224 pixels
- Applies ImageNet normalization
- Processes in chunks for memory efficiency

## 📝 Citation

If you use this work, please cite:

```bibtex
@misc{gaitlab2024,
  title={Knowledge-Distilled Large Vision Models for Gait-Based Screening of Skeletal Disorders},
  author={Joseph Otai},
  year={2024},
  publisher={Hugging Face},
  url={https://huggingface.co/spaces/YOUR_USERNAME/gaitlab}
}
```

## 📄 License

MIT License

## 🤝 Acknowledgments

Built using:
- PyTorch for deep learning
- Gradio for the web interface
- Hugging Face Spaces for deployment

---

## Local Development

If you want to run this locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Gradio app
python app.py
```

The app will be available at `http://localhost:7860`
