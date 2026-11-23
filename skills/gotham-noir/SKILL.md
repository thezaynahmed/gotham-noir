---
name: gotham-noir
description: Installs, configures, customizes, and builds the Gotham Noir anti-halation OKLCH + APCA dark theme ecosystem across 20+ editors, terminals, web apps, and shadcn/ui projects. Use when the user asks to install Gotham Noir, switch variants (Year One, Batcomputer, Arkham Slate, Vengeance), apply Gotham Noir CSS/shadcn tokens, port Gotham Noir to a new app, or verify palette contrast.
---

# Gotham Noir Theme Skill

Apply, install, or extend **Gotham Noir** (4 anti-halation OKLCH + APCA dark variants) from its live site (https://gothamnoir.zainahmed.net) and single-source-of-truth repository (`thezaynahmed/gotham-noir`).

## Variant Selection

Pick the variant matching the user's lighting and focus needs:

| Variant | Slug | Canvas / Text / Accent | Best For |
| :--- | :--- | :--- | :--- |
| **Gotham Noir - Year One** | `year-one` | `#15171A` / `#D8D6CF` / `#F0C946` | Balanced flagship for day and night coding |
| **Gotham Noir - Batcomputer** | `batcomputer` | `#101215` / `#DCE0E5` / `#F5D042` + `#56CCA0` | OLED obsidian control plane for AI agents, K8s, MLOps |
| **Gotham Noir - Arkham Slate** | `arkham-slate` | `#1D1F21` / `#DAD5C7` / `#E6C15A` | Warm weathered slate for 3 AM zero-glare and dyslexia focus |
| **Gotham Noir - Vengeance** | `vengeance` | `#151417` / `#DDD8D5` / `#E5535C` | Rain-soaked obsidian chrome with crimson flare |

## Installation Workflows

### 1. Universal Terminal & IDE Sync (macOS & Linux)

```bash
curl -fsSL https://raw.githubusercontent.com/thezaynahmed/ghostty-config/main/install.sh | bash -s -- --all
theme-sync year-one --all
```

### 2. VS Code, Cursor, Windsurf, Antigravity IDE

Download `gotham-noir-1.0.0.vsix` from GitHub Releases (`https://github.com/thezaynahmed/gotham-noir/releases/latest`) or build locally:

```bash
python3 scripts/build.py
cd packages/vscode && npx --yes @vscode/vsce package -o gotham-noir-1.0.0.vsix
code --install-extension gotham-noir-1.0.0.vsix   # or: cursor / windsurf / antigravity-ide
```

### 3. Zed, Neovim, JetBrains, Windows Terminal, macOS Terminal, Herdr, Chrome, GitHub, Linear, Slack

- **Zed:** `mkdir -p ~/.config/zed/themes && cp packages/zed/themes/gotham-noir.json ~/.config/zed/themes/`
- **Neovim:** Load `ports/neovim/` in `lazy.nvim` (`vim.cmd.colorscheme("gotham-noir-year-one")`).
- **JetBrains:** Import `.icls` from `ports/jetbrains/` under Color Scheme settings.
- **macOS Terminal.app:** `curl -fsSL https://raw.githubusercontent.com/thezaynahmed/gotham-noir/main/ports/macos-terminal/apply-macos-terminal.sh | bash -s -- "Gotham Noir - Year One"`
- **Windows Terminal + PowerShell:** `irm https://raw.githubusercontent.com/thezaynahmed/gotham-noir/main/ports/windows-terminal/install-windows-terminal.ps1 | iex` (+ `gotham-noir-psreadline.ps1` in `$PROFILE`).
- **Herdr (dark + light):** `mkdir -p ~/.config/herdr-app/themes && cp ports/herdr/*.json ~/.config/herdr-app/themes/`
- **Chrome (MV3):** Load `ports/chrome/gotham-noir-year-one/` via `chrome://extensions` -> Load unpacked.
- **GitHub / Linear:** Install `ports/github/gotham-noir.user.css` or `ports/linear/gotham-noir.user.css` in Stylus; import Linear LCH JSON from `ports/linear/*.json`.
- **Slack:** Paste any sidebar string from `ports/slack/*.txt` into Slack Preferences -> Themes -> Custom theme -> Import.

### 4. shadcn/ui & Web CSS Tokens

```bash
npx shadcn@latest add https://raw.githubusercontent.com/thezaynahmed/gotham-noir/main/ports/shadcn/r/gotham-noir.json
```

Or import `ports/palette/gotham-noir.css` (alias `ports/palette/gotham.css`) and set `data-gotham-theme="year-one|batcomputer|arkham-slate|vengeance"`.

## Extending or Auditing Palettes

1. Edit canonical JSON palettes in `palettes/` or generator scripts in `scripts/`.
2. Run `python3 scripts/build.py` (enforces WCAG 2.1 + APCA Lc + >= 110 deg R/G separation).
3. Run `python3 -m unittest discover -s tests -v`.
4. Never add `.svg` references inside `packages/vscode/package.json` or `packages/vscode/README.md`.

## Additional Resources

- Interactive preview & install deck: https://gothamnoir.zainahmed.net
- Complete token values and contrast metrics: [references/palettes.md](references/palettes.md)
