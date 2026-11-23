#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROFILE_NAME="${1:-Gotham Noir - Year One}"
THEME_FILE="${SCRIPT_DIR}/${PROFILE_NAME}.terminal"
if [[ ! -f "$THEME_FILE" ]]; then
  echo "Theme file not found: $THEME_FILE" >&2; exit 1
fi
open "$THEME_FILE"
sleep 1
defaults write com.apple.Terminal "Default Window Settings" -string "$PROFILE_NAME"
defaults write com.apple.Terminal "Startup Window Settings" -string "$PROFILE_NAME"
echo "✓ macOS Terminal.app configured with '$PROFILE_NAME'"
