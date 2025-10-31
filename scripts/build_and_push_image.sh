#!/usr/bin/env bash
set -euo pipefail

# Build and optionally push a Docker image with the model baked into the image.
# Usage:
#   MODEL_LOCAL_PATH=./models/gait_predict_model_v_1.pth \
#   DOCKER_REPO=myuser/gaitlab \
#   TAG=latest \
#   ./scripts/build_and_push_image.sh --push

MODEL_LOCAL_PATH_DEFAULT="./models/gait_predict_model_v_1.pth"
MODEL_LOCAL_PATH="${MODEL_LOCAL_PATH:-$MODEL_LOCAL_PATH_DEFAULT}"
DOCKER_REPO="${DOCKER_REPO:-}"   # e.g. mydockerhubuser/gaitlab
TAG="${TAG:-latest}"

show_help () {
  cat <<EOF
Usage: MODEL_LOCAL_PATH=./models/gait_predict_model_v_1.pth DOCKER_REPO=myuser/gaitlab TAG=latest $0 [--push]

Builds a Docker image using Dockerfile.baked. If --push is provided, the script will attempt to
push the image to the remote repository (docker login required).
EOF
}

if [[ "${1:-}" == "--help" ]]; then
  show_help
  exit 0
fi

PUSH=false
if [[ "${1:-}" == "--push" ]]; then
  PUSH=true
fi

if [ ! -f "$MODEL_LOCAL_PATH" ]; then
  echo "Model file not found at $MODEL_LOCAL_PATH"
  echo "Place the model at this path before building, or set MODEL_LOCAL_PATH to your model file." >&2
  exit 2
fi

if [ -z "$DOCKER_REPO" ]; then
  echo "Please set DOCKER_REPO environment variable (e.g. myuser/gaitlab)" >&2
  show_help
  exit 2
fi

echo "Copying model into build context (./models) if not present..."
mkdir -p ./models
cp -n "$MODEL_LOCAL_PATH" ./models/

IMAGE_TAG="$DOCKER_REPO:$TAG"
echo "Building Docker image $IMAGE_TAG using Dockerfile.baked..."
docker build -f Dockerfile.baked -t "$IMAGE_TAG" .

if [ "$PUSH" = true ]; then
  echo "Pushing $IMAGE_TAG to remote registry..."
  docker push "$IMAGE_TAG"
  echo "Image pushed: $IMAGE_TAG"
else
  echo "Built image: $IMAGE_TAG (not pushed). To push, rerun with --push and ensure 'docker login' has been run." 
fi

echo "Done."
