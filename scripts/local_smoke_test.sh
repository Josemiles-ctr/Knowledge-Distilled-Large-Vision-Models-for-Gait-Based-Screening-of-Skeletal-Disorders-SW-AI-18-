#!/usr/bin/env bash
set -euo pipefail

# Run the locally-built image and perform simple health/ready/predict smoke tests.
# Usage: IMAGE=gaitlab:local ./scripts/local_smoke_test.sh

IMAGE="${IMAGE:-gaitlab:local}"
PORT="${PORT:-8000}"

CONTAINER_NAME="gaitlab_smoketest_$$"

echo "Running container $IMAGE as $CONTAINER_NAME (port $PORT)..."
docker run --rm -d -p ${PORT}:8000 -e PORT=8000 --name "$CONTAINER_NAME" "$IMAGE"

trap 'echo "Stopping container..."; docker stop "$CONTAINER_NAME" >/dev/null 2>&1 || true' EXIT

echo "Waiting 3s for startup..."
sleep 3

echo "Health check:"
curl -i --max-time 5 http://127.0.0.1:${PORT}/health || true

echo "Ready check:"
curl -i --max-time 5 http://127.0.0.1:${PORT}/ready || true

if [ -f test_video.mp4 ]; then
  echo "Predict test (small file):"
  curl -X POST -s -o /tmp/predict_out.json -w "\nHTTP_STATUS:%{http_code}\n" \
    -F "video=@test_video.mp4;type=video/mp4" \
    -F "clinical_condition=smoke test" \
    http://127.0.0.1:${PORT}/predict || true
  echo "Predict response saved to /tmp/predict_out.json"
else
  echo "No test_video.mp4 found in repo root; skipping predict test." 
fi

echo "Smoke tests done. Container will be stopped now (trap)."
