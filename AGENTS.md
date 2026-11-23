# Agent Setup Instructions (AGENTS.md)

Use this file when a user asks an AI agent to install, build, or verify **Gotham Noir**.

## 1. Sync Across Ghostty and 15+ Terminals / IDEs

Run the companion [`ghostty-config`](https://github.com/thezaynahmed/ghostty-config) installer and switch to any Gotham Noir variant:

```bash
curl -fsSL https://raw.githubusercontent.com/thezaynahmed/ghostty-config/main/install.sh | bash -s -- --all
theme-sync year-one --all
```

Available variant shortcuts: `year-one`, `batcomputer`, `arkham`, `vengeance`.

## 2. Build & Install the VS Code / Cursor / Windsurf / Antigravity IDE Extension

Package the local `.vsix` from the Single Source of Truth (SSOT) generator and install it into the user's editor CLI:

```bash
python3 scripts/build.py
cd packages/vscode
npx --yes @vscode/vsce package -o gotham-noir-1.0.0.vsix
code --install-extension gotham-noir-1.0.0.vsix
```

For Cursor, Windsurf, or Antigravity IDE, replace `code` with `cursor`, `windsurf`, or `antigravity-ide`. Then set `"workbench.colorTheme": "Gotham Noir - Year One"` in the editor's `settings.json` (recommended typography presets live in `ports/ide-settings/font-presets.json`).

## 3. Install in Zed

```bash
mkdir -p ~/.config/zed/themes
cp packages/zed/themes/gotham-noir.json ~/.config/zed/themes/
```

## 4. Validate

Run contrast verification (WCAG 2.1 + APCA Lc) and the full unit test suite:

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests -v
```
