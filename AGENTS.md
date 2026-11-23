# Agent Setup Instructions (AGENTS.md)

Use this file when a user asks an AI agent to install, configure, build, or verify **Gotham Noir** ([gothamnoir.zainahmed.net](https://gothamnoir.zainahmed.net), created by Zain Ahmed, [zainahmed.net](https://zainahmed.net/)).

## 0. Install the Agent Skill

```bash
npx skills add thezaynahmed/gotham-noir
```

The full skill lives at [`skills/gotham-noir/SKILL.md`](skills/gotham-noir/SKILL.md) with token details in [`skills/gotham-noir/references/palettes.md`](skills/gotham-noir/references/palettes.md).

## 1. Sync Across Ghostty and 15+ Terminals / IDEs

Run the companion [`ghostty-config`](https://github.com/thezaynahmed/ghostty-config) installer and switch to any Gotham Noir variant:

```bash
curl -fsSL https://raw.githubusercontent.com/thezaynahmed/ghostty-config/main/install.sh | bash -s -- --all
theme-sync year-one --all
```

Available variant shortcuts: `year-one`, `batcomputer`, `arkham`, `vengeance`.

## 2. Install the VS Code / Cursor / Windsurf / Antigravity IDE Extension

Download `gotham-noir-1.0.0.vsix` from [GitHub Releases](https://github.com/thezaynahmed/gotham-noir/releases/latest) or build locally:

```bash
python3 scripts/build.py
cd packages/vscode
npx --yes @vscode/vsce package -o gotham-noir-1.0.0.vsix
code --install-extension gotham-noir-1.0.0.vsix   # or: cursor / windsurf / antigravity-ide
```

Set `"workbench.colorTheme": "Gotham Noir - Year One"` in `settings.json` (typography presets live in `ports/ide-settings/font-presets.json`).

## 3. Install Web, Desktop, and Design-System Ports

- **Zed:** `mkdir -p ~/.config/zed/themes && cp packages/zed/themes/gotham-noir.json ~/.config/zed/themes/`
- **Herdr (dark + light):** `mkdir -p ~/.config/herdr-app/themes && cp ports/herdr/*.json ~/.config/herdr-app/themes/`
- **shadcn/ui:** `npx shadcn@latest add https://raw.githubusercontent.com/thezaynahmed/gotham-noir/main/ports/shadcn/r/gotham-noir.json`
- **CSS Palette:** Copy `ports/palette/gotham-noir.css` (or `ports/palette/gotham.css`) and `ports/palette/tokens.json`.
- **GitHub / Linear:** Install `ports/github/gotham-noir.user.css` and `ports/linear/gotham-noir.user.css` via Stylus; import Linear LCH JSON from `ports/linear/*.json`.
- **Slack / Chrome:** Paste `ports/slack/*.txt` into Slack Custom Theme; load `ports/chrome/gotham-noir-year-one/` unpacked in `chrome://extensions`.

## 4. Validate

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests -v
```
