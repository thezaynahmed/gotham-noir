#!/usr/bin/env python3
"""Single-source-of-truth builder for the Gotham Noir theme ecosystem."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from assets import generate_icon_png, generate_palette_preview_png
from contrast import verify_palette
from generators_ide import write_ide_outputs
from generators_terminals import write_terminal_ports


def load_palettes(palettes_dir: Path) -> list[dict]:
    """Load palettes in canonical Batman lore order."""
    order = [
        "gotham-noir-year-one.json",
        "gotham-noir-batcomputer.json",
        "gotham-noir-arkham-slate.json",
        "gotham-noir-vengeance.json",
    ]
    return [json.loads((palettes_dir / fname).read_text(encoding="utf-8")) for fname in order]


def clean_generated_dirs(root: Path) -> None:
    """Remove generated theme artifacts so stale filenames never persist across renames."""
    dirs = [
        root / "packages" / "vscode" / "themes",
        root / "ports" / "ghostty",
        root / "ports" / "warp",
        root / "ports" / "alacritty",
        root / "ports" / "wezterm",
        root / "ports" / "kitty",
        root / "ports" / "iterm2",
        root / "ports" / "macos-terminal",
        root / "ports" / "tmux",
    ]
    for d in dirs:
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True, exist_ok=True)


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    palettes = load_palettes(root / "palettes")

    print("=== Contrast & Color Science Gate (WCAG 2.1 + APCA Lc) ===")
    for pal in palettes:
        for line in verify_palette(pal):
            print("  PASS:", line)

    clean_generated_dirs(root)
    shutil.copy2(root / "LICENSE", root / "packages" / "vscode" / "LICENSE")
    generate_icon_png(root / "assets" / "icon-512.png", size=512)
    generate_icon_png(root / "packages" / "vscode" / "images" / "icon.png", size=128)
    generate_palette_preview_png(palettes, root / "packages" / "vscode" / "images" / "palette-preview.png")
    print("✓ Generated PNG assets (0 SVGs)")

    write_ide_outputs(palettes, root)
    print("✓ Generated VS Code, Zed, Antigravity presets, Paradev themes, and IDE configs")

    write_terminal_ports(palettes, root)
    print("✓ Generated Ghostty, Warp, Alacritty, WezTerm, Kitty, Windows Terminal, iTerm2, macOS Terminal, tmux, Fontconfig & Zsh ports")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
