#!/usr/bin/env bash
set -euo pipefail

# Download model artifact at startup if MODEL_URL is provided.
# Usage: set MODEL_URL to an http/https presigned URL or direct link to the model file.

MODEL_PATH_DEFAULT="/app/models/gait_predict_model_v_1.pth"
MODEL_PATH_ENV="${MODEL_PATH:-$MODEL_PATH_DEFAULT}"

if [ -z "${MODEL_URL:-}" ]; then
  echo "MODEL_URL not set. Skipping model download. Expecting model at ${MODEL_PATH_ENV}"
  if [ ! -f "${MODEL_PATH_ENV}" ]; then
    echo "Warning: model file not found at ${MODEL_PATH_ENV}. Inference will fail until model is available."
  fi
  exit 0
fi

echo "MODEL_URL is set. Will download model to ${MODEL_PATH_ENV}"
mkdir -p "$(dirname "${MODEL_PATH_ENV}")"

if [ -f "${MODEL_PATH_ENV}" ]; then
  echo "Model file already exists at ${MODEL_PATH_ENV}, skipping download."
  exit 0
fi

echo "Downloading model from ${MODEL_URL} ..."
curl -fSL "${MODEL_URL}" -o "${MODEL_PATH_ENV}"
echo "Model downloaded to ${MODEL_PATH_ENV}"

exit 0
