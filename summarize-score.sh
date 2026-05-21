#!/bin/bash
cd "$(dirname "$0")"
if [ ! -f ".venv/bin/activate" ]; then
  echo ""
  echo "Virtual environment not found."
  echo "Run the installer for your system once (see install/README.md)."
  echo ""
  read -r -p "Press Enter to close..."
  exit 1
fi
# shellcheck disable=SC1091
source ".venv/bin/activate"
python -m registral_dispersion summarize "$@"
