# Gotham Noir

![Gotham Noir Variants](images/palette-preview.png)

Dark themes that won't fry your eyes at 3 AM, bury functions in muddy navy, or break `git diff`. **Gotham Noir** ships 4 anti-halation dark-only palettes tuned with OKLCH perceptual balance, WCAG 2.1 + APCA contrast verification, and full 2027 AI agent / MLOps / DevOps semantic tokens.

## Why Gotham Noir

Legacy nocturnal themes relied on `#000000`/`#FFFFFF` halation, low-contrast navy functions (`2.8:1`), and yellow-on-yellow ANSI palettes that obscured diffs. Gotham Noir starts from optical ergonomics first (`11.28:1` to `14.15:1` primary contrast, `>= 110 deg` red/green separation) and pairs it with classic 1930s-to-modern detective noir atmosphere.

## Quick Install

Install **Gotham Noir** from VS Code / Open VSX (`Cmd+K Cmd+T` on macOS, `Ctrl+K Ctrl+T` on Windows/Linux), or build and install locally:

```bash
git clone https://github.com/thezaynahmed/gotham-noir.git && cd gotham-noir/packages/vscode
npx --yes @vscode/vsce package -o gotham-noir-1.0.0.vsix
code --install-extension gotham-noir-1.0.0.vsix   # or: cursor / windsurf / antigravity-ide
```

## 4 Dark Variants

| Variant | Canvas | Foreground | Signature Accent | Character |
| :--- | :--- | :--- | :--- | :--- |
| **Gotham Noir - Year One** | `#15171A` | `#D8D6CF` | `#F0C946` Signal Gold | Matte Kevlar charcoal + rooftop halogen gold (`12.35:1` / `Lc 80.7`) |
| **Gotham Noir - Batcomputer** | `#101215` | `#DCE0E5` | `#F5D042` + `#56CCA0` | OLED obsidian control plane for AI agents, K8s & MLOps (`14.15:1` / `Lc 87.0`) |
| **Gotham Noir - Arkham Slate** | `#1D1F21` | `#DAD5C7` | `#E6C15A` Antique Gold | Weathered warm slate for 3 AM zero-glare focus (`11.28:1` / `Lc 79.2`) |
| **Gotham Noir - Vengeance** | `#151417` | `#DDD8D5` | `#E5535C` Flare Crimson | Rain-soaked dark chrome + tactical crimson flare (`12.98:1` / `Lc 82.7`) |

## Semantic Palette

| Role | Color Channel | Usage |
| :--- | :--- | :--- |
| **Nomex Kevlar** | Background Surface | Zero `#000000` / `#FFFFFF` halation canvas |
| **Parchment** | Primary Ink | Identifiers and primary output (`11:1` to `14:1` WCAG) |
| **Signal Gold** | Types & Cursor | Classes, interfaces, types, active cursor, active line number |
| **Detective Blue** | Functions | Methods, calls, HTML/JSX tags, and Terraform resources |
| **Oracle Emerald** | Strings & Diff + | String literals, `git diff` additions, passing test checks |
| **Cryo Sonar Cyan** | Operators & Keys | Operators, regex escapes, YAML/JSON keys, builtins |
| **Utility Brass** | Constants & Params | Numbers, booleans, enums, function parameters |
| **Noir Violet** | Control Flow | Keywords (`async`, `return`, `import`) and decorators |
| **Flare Crimson** | Errors & Diff - | Errors, `git diff` deletions, mismatched brackets |

```python
@telemetry_node(clearance="SUB-LEVEL-04")
class SignalControlPlane(OracleStream):
    """Forensic and MLOps inference node across nocturnal clusters."""
    def trace_signal(self, sector: str = "Dockside") -> dict[str, int]:
        nodes = {"arkham": 27, "narrows": 89, "iceberg": 2022}
        return {k: v for k, v in nodes.items() if sector != "Fault"}
```

## Recommended Editor Settings

```json
{
  "workbench.colorTheme": "Gotham Noir - Year One",
  "editor.fontFamily": "'Monaspace Neon', 'Intel One Mono', 'Atkinson Hyperlegible Mono', monospace",
  "editor.fontLigatures": "'calt', 'ss01', 'ss02', 'ss03', 'zero', 'cv10'",
  "editor.lineHeight": 1.5,
  "editor.bracketPairColorization.enabled": true,
  "editor.guides.bracketPairs": "active",
  "editor.stickyScroll.enabled": true,
  "editor.semanticHighlighting.enabled": true,
  "editor.cursorBlinking": "solid",
  "editor.renderWhitespace": "boundary"
}
```

### Dyslexia & Readability Font Alternatives
- **Monaspace Argon**: Wider humanist proportions with Texture Healing.
- **Intel One Mono**: Designed by Frere-Jones Type to separate `b/d/p/q` and `1/l/I`.
- **Atkinson Hyperlegible Mono**: Braille Institute's monospaced font for maximum homoglyph clarity.
- **Commit Mono**: Neutral engineering proportions with customizable alternates.

## Cross-Platform Ports & Contributing

Native ports for **Ghostty**, **Zed**, **Warp**, **Kitty**, **Alacritty**, **WezTerm**, **Windows Terminal**, **iTerm2**, **macOS Terminal.app**, **tmux**, **Paradev**, and **Regular Antigravity** live in [github.com/thezaynahmed/gotham-noir](https://github.com/thezaynahmed/gotham-noir). See [Contributing](https://github.com/thezaynahmed/gotham-noir/blob/main/CONTRIBUTING.md) or open bug reports on [GitHub Issues](https://github.com/thezaynahmed/gotham-noir/issues).

*Independent open-source color system created by Zain Ahmed. Not affiliated with or endorsed by any studio or publisher.*
