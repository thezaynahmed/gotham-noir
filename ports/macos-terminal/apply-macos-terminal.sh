#!/usr/bin/env bash
set -euo pipefail
NO_OPEN=0
if [[ "${1:-}" == "--no-open" ]]; then
  NO_OPEN=1
  shift
fi
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
PROFILE_NAME="${1:-Gotham Noir - Year One}"
case "$PROFILE_NAME" in
  year-one) PROFILE_NAME="Gotham Noir - Year One" ;;
  batcomputer) PROFILE_NAME="Gotham Noir - Batcomputer" ;;
  arkham|arkham-slate) PROFILE_NAME="Gotham Noir - Arkham Slate" ;;
  vengeance) PROFILE_NAME="Gotham Noir - Vengeance" ;;
esac
THEME_FILE="${SCRIPT_DIR}/${PROFILE_NAME}.terminal"
TMP_DIR=""
cleanup() {
  if [[ -n "$TMP_DIR" && -d "$TMP_DIR" ]]; then rm -rf "$TMP_DIR"; fi
}
trap cleanup EXIT
if [[ ! -f "$THEME_FILE" ]]; then
  TMP_DIR="$(mktemp -d)"
  ENCODED_FILE="${PROFILE_NAME// /%20}.terminal"
  THEME_FILE="${TMP_DIR}/${PROFILE_NAME}.terminal"
  curl -fsSL "https://raw.githubusercontent.com/thezaynahmed/gotham-noir/main/ports/macos-terminal/${ENCODED_FILE}" -o "$THEME_FILE"
fi
if [[ "$NO_OPEN" -eq 0 && -z "${GOTHAM_NO_OPEN:-}" ]]; then
  open "$THEME_FILE"
  sleep 1
fi
defaults write com.apple.Terminal "Default Window Settings" -string "$PROFILE_NAME"
defaults write com.apple.Terminal "Startup Window Settings" -string "$PROFILE_NAME"
echo "✓ macOS Terminal.app configured with '$PROFILE_NAME'"
