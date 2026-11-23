"""Terminal, tmux, plist (.itermcolors / .terminal), Fontconfig, and Zsh generators."""

from __future__ import annotations

import json
import plistlib
from pathlib import Path
from contrast import hex_to_rgb01


ANSI_ORDER = [
    "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white",
    "brightBlack", "brightRed", "brightGreen", "brightYellow",
    "brightBlue", "brightMagenta", "brightCyan", "brightWhite",
]


def _iterm_color_dict(hex_color: str) -> dict:
    r, g, b = hex_to_rgb01(hex_color)
    return {
        "Alpha Component": 1.0,
        "Blue Component": float(round(b, 6)),
        "Color Space": "sRGB",
        "Green Component": float(round(g, 6)),
        "Red Component": float(round(r, 6)),
    }


def _ns_color_archive(hex_color: str) -> bytes:
    """Encode a hex color as an Apple NSKeyedArchiver NSColor binary plist."""
    r, g, b = hex_to_rgb01(hex_color)
    nsrgb = f"{r:.4f} {g:.4f} {b:.4f}\x00".encode("ascii")
    archive = {
        "$version": 100000,
        "$archiver": "NSKeyedArchiver",
        "$top": {"root": plistlib.UID(1)},
        "$objects": [
            "$null",
            {"NSRGB": nsrgb, "NSColorSpace": 2, "$class": plistlib.UID(2)},
            {"$classname": "NSColor", "$classes": ["NSColor", "NSObject"]},
        ],
    }
    return plistlib.dumps(archive, fmt=plistlib.FMT_BINARY)


def _ns_font_archive(font_name: str = "MonaspaceNeon-Regular", size: float = 14.5) -> bytes:
    """Encode a font as an Apple NSKeyedArchiver NSFont binary plist."""
    archive = {
        "$version": 100000,
        "$archiver": "NSKeyedArchiver",
        "$top": {"root": plistlib.UID(1)},
        "$objects": [
            "$null",
            {"$class": plistlib.UID(3), "NSName": plistlib.UID(2), "NSSize": float(size), "NSfFlags": 16},
            font_name,
            {"$classes": ["NSFont", "NSObject"], "$classname": "NSFont"},
        ],
    }
    return plistlib.dumps(archive, fmt=plistlib.FMT_BINARY)


def write_terminal_ports(palettes: list[dict], root: Path) -> None:
    """Generate all terminal, multiplexer, fontconfig, and shell ports from SSOT palettes."""
    ports = root / "ports"
    flagship = palettes[0]

    # 1. Ghostty
    ghostty_dir = ports / "ghostty"
    ghostty_dir.mkdir(parents=True, exist_ok=True)
    for pal in palettes:
        ui, ansi = pal["ui"], pal["ansi"]
        lore = pal.get("lore", {})
        lines = [
            f"# {pal['name']} — {lore.get('protocol', 'GOTHAM-NOIR')}",
            f"# {lore.get('reference', pal['description'])}",
        ]
        lines.extend(f"palette = {i}={ansi[k].lower()}" for i, k in enumerate(ANSI_ORDER))
        lines.extend([
            f"background = {ui['bg'].lower()}",
            f"foreground = {ui['fg'].lower()}",
            f"cursor-color = {ui['cursorBg'].lower()}",
            f"cursor-text = {ui['cursorFg'].lower()}",
            f"selection-background = {ui['selectionBg'].lower()}",
            f"selection-foreground = {ui['fgStrong'].lower()}",
        ])
        (ghostty_dir / pal["name"]).write_text("\n".join(lines) + "\n", encoding="utf-8")

    # 2. Warp (warpdotdev/themes YAML format)
    warp_dir = ports / "warp"
    warp_dir.mkdir(parents=True, exist_ok=True)
    for pal in palettes:
        ui, ansi = pal["ui"], pal["ansi"]
        lore = pal.get("lore", {})
        yaml_txt = (
            f"# {pal['name']} ({lore.get('protocol', 'GOTHAM-NOIR')})\n"
            f"# {lore.get('reference', pal['description'])}\n"
            f"name: \"{pal['name']}\"\n"
            f"accent: \"{ui['accent'].lower()}\"\n"
            f"cursor: \"{ui['cursorBg'].lower()}\"\n"
            f"background: \"{ui['bg'].lower()}\"\n"
            f"foreground: \"{ui['fg'].lower()}\"\n"
            f"details: darker\n"
            f"terminal_colors:\n"
            f"  normal:\n"
            f"    black: \"{ansi['black'].lower()}\"\n"
            f"    red: \"{ansi['red'].lower()}\"\n"
            f"    green: \"{ansi['green'].lower()}\"\n"
            f"    yellow: \"{ansi['yellow'].lower()}\"\n"
            f"    blue: \"{ansi['blue'].lower()}\"\n"
            f"    magenta: \"{ansi['magenta'].lower()}\"\n"
            f"    cyan: \"{ansi['cyan'].lower()}\"\n"
            f"    white: \"{ansi['white'].lower()}\"\n"
            f"  bright:\n"
            f"    black: \"{ansi['brightBlack'].lower()}\"\n"
            f"    red: \"{ansi['brightRed'].lower()}\"\n"
            f"    green: \"{ansi['brightGreen'].lower()}\"\n"
            f"    yellow: \"{ansi['brightYellow'].lower()}\"\n"
            f"    blue: \"{ansi['brightBlue'].lower()}\"\n"
            f"    magenta: \"{ansi['brightMagenta'].lower()}\"\n"
            f"    cyan: \"{ansi['brightCyan'].lower()}\"\n"
            f"    white: \"{ansi['brightWhite'].lower()}\"\n"
        )
        (warp_dir / f"{pal['warpSlug']}.yaml").write_text(yaml_txt, encoding="utf-8")

    # 3. Alacritty (standalone themes + full alacritty.toml)
    ala_dir = ports / "alacritty"
    ala_dir.mkdir(parents=True, exist_ok=True)
    for pal in palettes:
        ui, ansi = pal["ui"], pal["ansi"]
        toml_txt = (
            f"# {pal['name']} for Alacritty\n"
            f"[colors.primary]\n"
            f"background = \"{ui['bg'].lower()}\"\n"
            f"foreground = \"{ui['fg'].lower()}\"\n\n"
            f"[colors.cursor]\n"
            f"text = \"{ui['cursorFg'].lower()}\"\n"
            f"cursor = \"{ui['cursorBg'].lower()}\"\n\n"
            f"[colors.selection]\n"
            f"text = \"{ui['fgStrong'].lower()}\"\n"
            f"background = \"{ui['selectionBg'].lower()}\"\n\n"
            f"[colors.normal]\n"
            f"black   = \"{ansi['black'].lower()}\"\n"
            f"red     = \"{ansi['red'].lower()}\"\n"
            f"green   = \"{ansi['green'].lower()}\"\n"
            f"yellow  = \"{ansi['yellow'].lower()}\"\n"
            f"blue    = \"{ansi['blue'].lower()}\"\n"
            f"magenta = \"{ansi['magenta'].lower()}\"\n"
            f"cyan    = \"{ansi['cyan'].lower()}\"\n"
            f"white   = \"{ansi['white'].lower()}\"\n\n"
            f"[colors.bright]\n"
            f"black   = \"{ansi['brightBlack'].lower()}\"\n"
            f"red     = \"{ansi['brightRed'].lower()}\"\n"
            f"green   = \"{ansi['brightGreen'].lower()}\"\n"
            f"yellow  = \"{ansi['brightYellow'].lower()}\"\n"
            f"blue    = \"{ansi['brightBlue'].lower()}\"\n"
            f"magenta = \"{ansi['brightMagenta'].lower()}\"\n"
            f"cyan    = \"{ansi['brightCyan'].lower()}\"\n"
            f"white   = \"{ansi['brightWhite'].lower()}\"\n"
        )
        (ala_dir / f"{pal['slug']}.toml").write_text(toml_txt, encoding="utf-8")
    f_theme_body = (ala_dir / f"{flagship['slug']}.toml").read_text(encoding="utf-8")
    (ala_dir / "alacritty.toml").write_text(
        "# Alacritty Config - Gotham Noir (Dyslexia + ADHD + Late-Night Edition)\n"
        "[window]\npadding = { x = 14, y = 12 }\ndynamic_padding = true\nopacity = 1.0\n"
        "blur = false\noption_as_alt = \"OnlyLeft\"\n\n"
        "[scrolling]\nhistory = 10000\n\n"
        "[font]\nsize = 14.5\n"
        "normal = { family = \"Monaspace Neon\", style = \"Regular\" }\n"
        "bold = { family = \"Monaspace Neon\", style = \"Bold\" }\n"
        "italic = { family = \"Monaspace Radon\", style = \"Regular\" }\n"
        "bold_italic = { family = \"Monaspace Radon\", style = \"Bold\" }\n"
        "offset = { x = 1, y = 3 }\n\n"
        "[cursor]\nstyle = { shape = \"Block\", blinking = \"Never\" }\n\n"
        + f_theme_body,
        encoding="utf-8",
    )

    # 4. WezTerm (TOML schemes + full wezterm.lua)
    wez_dir = ports / "wezterm"
    wez_dir.mkdir(parents=True, exist_ok=True)
    for pal in palettes:
        ui, ansi = pal["ui"], pal["ansi"]
        normals = [ansi[k].lower() for k in ANSI_ORDER[:8]]
        brights = [ansi[k].lower() for k in ANSI_ORDER[8:]]
        wt_toml = (
            f"[metadata]\nname = \"{pal['name']}\"\nauthor = \"Zain Ahmed\"\n\n"
            f"[colors]\n"
            f"foreground = \"{ui['fg'].lower()}\"\n"
            f"background = \"{ui['bg'].lower()}\"\n"
            f"cursor_bg = \"{ui['cursorBg'].lower()}\"\n"
            f"cursor_fg = \"{ui['cursorFg'].lower()}\"\n"
            f"cursor_border = \"{ui['cursorBg'].lower()}\"\n"
            f"selection_fg = \"{ui['fgStrong'].lower()}\"\n"
            f"selection_bg = \"{ui['selectionBg'].lower()}\"\n"
            f"ansi = {json.dumps(normals)}\n"
            f"brights = {json.dumps(brights)}\n"
        )
        (wez_dir / f"{pal['name']}.toml").write_text(wt_toml, encoding="utf-8")

    fui, fansi = flagship["ui"], flagship["ansi"]
    fnorm = json.dumps([fansi[k].lower() for k in ANSI_ORDER[:8]]).replace('"', "'")
    fbright = json.dumps([fansi[k].lower() for k in ANSI_ORDER[8:]]).replace('"', "'")
    wez_lua = (
        "-- WezTerm Config - Gotham Noir Edition\n"
        "local wezterm = require 'wezterm'\n"
        "local config = wezterm.config_builder and wezterm.config_builder() or {}\n\n"
        "config.font = wezterm.font_with_fallback({\n"
        "  { family = 'Monaspace Neon', harfbuzz_features = { 'calt=1', 'ss01=1', 'ss02=1', 'ss03=1', 'zero=1', 'cv10=1' } },\n"
        "})\n"
        "config.font_rules = {\n"
        "  { italic = true, font = wezterm.font('Monaspace Radon', { italic = false }) },\n"
        "}\n"
        "config.font_size = 14.5\nconfig.line_height = 1.20\nconfig.cell_width = 1.04\n"
        "config.freetype_load_target = 'Light'\nconfig.front_end = 'WebGpu'\n"
        "config.default_cursor_style = 'SteadyBlock'\nconfig.cursor_blink_rate = 0\n"
        "config.window_background_opacity = 1.0\nconfig.macos_window_background_blur = 0\n"
        "config.window_padding = { left = 14, right = 14, top = 12, bottom = 12 }\n"
        "config.inactive_pane_hsb = { saturation = 0.85, brightness = 0.65 }\n"
        "config.scrollback_lines = 10000\nconfig.send_composed_key_when_left_alt_is_pressed = false\n\n"
        "config.colors = {\n"
        f"  foreground = '{fui['fg'].lower()}',\n"
        f"  background = '{fui['bg'].lower()}',\n"
        f"  cursor_bg = '{fui['cursorBg'].lower()}',\n"
        f"  cursor_fg = '{fui['cursorFg'].lower()}',\n"
        f"  cursor_border = '{fui['cursorBg'].lower()}',\n"
        f"  selection_fg = '{fui['fgStrong'].lower()}',\n"
        f"  selection_bg = '{fui['selectionBg'].lower()}',\n"
        f"  ansi = {fnorm},\n"
        f"  brights = {fbright},\n"
        "}\nreturn config\n"
    )
    (wez_dir / "wezterm.lua").write_text(wez_lua, encoding="utf-8")

    # 5. Kitty (kitty-themes upstream PR format + full kitty.conf)
    kitty_dir = ports / "kitty"
    kitty_dir.mkdir(parents=True, exist_ok=True)
    for pal in palettes:
        ui, ansi = pal["ui"], pal["ansi"]
        color_lines = [f"color{i:<2d} {ansi[k].lower()}" for i, k in enumerate(ANSI_ORDER)]
        k_txt = (
            f"## name: {pal['name']}\n"
            f"## author: Zain Ahmed\n"
            f"## license: MIT\n"
            f"## upstream: https://github.com/thezaynahmed/gotham-noir\n"
            f"## blurb: {pal['description']}\n\n"
            f"background {ui['bg'].lower()}\n"
            f"foreground {ui['fg'].lower()}\n"
            f"cursor {ui['cursorBg'].lower()}\n"
            f"cursor_text_color {ui['cursorFg'].lower()}\n"
            f"selection_background {ui['selectionBg'].lower()}\n"
            f"selection_foreground {ui['fgStrong'].lower()}\n\n"
            + "\n".join(color_lines) + "\n"
        )
        (kitty_dir / f"{pal['kittySlug']}.conf").write_text(k_txt, encoding="utf-8")
    (kitty_dir / "kitty.conf").write_text(
        "# Kitty Config - Gotham Noir Edition\n"
        "font_family      Monaspace Neon\nitalic_font      Monaspace Radon\n"
        "bold_italic_font Monaspace Radon\nfont_size        14.5\n"
        "font_features    MonaspaceNeon-Regular +calt +ss01 +ss02 +ss03 +zero +cv10\n\n"
        "modify_font cell_height 120%\nmodify_font cell_width 104%\n"
        "text_composition_strategy 1.7 30\n\n"
        "cursor_shape block\ncursor_blink_interval 0\nshell_integration no-cursor\n"
        "background_opacity 1.0\nbackground_blur 0\ninactive_text_alpha 0.65\n"
        "window_padding_width 12 14\nscrollback_lines 10000\nmacos_option_as_alt left\n\n"
        + (kitty_dir / f"{flagship['kittySlug']}.conf").read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    # 6. Windows Terminal
    wt_dir = ports / "windows-terminal"
    wt_dir.mkdir(parents=True, exist_ok=True)
    schemes = []
    for pal in palettes:
        ui, ansi = pal["ui"], pal["ansi"]
        schemes.append({
            "name": pal["name"],
            "background": ui["bg"].lower(),
            "foreground": ui["fg"].lower(),
            "cursorColor": ui["cursorBg"].lower(),
            "selectionBackground": ui["selectionBg"].lower(),
            "black": ansi["black"].lower(),
            "red": ansi["red"].lower(),
            "green": ansi["green"].lower(),
            "yellow": ansi["yellow"].lower(),
            "blue": ansi["blue"].lower(),
            "purple": ansi["magenta"].lower(),
            "cyan": ansi["cyan"].lower(),
            "white": ansi["white"].lower(),
            "brightBlack": ansi["brightBlack"].lower(),
            "brightRed": ansi["brightRed"].lower(),
            "brightGreen": ansi["brightGreen"].lower(),
            "brightYellow": ansi["brightYellow"].lower(),
            "brightBlue": ansi["brightBlue"].lower(),
            "brightPurple": ansi["brightMagenta"].lower(),
            "brightCyan": ansi["brightCyan"].lower(),
            "brightWhite": ansi["brightWhite"].lower(),
        })
    (wt_dir / "gotham-noir-schemes.json").write_text(json.dumps({"schemes": schemes}, indent=2) + "\n", encoding="utf-8")

    # 7. iTerm2 (.itermcolors Apple XML plist + Dynamic Profiles JSON)
    iterm_dir = ports / "iterm2"
    iterm_dir.mkdir(parents=True, exist_ok=True)
    dyn_profiles = []
    for pal in palettes:
        ui, ansi = pal["ui"], pal["ansi"]
        plist_dict = {f"Ansi {i} Color": _iterm_color_dict(ansi[k]) for i, k in enumerate(ANSI_ORDER)}
        plist_dict.update({
            "Background Color": _iterm_color_dict(ui["bg"]),
            "Bold Color": _iterm_color_dict(ui["fgStrong"]),
            "Cursor Color": _iterm_color_dict(ui["cursorBg"]),
            "Cursor Guide Color": _iterm_color_dict(ui["lineHighlightBg"]),
            "Cursor Text Color": _iterm_color_dict(ui["cursorFg"]),
            "Foreground Color": _iterm_color_dict(ui["fg"]),
            "Link Color": _iterm_color_dict(pal["syntax"]["blue"]),
            "Selected Text Color": _iterm_color_dict(ui["fgStrong"]),
            "Selection Color": _iterm_color_dict(ui["selectionBg"]),
        })
        with open(iterm_dir / f"{pal['itermName']}.itermcolors", "wb") as f:
            plistlib.dump(plist_dict, f, fmt=plistlib.FMT_XML, sort_keys=True)

        prof = {
            "Name": f"{pal['name']} (Dyslexia + ADHD)",
            "Guid": f"GOTHAM-NOIR-{pal['slug'].upper()}",
            "Normal Font": "MonaspaceNeon-Regular 15",
            "Horizontal Spacing": 1.04,
            "Vertical Spacing": 1.2,
            "Cursor Type": 2,
            "Blinking Cursor": False,
            "Blur": False,
            "Transparency": 0.0,
            "Minimum Contrast": 0.35,
            "ASCII Ligatures": True,
            "Option Key Sends": 2,
            "Scrollback Lines": 10000,
            "Prompt Before Closing 2": False,
        }
        prof.update({k: v for k, v in plist_dict.items() if k in {
            "Background Color", "Foreground Color", "Cursor Color", "Cursor Text Color",
            "Selection Color", "Selected Text Color",
        } or k.startswith("Ansi ")})
        dyn_profiles.append(prof)
    (iterm_dir / "gotham-noir-dynamic-profiles.json").write_text(
        json.dumps({"Profiles": dyn_profiles}, indent=2) + "\n", encoding="utf-8"
    )

    # 8. macOS Terminal.app (.terminal Apple XML plist + NSKeyedArchiver blobs)
    mterm_dir = ports / "macos-terminal"
    mterm_dir.mkdir(parents=True, exist_ok=True)
    ansi_term_keys = [
        ("ANSIBlackColor", "black"), ("ANSIRedColor", "red"), ("ANSIGreenColor", "green"),
        ("ANSIYellowColor", "yellow"), ("ANSIBlueColor", "blue"), ("ANSIMagentaColor", "magenta"),
        ("ANSICyanColor", "cyan"), ("ANSIWhiteColor", "white"),
        ("ANSIBrightBlackColor", "brightBlack"), ("ANSIBrightRedColor", "brightRed"),
        ("ANSIBrightGreenColor", "brightGreen"), ("ANSIBrightYellowColor", "brightYellow"),
        ("ANSIBrightBlueColor", "brightBlue"), ("ANSIBrightMagentaColor", "brightMagenta"),
        ("ANSIBrightCyanColor", "brightCyan"), ("ANSIBrightWhiteColor", "brightWhite"),
    ]
    for pal in palettes:
        ui, ansi = pal["ui"], pal["ansi"]
        term_plist = {
            "name": pal["name"],
            "type": "Window Settings",
            "ProfileCurrentVersion": 2.07,
            "columnCount": 110,
            "rowCount": 32,
            "BackgroundBlur": 0.0,
            "Bell": False,
            "VisualBell": False,
            "CursorBlink": False,
            "CursorType": 0,
            "Font": _ns_font_archive("MonaspaceNeon-Regular", 14.5),
            "FontAntialias": True,
            "FontWidthSpacing": 1.04,
            "FontHeightSpacing": 1.2,
            "shellExitAction": 1,
            "ShowActiveProcessArgumentsInTitle": False,
            "ShowActiveProcessInTitle": True,
            "ShowCommandKeyInTitle": False,
            "ShowDimensionsInTitle": False,
            "ShowRepresentedURLInTitle": False,
            "ShowRepresentedURLPathInTitle": False,
            "ShowShellCommandInTitle": False,
            "ShowTTYNameInTitle": False,
            "ShowWindowSettingsNameInTitle": False,
            "BackgroundColor": _ns_color_archive(ui["bg"]),
            "TextColor": _ns_color_archive(ui["fg"]),
            "TextBoldColor": _ns_color_archive(ui["fgStrong"]),
            "CursorColor": _ns_color_archive(ui["cursorBg"]),
            "SelectionColor": _ns_color_archive(ui["selectionBg"]),
        }
        for tkey, akey in ansi_term_keys:
            term_plist[tkey] = _ns_color_archive(ansi[akey])
        with open(mterm_dir / f"{pal['name']}.terminal", "wb") as f:
            plistlib.dump(term_plist, f, fmt=plistlib.FMT_XML, sort_keys=True)

    apply_sh = (
        "#!/usr/bin/env bash\nset -euo pipefail\n"
        "SCRIPT_DIR=\"$(cd \"$(dirname \"${BASH_SOURCE[0]}\")\" && pwd)\"\n"
        f"PROFILE_NAME=\"${{1:-{flagship['name']}}}\"\n"
        "THEME_FILE=\"${SCRIPT_DIR}/${PROFILE_NAME}.terminal\"\n"
        "if [[ ! -f \"$THEME_FILE\" ]]; then\n"
        "  echo \"Theme file not found: $THEME_FILE\" >&2; exit 1\n"
        "fi\n"
        "open \"$THEME_FILE\"\nsleep 1\n"
        "defaults write com.apple.Terminal \"Default Window Settings\" -string \"$PROFILE_NAME\"\n"
        "defaults write com.apple.Terminal \"Startup Window Settings\" -string \"$PROFILE_NAME\"\n"
        "echo \"✓ macOS Terminal.app configured with '$PROFILE_NAME'\"\n"
    )
    apply_path = mterm_dir / "apply-macos-terminal.sh"
    apply_path.write_text(apply_sh, encoding="utf-8")
    apply_path.chmod(0o755)

    # 9. tmux snippets + full tmux.conf
    tmux_dir = ports / "tmux"
    tmux_dir.mkdir(parents=True, exist_ok=True)
    for pal in palettes:
        ui = pal["ui"]
        lore = pal.get("lore", {})
        snippet = (
            f"# {pal['name']} ({lore.get('protocol', 'GOTHAM-NOIR')}) - tmux theme\n"
            f"setw -g window-style 'fg={ui['fgMuted'].lower()},bg={ui['tmuxDimBg'].lower()}'\n"
            f"setw -g window-active-style 'fg={ui['fg'].lower()},bg={ui['bg'].lower()}'\n"
            f"set -g pane-border-style 'fg={ui['borderSubtle'].lower()}'\n"
            f"set -g pane-active-border-style 'fg={ui['accent'].lower()}'\n"
        )
        (tmux_dir / f"{pal['slug']}.conf").write_text(snippet, encoding="utf-8")
    (tmux_dir / "tmux.conf").write_text(
        "# tmux Config - Gotham Noir (Dyslexia + ADHD + Late-Night Edition)\n"
        "set -g default-terminal \"tmux-256color\"\n"
        "set -ag terminal-overrides \",*:RGB\"\n"
        "set -g focus-events on\n"
        "set -ga terminal-overrides ',*:Ss=\\E[2 q:Se=\\E[2 q'\n"
        + (tmux_dir / f"{flagship['slug']}.conf").read_text(encoding="utf-8")
        + "set -g history-limit 10000\n",
        encoding="utf-8",
    )

    # 10. Linux Fontconfig
    fc_dir = ports / "linux-fontconfig"
    fc_dir.mkdir(parents=True, exist_ok=True)
    (fc_dir / "70-gotham-noir-fonts.conf").write_text(
        '<?xml version="1.0"?>\n<!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd">\n'
        "<!-- Linux Fontconfig - Monaspace, Intel One Mono & Atkinson Hyperlegible Mono -->\n"
        "<fontconfig>\n"
        "  <match target=\"font\">\n"
        "    <test name=\"family\" compare=\"contains\"><string>Monaspace</string></test>\n"
        "    <edit name=\"antialias\" mode=\"assign\"><bool>true</bool></edit>\n"
        "    <edit name=\"hinting\" mode=\"assign\"><bool>true</bool></edit>\n"
        "    <edit name=\"hintstyle\" mode=\"assign\"><const>hintslight</const></edit>\n"
        "    <edit name=\"lcdfilter\" mode=\"assign\"><const>lcddefault</const></edit>\n"
        "    <edit name=\"fontfeatures\" mode=\"append\">\n"
        "      <string>calt on</string><string>ss01 on</string><string>ss02 on</string>\n"
        "      <string>ss03 on</string><string>zero on</string><string>cv10 on</string>\n"
        "    </edit>\n"
        "  </match>\n"
        "  <match target=\"font\">\n"
        "    <test name=\"family\" compare=\"contains\"><string>Intel One Mono</string></test>\n"
        "    <edit name=\"antialias\" mode=\"assign\"><bool>true</bool></edit>\n"
        "    <edit name=\"hinting\" mode=\"assign\"><bool>true</bool></edit>\n"
        "    <edit name=\"hintstyle\" mode=\"assign\"><const>hintslight</const></edit>\n"
        "    <edit name=\"lcdfilter\" mode=\"assign\"><const>lcddefault</const></edit>\n"
        "  </match>\n"
        "  <match target=\"font\">\n"
        "    <test name=\"family\" compare=\"contains\"><string>Atkinson Hyperlegible Mono</string></test>\n"
        "    <edit name=\"antialias\" mode=\"assign\"><bool>true</bool></edit>\n"
        "    <edit name=\"hinting\" mode=\"assign\"><bool>true</bool></edit>\n"
        "    <edit name=\"hintstyle\" mode=\"assign\"><const>hintslight</const></edit>\n"
        "    <edit name=\"lcdfilter\" mode=\"assign\"><const>lcddefault</const></edit>\n"
        "  </match>\n"
        "</fontconfig>\n",
        encoding="utf-8",
    )

    # 11. Zsh ergonomic hook
    zsh_dir = ports / "zsh"
    zsh_dir.mkdir(parents=True, exist_ok=True)
    (zsh_dir / "gotham-noir-zsh.zsh").write_text(
        "# Gotham Noir Zsh Ergonomics\n"
        "[[ -o interactive ]] || return 0\n"
        "_gotham_steady_cursor() { printf '\\e[2 q'; }\n"
        "autoload -Uz add-zsh-hook && add-zsh-hook precmd _gotham_steady_cursor\n"
        "export LSCOLORS=\"Gxfxcxdxbxegedabagacad\"\n"
        "export LS_COLORS=\"di=1;36:ln=35:so=32:pi=33:ex=31:bd=34;46:cd=34;43:su=30;41:sg=30;46:tw=30;42:ow=30;43\"\n",
        encoding="utf-8",
    )
