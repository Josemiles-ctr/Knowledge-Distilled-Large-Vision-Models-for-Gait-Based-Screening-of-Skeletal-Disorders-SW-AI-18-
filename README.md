# GaitLab - Gait Analysis ML Model Server

A FastAPI-based REST API server for gait analysis using deep learning models to classify various gait conditions.

## Features

- **FastAPI REST API** for video-based gait analysis
- **Pre-trained PyTorch model** for gait condition classification
- **Docker containerization** for easy deployment
- **Automated CI/CD** via GitHub Actions to Docker Hub
- Supports gait conditions: Normal, Early/Mild/Severe KOA, Early/Mild/Severe PD, Disabled (assistive/non-assistive)

## Project Structure

```
GaitLab/
├── app/                    # FastAPI application
│   ├── config.py          # Configuration
│   └── main.py            # API routes and app setup
├── models/                # Model artifacts and utilities
│   ├── class_mapping.py   # Clinical descriptions and class indices
│   ├── model.py           # Model architecture
│   ├── student_model.py   # Student model (knowledge distillation)
│   ├── load_model.py      # Model loading utilities
│   └── gait_predict_model_v_1.pth  # Pre-trained model
├── scripts/               # Utility scripts
│   ├── download_model.sh  # Download model at container startup
│   ├── build_and_push_image.sh     # Build Docker image locally
│   ├── tag_and_push_image.sh       # Tag and push to registry
│   └── local_smoke_test.sh         # Local integration tests
├── utils/                 # Utility modules
│   ├── clinical_utils.py  # Clinical classification logic
│   └── video_utils.py     # Video processing utilities
├── main.py                # Root entry point for Render/direct runs
├── requirements.txt       # Python dependencies
├── Dockerfile             # Production Docker image definition
├── .github/workflows/     # CI/CD workflows
│   └── docker-publish.yml # Automated build and push to Docker Hub
└── README.md              # This file
```

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --host 0.0.0.0 --port 8000
```

### API Endpoints

- **`GET /health`** – Health check (returns 200 OK)
- **`GET /ready`** – Readiness check (model loaded; returns 200 OK)
- **`POST /predict`** – Predict gait condition from video
  - Form data: `video` (file), `clinical_condition` (string, optional)
  - Returns: JSON with predicted condition and confidence scores

### Example Prediction Request

```bash
curl -X POST http://localhost:8000/predict \
  -F "video=@sample_video.mp4" \
  -F "clinical_condition=normal"
```

## Docker Deployment

### Build Locally

```bash
docker build -t josemiles/gaitanalysis:latest .
```

### Run Locally

```bash
docker run -d -p 8000:8000 josemiles/gaitanalysis:latest
```

### Push to Docker Hub

Requires Docker Hub credentials and access token. First, log in:

```bash
echo "<DOCKER_HUB_TOKEN>" | docker login --username josemiles --password-stdin
```

Then push:

```bash
docker push josemiles/gaitanalysis:latest
```

## Automated CI/CD with GitHub Actions

The project includes a GitHub Actions workflow (`.github/workflows/docker-publish.yml`) that:
- Builds the Docker image on every push to `main`
- Pushes the image to Docker Hub as `docker.io/josemiles/gaitanalysis:latest`
- Tags images with both `latest` and the git commit SHA

### Setup

1. Add GitHub Secrets to your repository:
   - `DOCKERHUB_USERNAME` = your Docker Hub username
   - `DOCKERHUB_TOKEN` = your Docker Hub access token (create in Account Settings → Security)

2. Commit and push to `main` to trigger the workflow.

3. Monitor the build in the **Actions** tab of your GitHub repository.

## Deployment on Render

See [`DEPLOY_ON_RENDER.md`](DEPLOY_ON_RENDER.md) for step-by-step Render deployment instructions.

### Environment Variables

- `PORT` – Port to bind (default: 8000)
- `MODEL_PATH` – Path to model file (default: `/app/models/gait_predict_model_v_1.pth`)
- `MODEL_URL` – Optional: URL to download model at startup (if not baked in image)

## Testing

Run the smoke test locally (requires Docker):

```bash
IMAGE=josemiles/gaitanalysis:latest ./scripts/local_smoke_test.sh
```

This will:
- Start the container
- Test `/health` and `/ready` endpoints
- Send a test video to `/predict` and save the response

## Model Information

- **Model Type**: PyTorch CNN (ResNet-based)
- **Input**: Video file (MP4)
- **Output**: Gait condition classification with confidence scores
- **Classes**: Normal, KOA_Early, KOA_Mild, KOA_Severe, PD_Early, PD_Mild, PD_Severe, Disabled_Assistive, Disabled_NonAssistive

See `models/class_mapping.py` for clinical descriptions of each class.

## Requirements

- Python 3.11+
- PyTorch
- FastAPI
- OpenCV (cv2)
- FFmpeg

See `requirements.txt` for full list.

## License

[Add your license information here]

## Contributing

[Add contribution guidelines if applicable]

## Support

For issues or questions, please open an issue on the GitHub repository.
