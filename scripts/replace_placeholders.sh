#!/usr/bin/env bash
set -euo pipefail

# Simple find-and-replace helper for repository placeholder tokens.
# Usage: ./scripts/replace_placeholders.sh PLACEHOLDER1=VALUE1 PLACEHOLDER2=VALUE2 ...
# Example: ./scripts/replace_placeholders.sh YOUR_DOCKER_REPO=ocio/gaitlab YOUR_SERVICE=gaitlab.onrender.com

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 KEY=VALUE [KEY=VALUE ...]" >&2
  exit 2
fi

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FILES=(DEPLOY_ON_RENDER.md scripts/build_and_push_image.sh scripts/download_model.sh)

for kv in "$@"; do
  KEY=${kv%%=*}
  VALUE=${kv#*=}
  echo "Replacing token '$KEY' with '$VALUE' in files..."
  for f in "${FILES[@]}"; do
    if [ -f "$REPO_ROOT/$f" ]; then
      # Use perl for in-place safe replacement
      perl -0777 -pe "s/\b${KEY}\b/${VALUE}/g" -i "$REPO_ROOT/$f"
    fi
  done
done

echo "Done. Review changes and commit if correct."
