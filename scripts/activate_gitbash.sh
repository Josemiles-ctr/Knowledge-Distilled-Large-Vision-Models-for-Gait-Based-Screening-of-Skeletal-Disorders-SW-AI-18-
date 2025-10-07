#!/usr/bin/env bash
# Helper: safely activate the Windows venv from Git Bash (MINGW64)
# Usage: source scripts/activate_gitbash.sh

# Path to the virtualenv root (relative to repo root)
VENV_DIR="./GaitEnv"
ACTIVATE_SCRIPT="$VENV_DIR/Scripts/activate"

if [ ! -f "$ACTIVATE_SCRIPT" ]; then
  echo "Activate script not found: $ACTIVATE_SCRIPT"
  return 1 2>/dev/null || exit 1
fi

# Ensure MSYS /usr/bin utilities (uname, cygpath, etc.) remain available
# Prepend /usr/bin if it exists and is not already in PATH
case ":$PATH:" in
  *:/usr/bin:*) ;;
  *)
    if [ -d "/usr/bin" ]; then
      export PATH="/usr/bin:$PATH"
    fi
    ;;
esac

# Source the venv activation (this will modify PATH to include the venv)
# Use a relative path to avoid Windows-style path conversion issues
source "$ACTIVATE_SCRIPT"

# Report back
if [ -n "$VIRTUAL_ENV" ]; then
  echo "Activated venv: $VIRTUAL_ENV"
  return 0 2>/dev/null || exit 0
else
  echo "Activation failed"
  return 1 2>/dev/null || exit 1
fi
