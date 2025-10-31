#!/usr/bin/env bash
set -euo pipefail

# Tag and push a locally-built image. Designed for use with podman (or docker shim).
# Usage examples:
#   IMAGE_ID=af4fd921e927 DOCKER_REPO=yourdockerhubuser/gaitlab TAG=latest ./scripts/tag_and_push_image.sh --push
#   DOCKER_REPO=yourdockerhubuser/gaitlab TAG=latest ./scripts/tag_and_push_image.sh --interactive

IMAGE_ID="${IMAGE_ID:-}"   # optional: docker image id to tag (if not provided script will try to find a dangling image)
DOCKER_REPO="${DOCKER_REPO:-}" # required (e.g. mydockerhubuser/gaitlab)
TAG="${TAG:-latest}"

PUSH=false
if [ "${1:-}" = "--push" ]; then
  PUSH=true
fi

if [ "$DOCKER_REPO" = "" ]; then
  echo "ERROR: DOCKER_REPO must be set (e.g. yourdockerhubuser/gaitlab)" >&2
  exit 2
fi

if [ -z "$IMAGE_ID" ]; then
  # try to find the recent <none> image if exists
  IMAGE_ID=$(docker images --format '{{.ID}} {{.Repository}}:{{.Tag}}' | awk '/^/ {print $1}' | head -n 1)
fi

if [ -z "$IMAGE_ID" ]; then
  echo "ERROR: could not determine an image id. Run 'docker images' (or 'podman images') and set IMAGE_ID env var." >&2
  docker images
  exit 2
fi

IMAGE_TAG="$DOCKER_REPO:$TAG"
echo "Tagging image $IMAGE_ID -> $IMAGE_TAG"
docker tag "$IMAGE_ID" "$IMAGE_TAG"

if [ "$PUSH" = true ]; then
  echo "Logging in to registry (interactive)..."
  docker login
  echo "Pushing $IMAGE_TAG..."
  docker push "$IMAGE_TAG"
  echo "Pushed $IMAGE_TAG"
else
  echo "Tagged locally as $IMAGE_TAG (not pushed). To push, rerun with --push after 'docker login'."
fi

echo "Done."
