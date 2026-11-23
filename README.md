<p align="center">
  <img src="./packages/vscode/images/palette-preview.png" width="100%" alt="Gotham Noir 4 dark-only nocturnal variants specimen">
</p>

# Gotham Noir

[![Validate Gotham Noir](https://github.com/thezaynahmed/gotham-noir/actions/workflows/validate.yml/badge.svg)](https://github.com/thezaynahmed/gotham-noir/actions/workflows/validate.yml)
[![MIT License](https://img.shields.io/badge/license-MIT-15171A?style=flat-square&labelColor=101215&color=F0C946)](LICENSE)
[![4 Dark Variants](https://img.shields.io/badge/variants-4_dark_only-15171A?style=flat-square&labelColor=101215&color=63C794)](#the-4-dark-variants)
[![15+ Targets](https://img.shields.io/badge/targets-15%2B_editors_%26_terminals-15171A?style=flat-square&labelColor=101215&color=74AEEB)](#supported-targets)

Dark themes that won't fry your eyes at 3 AM, bury functions in muddy navy, or break `git diff`. Built for developers, AI coding agents, MLOps, and DevOps engineers: **Gotham Noir** compiles 4 dark-only variants from one canonical palette source with OKLCH perceptual balance and APCA contrast across **15+ editors and terminals**.

<details>
  <summary>Table of Contents</summary>

- [Why Gotham Noir](#why-gotham-noir)
- [Quick Start](#quick-start)
- [The 4 Dark Variants](#the-4-dark-variants)
- [Color Architecture and Fonts](#color-architecture-and-fonts)
- [Supported Targets](#supported-targets)
- [Build and Contribute](#build-and-contribute)

</details>

---

## Why Gotham Noir

Classic nocturnal dark themes looked great in screenshots, then broke down during real engineering work: `#000000`/`#FFFFFF` halation fatigued eyes, `2.8:1` navy functions disappeared on dark gray, and yellow-on-yellow ANSI schemes turned `git diff` and Kubernetes logs into guesswork.

I engineered **Gotham Noir** from color science first: anti-halation matte canvases, equalized OKLCH syntax lightness, and an automated WCAG 2.1 + APCA contrast gate in CI. Each palette translates raw optical clarity into classic 1930s-to-modern detective noir atmosphere: matte Kevlar charcoal, rooftop signal gold, sub-level mainframe emerald, and rain-slicked crimson flare.

| Pain Point in Legacy Dark Themes | Gotham Noir Engineering Fix |
| :--- | :--- |
| `#000000` / `#FFFFFF` screen halation and eye shimmer | Softened charcoal canvases (`#101215` to `#1D1F21`) paired with warm parchment (`#D8D6CF` to `#DCE0E5`) |
| Functions and types buried at `< 3:1` contrast | `11.28:1` to `14.15:1` primary WCAG contrast (`Lc 79.2` to `87.0` APCA) across every variant |
| Muddy ANSI red/green collisions in `git diff` | >= 110 degree circular hue separation between crimson alerts and emerald additions |

---

## Quick Start

Sync every supported terminal and editor in one command via companion repo [`thezaynahmed/ghostty-config`](https://github.com/thezaynahmed/ghostty-config), or install your target directly:

**One-line universal setup (macOS & Linux):**

`curl -fsSL https://raw.githubusercontent.com/thezaynahmed/ghostty-config/main/install.sh | bash -s -- --all`

```bash
# Switch all synced terminals and IDEs at once:
theme-sync year-one --all
```

**Install with an AI Agent:** Paste this into Claude Code, Cursor, Antigravity, Codex, Windsurf, or Superset:

```text
Clone https://github.com/thezaynahmed/gotham-noir.git, read AGENTS.md, build and install the VS Code/Cursor/Zed themes, and verify all contrast gates with python3 -m unittest discover -s tests -v.
```

<details>
  <summary>Manual install for VS Code, Cursor, Windsurf, Antigravity IDE, and Zed</summary>

```bash
git clone https://github.com/thezaynahmed/gotham-noir.git
cd gotham-noir/packages/vscode
npx --yes @vscode/vsce package -o gotham-noir-1.0.0.vsix
code --install-extension gotham-noir-1.0.0.vsix        # or: cursor / windsurf / antigravity-ide

# Zed:
mkdir -p ~/.config/zed/themes
cp ../zed/themes/gotham-noir.json ~/.config/zed/themes/
```

</details>

---

## The 4 Dark Variants

| Variant | Background | Foreground | Accent | WCAG / APCA Lc | Visual Character & Use Case |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`Gotham Noir - Year One`** *(Flagship)* | `#15171A` | `#D8D6CF` | `#F0C946` Signal Gold | `12.35:1` / `Lc 80.7` | Matte Kevlar charcoal + rooftop halogen gold for all-day engineering |
| **`Gotham Noir - Batcomputer`** | `#101215` | `#DCE0E5` | `#F5D042` + `#56CCA0` | `14.15:1` / `Lc 87.0` | OLED obsidian control plane tuned for AI agents, K8s, and MLOps logs |
| **`Gotham Noir - Arkham Slate`** | `#1D1F21` | `#DAD5C7` | `#E6C15A` Antique Gold | `11.28:1` / `Lc 79.2` | Weathered warm slate + low-saturation gold for 3 AM zero-glare focus |
| **`Gotham Noir - Vengeance`** | `#151417` | `#DDD8D5` | `#E5535C` Flare Crimson | `12.98:1` / `Lc 82.7` | Rain-soaked dark chrome + tactical crimson for high-focus night sprints |

---

## Color Architecture and Fonts

Every variant maps code semantics consistently so ADHD context switching stays effortless across languages:

- **Nomex Kevlar (`#15171A`) & Parchment (`#D8D6CF`):** Zero-glare canvas and neutral identifiers.
- **Signal Gold (`#F0C946`):** Classes, types, interfaces, active cursor, and active line number.
- **Detective Blue (`#74AEEB`):** Functions, methods, HTML/JSX tags, and IaC resources.
- **Oracle Emerald (`#63C794`) & Alert Crimson (`#E86A74`):** Strings, `git diff` additions/deletions, and test telemetry.
- **Cryo Sonar Cyan (`#68C5CE`), Utility Brass (`#E29754`), Noir Violet (`#B695E8`):** Operators/YAML keys, constants/parameters, and control keywords.
- **2027 AI Agent & Diagnostic Tokens:** Native theming for `inlineChat`, `chat`, `agentsChatInput`, `editorGhostText`, `editorStickyScroll`, `editorInlayHint`, 6-level bracket pairs, and `terminalCommandDecoration`.

**Dyslexia & Readability Font Presets** in [`ports/ide-settings/font-presets.json`](ports/ide-settings/font-presets.json) and [`ports/linux-fontconfig/70-gotham-noir-fonts.conf`](ports/linux-fontconfig/70-gotham-noir-fonts.conf): **Monaspace Neon + Radon** (default Texture Healing), **Monaspace Argon**, **Intel One Mono**, **Atkinson Hyperlegible Mono**, and **Commit Mono**.

---

## Supported Targets

| Target | Location | Format |
| :--- | :--- | :--- |
| **VS Code / Cursor / Windsurf / Antigravity IDE** | [`packages/vscode/`](packages/vscode/) | Publishable `.vsix` extension (all 4 variants) |
| **Zed** | [`packages/zed/`](packages/zed/) | Official `v0.2.0` theme family JSON + `extension.toml` |
| **Regular Antigravity (Native Appearance)** | [`ports/antigravity-app/`](ports/antigravity-app/) | Native 3-color presets (`Background`, `Foreground`, `Accent`, `Contrast`) |
| **Ghostty** (macOS & Linux) | [`ports/ghostty/`](ports/ghostty/) | Native themes (`ghostty +validate-config` verified) |
| **Warp / Alacritty / WezTerm / Kitty** | [`ports/warp/`](ports/warp/), [`ports/alacritty/`](ports/alacritty/), [`ports/wezterm/`](ports/wezterm/), [`ports/kitty/`](ports/kitty/) | YAML, TOML, Lua, and metadata `.conf` ports |
| **iTerm2 / macOS Terminal.app / Windows Terminal** | [`ports/iterm2/`](ports/iterm2/), [`ports/macos-terminal/`](ports/macos-terminal/), [`ports/windows-terminal/`](ports/windows-terminal/) | `.itermcolors`, XML `.terminal` plists, JSON schemes |
| **tmux / Zsh / Fontconfig / Paradev** | [`ports/tmux/`](ports/tmux/), [`ports/zsh/`](ports/zsh/), [`ports/linux-fontconfig/`](ports/linux-fontconfig/), [`ports/paradev/`](ports/paradev/) | Split dimming, `LS_COLORS`, hinting rules, Paradev JSON |

---

## Build and Contribute

Regenerate every port from [`palettes/`](palettes/), run the contrast + E2E test suite, and build the `.vsix` locally:

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests -v
cd packages/vscode && npx --yes @vscode/vsce package -o gotham-noir-1.0.0.vsix
```

- Maintainer: [`@thezaynahmed`](https://github.com/thezaynahmed)
- Contributing & Publishing: See [`CONTRIBUTING.md`](CONTRIBUTING.md), [`PUBLISH.md`](PUBLISH.md), or open an issue on [GitHub Issues](https://github.com/thezaynahmed/gotham-noir/issues).
- Independent Project Notice: Gotham Noir is an independent, original open-source color system created by Zain Ahmed and is not affiliated with or endorsed by any studio or publisher.
- License: [MIT](LICENSE)
