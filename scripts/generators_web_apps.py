"""Generate web, browser, design-system, and desktop app ports from canonical palettes.

Covers: Herdr (dark + light), GitHub UserStyle, Linear (LCH JSON + UserStyle),
Slack sidebar strings, Chrome Manifest V3 themes, shadcn/ui (CSS + registry JSON),
Palette (gotham-noir.css, gotham.css, W3C tokens.json), and Fonts guide.
"""

from __future__ import annotations

import json
import math
import shutil
from pathlib import Path


def _hex_rgb(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _srgb_to_linear(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _hex_to_cie_lch(hex_color: str) -> list[float]:
    """Convert #RRGGBB to Linear's [L, C, H, 1] CIE LCH format."""
    r, g, b = (_srgb_to_linear(v / 255.0) for v in _hex_rgb(hex_color))
    # sRGB D65 -> CIE XYZ
    x = 0.4124564 * r + 0.3575761 * g + 0.1804375 * b
    y = 0.2126729 * r + 0.7151522 * g + 0.0721750 * b
    z = 0.0193339 * r + 0.1191920 * g + 0.9503041 * b
    # Normalize by D65 reference white
    xn, yn, zn = 0.95047, 1.00000, 1.08883

    def f(t: float) -> float:
        return t ** (1 / 3) if t > 0.008856 else (7.787 * t) + (16 / 116)

    fx, fy, fz = f(x / xn), f(y / yn), f(z / zn)
    L = 116.0 * fy - 16.0
    a = 500.0 * (fx - fy)
    b_val = 200.0 * (fy - fz)
    C = math.hypot(a, b_val)
    H = (math.degrees(math.atan2(b_val, a)) + 360.0) % 360.0
    return [round(L, 3), round(C, 3), round(H, 3), 1]


def _hex_to_oklch(hex_color: str) -> str:
    """Convert #RRGGBB to CSS oklch(L C H) string."""
    r, g, b = (_srgb_to_linear(v / 255.0) for v in _hex_rgb(hex_color))
    l_ = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m_ = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s_ = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l3, m3, s3 = l_ ** (1 / 3), m_ ** (1 / 3), s_ ** (1 / 3)
    L = 0.2104542553 * l3 + 0.7936177850 * m3 - 0.0040720468 * s3
    a = 1.9779984951 * l3 - 2.4285922050 * m3 + 0.4505937099 * s3
    b_val = 0.0259040371 * l3 + 0.7827717662 * m3 - 0.8086757660 * s3
    C = math.hypot(a, b_val)
    H = (math.degrees(math.atan2(b_val, a)) + 360.0) % 360.0
    return f"oklch({L:.4f} {C:.4f} {H:.2f})"


def _write_herdr(palettes: list[dict], root: Path) -> None:
    out_dir = root / "ports" / "herdr"
    out_dir.mkdir(parents=True, exist_ok=True)
    for pal in palettes:
        ui, syn, ansi = pal["ui"], pal["syntax"], pal["ansi"]
        doc = {
            "background": ui["bg"],
            "foreground": ui["fg"],
            "selection": ui["selectionBg"],
            "cursor": ui["cursorBg"],
            "ansi": [
                ansi["black"], ansi["red"], ansi["green"], ansi["yellow"],
                ansi["blue"], ansi["magenta"], ansi["cyan"], ansi["white"],
                ansi["brightBlack"], ansi["brightRed"], ansi["brightGreen"], ansi["brightYellow"],
                ansi["brightBlue"], ansi["brightMagenta"], ansi["brightCyan"], ansi["brightWhite"],
            ],
            "colors": {
                "canvas": ui["bgDeep"],
                "chrome": ui["bgSide"],
                "surface": ui["surface"],
                "popover": ui["elevated"],
                "raised": ui["surfaceHover"],
                "hover": ui["surfaceHover"],
                "selected": ui["selectionBg"],
                "border": ui["border"],
                "input": ui["borderActive"],
                "muted": ui["fgMuted"],
                "dim": ui["fgSubtle"],
                "accent": ui["accent"],
                "accent_foreground": ui["accentFg"],
                "solid": ui["buttonBg"],
                "solid_foreground": ui["buttonFg"],
                "working": syn["gold"],
                "blocked": syn["crimson"],
                "done": syn["emerald"],
                "idle": ui["fgMuted"],
                "unknown": ui["fgSubtle"],
            },
        }
        (out_dir / f"{pal['slug']}.json").write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")

    # Warm-parchment Daylight companion for Herdr auto light/dark switching
    light_doc = {
        "background": "#F6F3EC",
        "foreground": "#1D2026",
        "selection": "#E4D9BF",
        "cursor": "#B08212",
        "ansi": [
            "#1D2026", "#C43B46", "#2B7F56", "#A4780E",
            "#2A6AB3", "#734EB8", "#1F7A84", "#636973",
            "#5C636E", "#D94C58", "#359667", "#BC8C16",
            "#3B7EC9", "#8763CC", "#29919C", "#15171A",
        ],
        "colors": {
            "canvas": "#EFECE4",
            "chrome": "#ECE8DF",
            "surface": "#F6F3EC",
            "popover": "#FAF8F3",
            "raised": "#E5E0D5",
            "hover": "#EAE5DB",
            "selected": "#E4D9BF",
            "border": "#D5CFC3",
            "input": "#A4780E",
            "muted": "#5C636E",
            "dim": "#878D96",
            "accent": "#A4780E",
            "accent_foreground": "#FAF8F3",
            "solid": "#A4780E",
            "solid_foreground": "#FAF8F3",
            "working": "#A4780E",
            "blocked": "#C43B46",
            "done": "#2B7F56",
            "idle": "#5C636E",
            "unknown": "#878D96",
        },
    }
    (out_dir / "gotham-noir-daylight.json").write_text(json.dumps(light_doc, indent=2) + "\n", encoding="utf-8")

    syntax_js = """// Generated by Gotham Noir scripts/build.py for Herdr Files panel syntax colors
export function gothamNoirSyntax(theme) {
  const bg = (theme?.background || "").toLowerCase();
  const darkMap = {
    "#15171a": { comment: "#878d96", keyword: "#b695e8", string: "#63c794", number: "#e29754", function: "#74aeeb", type: "#f0c946", operator: "#68c5ce", error: "#e86a74" },
    "#101215": { comment: "#838b96", keyword: "#b896ee", string: "#56cca0", number: "#e59a52", function: "#6fb3f5", type: "#f5d042", operator: "#5ccbd6", error: "#f06875" },
    "#1d1f21": { comment: "#91969c", keyword: "#b396de", string: "#75bf96", number: "#d99862", function: "#7fb0e0", type: "#e6c15a", operator: "#72bcc4", error: "#de717a" },
    "#151417": { comment: "#8b878f", keyword: "#ba94e8", string: "#5fc491", number: "#e49854", function: "#72ace8", type: "#efc850", operator: "#66c2cc", error: "#e5535c" },
    "#f6f3ec": { comment: "#5c636e", keyword: "#734eb8", string: "#2b7f56", number: "#a4780e", function: "#2a6ab3", type: "#a4780e", operator: "#1f7a84", error: "#c43b46" },
  };
  return darkMap[bg] || null;
}
"""
    (out_dir / "gotham-noir-syntax.js").write_text(syntax_js, encoding="utf-8")

    readme = """# Gotham Noir for Herdr

Includes all 4 dark variants (`gotham-noir-year-one`, `gotham-noir-batcomputer`, `gotham-noir-arkham-slate`, `gotham-noir-vengeance`) plus `gotham-noir-daylight` for automatic light/dark switching.

## Install

```bash
mkdir -p ~/.config/herdr-app/themes
cp ports/herdr/*.json ~/.config/herdr-app/themes/
```

Open **Settings -> Appearance** and select `gotham-noir-year-one` (or set `"theme": { "dark": "gotham-noir-year-one", "light": "gotham-noir-daylight" }` in `~/.config/herdr-app/settings.json`).

Optional syntax helper for the Herdr Files panel mod: [`gotham-noir-syntax.js`](gotham-noir-syntax.js).
"""
    (out_dir / "README.md").write_text(readme, encoding="utf-8")


def _write_github_userstyle(flagship: dict, root: Path) -> None:
    out_dir = root / "ports" / "github"
    out_dir.mkdir(parents=True, exist_ok=True)
    ui, syn = flagship["ui"], flagship["syntax"]
    css = f"""/* ==UserStyle==
@name         Gotham Noir for GitHub
@namespace    gotham-noir
@version      1.0.0
@description  Anti-halation Gotham Noir Year One dark theme for GitHub UI, diffs, and code blocks.
@author       Zain Ahmed (https://zainahmed.net/)
@license      MIT
==/UserStyle== */

@-moz-document domain("github.com") {{
  :root {{
    --fontStack-monospace: "Monaspace Neon", "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, Consolas, monospace !important;
  }}

  [data-color-mode="dark"],
  [data-color-mode="auto"][data-dark-theme*="dark"] {{
    color-scheme: dark;
    --bgColor-default: {ui["bg"]} !important;
    --bgColor-muted: {ui["bgSide"]} !important;
    --bgColor-inset: {ui["bgDeep"]} !important;
    --bgColor-emphasis: {ui["surfaceHover"]} !important;
    --bgColor-inverse: {ui["fgStrong"]} !important;
    --bgColor-disabled: {ui["surface"]} !important;
    --bgColor-neutral-emphasis: {ui["fgSubtle"]} !important;
    --bgColor-neutral-muted: {ui["fgMuted"]}26 !important;
    --bgColor-accent-emphasis: {syn["blue"]} !important;
    --bgColor-accent-muted: {syn["blue"]}26 !important;
    --bgColor-success-emphasis: {syn["emerald"]} !important;
    --bgColor-success-muted: {syn["emerald"]}26 !important;
    --bgColor-attention-emphasis: {syn["gold"]} !important;
    --bgColor-attention-muted: {syn["gold"]}26 !important;
    --bgColor-danger-emphasis: {syn["crimson"]} !important;
    --bgColor-danger-muted: {syn["crimson"]}26 !important;
    --fgColor-default: {ui["fg"]} !important;
    --fgColor-muted: {ui["fgMuted"]} !important;
    --fgColor-accent: {syn["blue"]} !important;
    --fgColor-success: {syn["emerald"]} !important;
    --fgColor-attention: {syn["gold"]} !important;
    --fgColor-danger: {syn["crimson"]} !important;
    --borderColor-default: {ui["border"]} !important;
    --borderColor-muted: {ui["borderSubtle"]} !important;
    --borderColor-accent-emphasis: {ui["accent"]} !important;
    --diffBlob-addition-bgColor-line: {ui["diffInsertLineBg"]} !important;
    --diffBlob-addition-bgColor-word: {ui["diffInsertBg"]} !important;
    --diffBlob-deletion-bgColor-line: {ui["diffRemoveLineBg"]} !important;
    --diffBlob-deletion-bgColor-word: {ui["diffRemoveBg"]} !important;
    --color-prettylights-syntax-comment: {syn["muted"]} !important;
    --color-prettylights-syntax-constant: {syn["amber"]} !important;
    --color-prettylights-syntax-entity: {syn["blue"]} !important;
    --color-prettylights-syntax-entity-tag: {syn["blue"]} !important;
    --color-prettylights-syntax-keyword: {syn["violet"]} !important;
    --color-prettylights-syntax-string: {syn["emerald"]} !important;
    --color-prettylights-syntax-variable: {syn["amber"]} !important;
    --color-prettylights-syntax-markup-heading: {syn["gold"]} !important;
    --color-prettylights-syntax-markup-inserted-text: {syn["emerald"]} !important;
    --color-prettylights-syntax-markup-deleted-text: {syn["crimson"]} !important;
  }}
}}
"""
    (out_dir / "gotham-noir.user.css").write_text(css, encoding="utf-8")
    readme = """# Gotham Noir for GitHub

Stylus UserStyle that themes GitHub's dark interface, pull request diffs, and syntax code blocks with **Gotham Noir - Year One**.

## Install

1. Install the [Stylus](https://add0n.com/stylus.html) browser extension.
2. Open **[gotham-noir.user.css](https://raw.githubusercontent.com/thezaynahmed/gotham-noir/main/ports/github/gotham-noir.user.css)** and click **Install style**.
3. Set GitHub Appearance to **Dark default** and reload.
"""
    (out_dir / "README.md").write_text(readme, encoding="utf-8")


def _write_linear(palettes: list[dict], root: Path) -> None:
    out_dir = root / "ports" / "linear"
    out_dir.mkdir(parents=True, exist_ok=True)
    flagship = palettes[0]
    snippets = []
    for pal in palettes:
        ui = pal["ui"]
        doc = {
            "base": _hex_to_cie_lch(ui["bg"]),
            "accent": _hex_to_cie_lch(ui["accent"]),
            "contrast": 35,
            "sidebar": {
                "base": _hex_to_cie_lch(ui["bgSide"]),
                "accent": _hex_to_cie_lch(ui["accent"]),
                "contrast": 35,
            },
        }
        line = json.dumps(doc, separators=(",", ":"))
        (out_dir / f"{pal['slug']}.json").write_text(line + "\n", encoding="utf-8")
        snippets.append(f"### {pal['name']}\n\n```json\n{line}\n```")

    ui, syn = flagship["ui"], flagship["syntax"]
    user_css = f"""/* ==UserStyle==
@name         Gotham Noir for Linear Code Blocks
@namespace    gotham-noir
@version      1.0.0
@description  Gotham Noir Year One syntax colors for Linear code blocks and diffs.
@author       Zain Ahmed (https://zainahmed.net/)
@license      MIT
==/UserStyle== */

@-moz-document domain("linear.app") {{
  pre, code, [data-line-text] {{
    font-family: "Monaspace Neon", "JetBrains Mono", ui-monospace, Menlo, monospace !important;
  }}

  @media (prefers-color-scheme: dark) {{
    pre, pre code {{
      background-color: {ui["bgSide"]} !important;
      color: {ui["fg"]} !important;
    }}
    [class*="syntax-comment"] {{ color: {syn["muted"]} !important; font-style: italic !important; }}
    [class*="syntax-string"] {{ color: {syn["emerald"]} !important; }}
    [class*="syntax-keyword"] {{ color: {syn["violet"]} !important; }}
    [class*="syntax-function"] {{ color: {syn["blue"]} !important; }}
    [class*="syntax-type"], [class*="syntax-class"] {{ color: {syn["gold"]} !important; }}
    [class*="syntax-number"], [class*="syntax-constant"] {{ color: {syn["amber"]} !important; }}
    [class*="syntax-operator"] {{ color: {syn["cyan"]} !important; }}
  }}
}}
"""
    (out_dir / "gotham-noir.user.css").write_text(user_css, encoding="utf-8")
    readme = (
        "# Gotham Noir for Linear\n\n"
        "## 1. Interface Theme\n\n"
        "Open **Settings -> Preferences -> Interface theme -> Custom -> Import theme** and paste any variant below:\n\n"
        + "\n\n".join(snippets)
        + "\n\n## 2. Code Blocks (Stylus UserStyle)\n\n"
        "1. Install [Stylus](https://add0n.com/stylus.html).\n"
        "2. Open **[gotham-noir.user.css](https://raw.githubusercontent.com/thezaynahmed/gotham-noir/main/ports/linear/gotham-noir.user.css)** and click **Install style**.\n"
    )
    (out_dir / "README.md").write_text(readme, encoding="utf-8")


def _write_slack(palettes: list[dict], root: Path) -> None:
    out_dir = root / "ports" / "slack"
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for pal in palettes:
        ui, syn = pal["ui"], pal["syntax"]
        # 10-color Slack custom sidebar string (compatible with classic & modern Slack)
        full_10 = ",".join([
            ui["bgSide"], ui["surface"], ui["selectionBg"], ui["fgStrong"],
            ui["surfaceHover"], ui["fg"], syn["emerald"], ui["accent"],
            ui["bgDeep"], ui["fgStrong"],
        ])
        modern_4 = ",".join([ui["bgSide"], ui["selectionBg"], syn["emerald"], ui["accent"]])
        (out_dir / f"{pal['slug']}.txt").write_text(full_10 + "\n", encoding="utf-8")
        rows.append(f"### {pal['name']}\n\n- **Full 10-color string:** `{full_10}`\n- **Compact 4-color string:** `{modern_4}`")

    readme = (
        "# Gotham Noir for Slack\n\n"
        "Open **Slack -> Preferences -> Themes -> Custom theme -> Import** (or paste any string into a Slack message to preview and apply):\n\n"
        + "\n\n".join(rows)
        + "\n"
    )
    (out_dir / "README.md").write_text(readme, encoding="utf-8")


def _write_chrome(palettes: list[dict], root: Path) -> None:
    out_dir = root / "ports" / "chrome"
    out_dir.mkdir(parents=True, exist_ok=True)
    icon_src = root / "packages" / "vscode" / "images" / "icon.png"
    for pal in palettes:
        ui = pal["ui"]
        vdir = out_dir / pal["slug"]
        vdir.mkdir(parents=True, exist_ok=True)
        if icon_src.exists():
            shutil.copy2(icon_src, vdir / "icon-128.png")
        manifest = {
            "manifest_version": 3,
            "name": pal["name"],
            "version": "1.0.0",
            "description": f"{pal['name']} anti-halation dark theme for Chrome (OKLCH + APCA calibrated).",
            "icons": {"128": "icon-128.png"},
            "theme": {
                "colors": {
                    "frame": list(_hex_rgb(ui["bgDeep"])),
                    "frame_inactive": list(_hex_rgb(ui["bgDeep"])),
                    "frame_incognito": list(_hex_rgb(ui["bgDeep"])),
                    "frame_incognito_inactive": list(_hex_rgb(ui["bgDeep"])),
                    "toolbar": list(_hex_rgb(ui["bg"])),
                    "toolbar_text": list(_hex_rgb(ui["fg"])),
                    "toolbar_button_icon": list(_hex_rgb(ui["fgMuted"])),
                    "tab_text": list(_hex_rgb(ui["fgStrong"])),
                    "tab_background_text": list(_hex_rgb(ui["fgMuted"])),
                    "tab_background_text_inactive": list(_hex_rgb(ui["fgSubtle"])),
                    "bookmark_text": list(_hex_rgb(ui["fg"])),
                    "ntp_background": list(_hex_rgb(ui["bg"])),
                    "ntp_text": list(_hex_rgb(ui["fg"])),
                    "ntp_link": list(_hex_rgb(ui["accent"])),
                    "omnibox_background": list(_hex_rgb(ui["bgSide"])),
                    "omnibox_text": list(_hex_rgb(ui["fgStrong"])),
                }
            },
        }
        (vdir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    readme = """# Gotham Noir for Google Chrome

Manifest V3 browser themes for all 4 dark variants (`gotham-noir-year-one`, `gotham-noir-batcomputer`, `gotham-noir-arkham-slate`, `gotham-noir-vengeance`).

## Install

1. Open `chrome://extensions` in Google Chrome.
2. Enable **Developer mode** (top right).
3. Click **Load unpacked** and select any variant folder inside `ports/chrome/` (for example `ports/chrome/gotham-noir-year-one`).
"""
    (out_dir / "README.md").write_text(readme, encoding="utf-8")


def _write_shadcn(palettes: list[dict], root: Path) -> None:
    out_dir = root / "ports" / "shadcn"
    reg_dir = out_dir / "r"
    reg_dir.mkdir(parents=True, exist_ok=True)
    flagship = palettes[0]

    def css_block(pal: dict) -> dict[str, str]:
        ui, syn = pal["ui"], pal["syntax"]
        return {
            "radius": "0.5rem",
            "background": ui["bg"],
            "foreground": ui["fg"],
            "card": ui["surface"],
            "card-foreground": ui["fgStrong"],
            "popover": ui["elevated"],
            "popover-foreground": ui["fgStrong"],
            "primary": ui["buttonBg"],
            "primary-foreground": ui["buttonFg"],
            "secondary": ui["surfaceHover"],
            "secondary-foreground": ui["fgStrong"],
            "muted": ui["bgSide"],
            "muted-foreground": ui["fgMuted"],
            "accent": ui["selectionBg"],
            "accent-foreground": ui["fgStrong"],
            "destructive": syn["crimson"],
            "destructive-foreground": "#111316",
            "border": ui["border"],
            "input": ui["border"],
            "ring": ui["borderActive"],
            "chart-1": ui["accent"],
            "chart-2": syn["emerald"],
            "chart-3": syn["blue"],
            "chart-4": syn["violet"],
            "chart-5": syn["crimson"],
            "sidebar": ui["bgSide"],
            "sidebar-foreground": ui["fg"],
            "sidebar-primary": ui["accent"],
            "sidebar-primary-foreground": ui["accentFg"],
            "sidebar-accent": ui["surfaceHover"],
            "sidebar-accent-foreground": ui["fgStrong"],
            "sidebar-border": ui["borderSubtle"],
            "sidebar-ring": ui["borderActive"],
        }

    dark_vars = css_block(flagship)
    light_vars = {
        "radius": "0.5rem",
        "background": "#F6F3EC",
        "foreground": "#1D2026",
        "card": "#FAF8F3",
        "card-foreground": "#15171A",
        "popover": "#FAF8F3",
        "popover-foreground": "#15171A",
        "primary": "#A4780E",
        "primary-foreground": "#FAF8F3",
        "secondary": "#EAE5DB",
        "secondary-foreground": "#1D2026",
        "muted": "#EFECE4",
        "muted-foreground": "#5C636E",
        "accent": "#E4D9BF",
        "accent-foreground": "#15171A",
        "destructive": "#C43B46",
        "destructive-foreground": "#FAF8F3",
        "border": "#D5CFC3",
        "input": "#D5CFC3",
        "ring": "#A4780E",
        "chart-1": "#A4780E",
        "chart-2": "#2B7F56",
        "chart-3": "#2A6AB3",
        "chart-4": "#734EB8",
        "chart-5": "#C43B46",
        "sidebar": "#ECE8DF",
        "sidebar-foreground": "#1D2026",
        "sidebar-primary": "#A4780E",
        "sidebar-primary-foreground": "#FAF8F3",
        "sidebar-accent": "#E4D9BF",
        "sidebar-accent-foreground": "#15171A",
        "sidebar-border": "#D5CFC3",
        "sidebar-ring": "#A4780E",
    }

    registry_item = {
        "$schema": "https://ui.shadcn.com/schema/registry-item.json",
        "name": "gotham-noir",
        "type": "registry:theme",
        "title": "Gotham Noir",
        "description": "Anti-halation nocturnal dark theme (Year One) for shadcn/ui with OKLCH + APCA contrast.",
        "author": "Zain Ahmed (https://zainahmed.net/)",
        "cssVars": {
            "light": light_vars,
            "dark": dark_vars,
        },
    }
    (reg_dir / "gotham-noir.json").write_text(json.dumps(registry_item, indent=2) + "\n", encoding="utf-8")

    def render_vars(mapping: dict[str, str]) -> str:
        return "\n".join(f"  --{k}: {v};" for k, v in mapping.items())

    variant_blocks = []
    for pal in palettes[1:]:
        cls = pal["slug"].replace("gotham-noir-", "theme-")
        variant_blocks.append(f".dark.{cls} {{\n{render_vars(css_block(pal))}\n}}")

    css_text = (
        "/* Gotham Noir for shadcn/ui (Tailwind CSS v4 + v3 compatible) */\n"
        f":root {{\n{render_vars(light_vars)}\n}}\n\n"
        f".dark {{\n{render_vars(dark_vars)}\n}}\n\n"
        + "\n\n".join(variant_blocks)
        + "\n"
    )
    (out_dir / "gotham-noir.css").write_text(css_text, encoding="utf-8")

    readme = """# Gotham Noir for shadcn/ui

Install directly via the shadcn CLI registry item, or import [`gotham-noir.css`](gotham-noir.css) into `globals.css`.

## Install with shadcn CLI

```bash
npx shadcn@latest add https://raw.githubusercontent.com/thezaynahmed/gotham-noir/main/ports/shadcn/r/gotham-noir.json
```

Optional dark variant modifier classes in [`gotham-noir.css`](gotham-noir.css): `.dark.theme-batcomputer`, `.dark.theme-arkham-slate`, and `.dark.theme-vengeance`.
"""
    (out_dir / "README.md").write_text(readme, encoding="utf-8")


def _write_palette_and_fonts(palettes: list[dict], root: Path) -> None:
    out_dir = root / "ports" / "palette"
    out_dir.mkdir(parents=True, exist_ok=True)

    def css_vars(pal: dict) -> str:
        ui, syn = pal["ui"], pal["syntax"]
        pairs = [
            ("bg", ui["bg"]), ("bg-deep", ui["bgDeep"]), ("bg-side", ui["bgSide"]),
            ("surface", ui["surface"]), ("surface-hover", ui["surfaceHover"]),
            ("elevated", ui["elevated"]), ("border", ui["border"]),
            ("border-subtle", ui["borderSubtle"]), ("border-active", ui["borderActive"]),
            ("fg", ui["fg"]), ("fg-strong", ui["fgStrong"]), ("fg-muted", ui["fgMuted"]),
            ("fg-subtle", ui["fgSubtle"]), ("accent", ui["accent"]), ("accent-fg", ui["accentFg"]),
            ("selection", ui["selectionBg"]), ("gold", syn["gold"]), ("blue", syn["blue"]),
            ("emerald", syn["emerald"]), ("cyan", syn["cyan"]), ("amber", syn["amber"]),
            ("violet", syn["violet"]), ("crimson", syn["crimson"]), ("rose", syn["rose"]),
        ]
        return "\n".join(f"  --gn-{k}: {v};" for k, v in pairs)

    blocks = [f"/* Gotham Noir CSS Palette Tokens (https://github.com/thezaynahmed/gotham-noir) */\n:root,\n[data-gotham-theme=\"year-one\"] {{\n{css_vars(palettes[0])}\n}}"]
    for pal in palettes[1:]:
        key = pal["slug"].replace("gotham-noir-", "")
        blocks.append(f"[data-gotham-theme=\"{key}\"] {{\n{css_vars(pal)}\n}}")

    css_out = "\n\n".join(blocks) + "\n"
    (out_dir / "gotham-noir.css").write_text(css_out, encoding="utf-8")
    (out_dir / "gotham.css").write_text(css_out, encoding="utf-8")

    # W3C Design Tokens JSON (hex + OKLCH)
    w3c_tokens: dict[str, dict] = {}
    for pal in palettes:
        key = pal["slug"].replace("gotham-noir-", "")
        w3c_tokens[key] = {
            "ui": {
                k: {"$type": "color", "$value": v, "oklch": _hex_to_oklch(v)}
                for k, v in pal["ui"].items()
                if isinstance(v, str) and len(v) == 7 and v.startswith("#")
            },
            "syntax": {
                k: {"$type": "color", "$value": v, "oklch": _hex_to_oklch(v)}
                for k, v in pal["syntax"].items()
            },
            "ansi": {
                k: {"$type": "color", "$value": v, "oklch": _hex_to_oklch(v)}
                for k, v in pal["ansi"].items()
            },
        }
    (out_dir / "tokens.json").write_text(json.dumps(w3c_tokens, indent=2) + "\n", encoding="utf-8")

    (out_dir / "README.md").write_text(
        "# Gotham Noir Palette & CSS Tokens\n\n"
        "- [`gotham-noir.css`](gotham-noir.css) and [`gotham.css`](gotham.css): CSS custom properties (`--gn-*`) for all 4 dark variants using `:root` and `[data-gotham-theme=\"batcomputer|arkham-slate|vengeance\"]`.\n"
        "- [`tokens.json`](tokens.json): W3C Design Tokens JSON with both sRGB hex and OKLCH values.\n",
        encoding="utf-8",
    )

    fonts_dir = root / "ports" / "fonts"
    fonts_dir.mkdir(parents=True, exist_ok=True)
    (fonts_dir / "README.md").write_text(
        "# Gotham Noir Dyslexia & Readability Font Stack\n\n"
        "Gotham Noir pairs anti-halation contrast with high-legibility monospaced typography.\n\n"
        "| Preset | Font Family | Best For |\n"
        "| :--- | :--- | :--- |\n"
        "| **Default** | `Monaspace Neon` + `Monaspace Radon` italics | Texture Healing (`+calt +ss01..03 +zero +cv10`) |\n"
        "| **Wider Humanist** | `Monaspace Argon` + `Monaspace Radon` | Wider letter spacing for dyslexia comfort |\n"
        "| **Low-Vision / Dyslexia** | `Intel One Mono` | Distinct `b/d/p/q` and `1/l/I` separation |\n"
        "| **Maximum Homoglyph Clarity** | `Atkinson Hyperlegible Mono` | Braille Institute SIL OFL monospace |\n"
        "| **Neutral Geometry** | `Commit Mono` | Ultra-neutral engineering proportions |\n\n"
        "Ready-to-paste editor and Linux configs live in [`ports/ide-settings/font-presets.json`](../ide-settings/font-presets.json) and [`ports/linux-fontconfig/70-gotham-noir-fonts.conf`](../linux-fontconfig/70-gotham-noir-fonts.conf).\n",
        encoding="utf-8",
    )


def write_web_and_app_ports(palettes: list[dict], root: Path) -> None:
    """Write Herdr, GitHub, Linear, Slack, Chrome, shadcn/ui, Palette CSS, and Fonts ports."""
    _write_herdr(palettes, root)
    _write_github_userstyle(palettes[0], root)
    _write_linear(palettes, root)
    _write_slack(palettes, root)
    _write_chrome(palettes, root)
    _write_shadcn(palettes, root)
    _write_palette_and_fonts(palettes, root)
