"""Generate crisp, real-code PNG icons and non-AI syntax specimen screenshots."""

from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def _hex_rgba(hex_color: str, alpha: int = 255) -> tuple[int, int, int, int]:
    h = hex_color.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), alpha


def _load_font(size: int, bold: bool = False, italic: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Load crisp installed monospace font (Monaspace / JetBrains Mono / Menlo / DejaVu)."""
    home = Path.home()
    if italic:
        candidates = [
            home / "Library/Fonts/MonaspaceRadon-Italic.otf",
            home / "Library/Fonts/MonaspaceNeon-Italic.otf",
            home / "Library/Fonts/MonaspaceArgon-Italic.otf",
            home / "Library/Fonts/JetBrainsMono-Italic.ttf",
            Path("/Library/Fonts/MonaspaceRadon-Italic.otf"),
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Oblique.ttf"),
            Path("/usr/share/fonts/truetype/liberation/LiberationMono-Italic.ttf"),
        ]
    elif bold:
        candidates = [
            home / "Library/Fonts/MonaspaceNeon-SemiBold.otf",
            home / "Library/Fonts/MonaspaceNeon-Bold.otf",
            home / "Library/Fonts/MonaspaceArgon-SemiBold.otf",
            home / "Library/Fonts/JetBrainsMono-SemiBold.ttf",
            home / "Library/Fonts/JetBrainsMono-Bold.ttf",
            Path("/System/Library/Fonts/Menlo.ttc"),
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"),
            Path("/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"),
        ]
    else:
        candidates = [
            home / "Library/Fonts/MonaspaceNeon-Medium.otf",
            home / "Library/Fonts/MonaspaceNeon-Regular.otf",
            home / "Library/Fonts/MonaspaceArgon-Regular.otf",
            home / "Library/Fonts/JetBrainsMono-Regular.ttf",
            Path("/System/Library/Fonts/Menlo.ttc"),
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"),
            Path("/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"),
        ]
    for path in candidates:
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size=size)
            except OSError:
                continue
    return ImageFont.load_default()


def generate_icon_png(out_path: Path, size: int = 512) -> None:
    """Render an original geometric nocturnal obsidian + Signal Gold PNG icon."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    ss = size * 2
    img = Image.new("RGBA", (ss, ss), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    pad = int(ss * 0.04)
    radius = int(ss * 0.20)
    draw.rounded_rectangle(
        [pad, pad, ss - pad, ss - pad],
        radius=radius,
        fill=_hex_rgba("#15171A"),
        outline=_hex_rgba("#2D323B"),
        width=max(4, ss // 64),
    )

    inset = int(ss * 0.11)
    draw.rounded_rectangle(
        [inset, inset, ss - inset, ss - inset],
        radius=int(radius * 0.72),
        fill=_hex_rgba("#101215"),
        outline=_hex_rgba("#23272F"),
        width=max(2, ss // 128),
    )

    for frac in (0.30, 0.50, 0.70):
        y = int(ss * frac)
        draw.line(
            [(inset + 12, y), (ss - inset - 12, y)],
            fill=_hex_rgba("#1C1F24"),
            width=max(2, ss // 180),
        )

    cx, cy = ss // 2, int(ss * 0.49)
    w = ss * 0.30
    h = ss * 0.19
    crest = [
        (cx - w, cy - h * 0.25),
        (cx - w * 0.52, cy - h * 0.85),
        (cx - w * 0.16, cy - h * 0.28),
        (cx, cy - h * 0.65),
        (cx + w * 0.16, cy - h * 0.28),
        (cx + w * 0.52, cy - h * 0.85),
        (cx + w, cy - h * 0.25),
        (cx + w * 0.58, cy + h * 0.45),
        (cx + w * 0.24, cy + h * 0.18),
        (cx, cy + h * 0.92),
        (cx - w * 0.24, cy + h * 0.18),
        (cx - w * 0.58, cy + h * 0.45),
    ]
    draw.polygon(crest, fill=_hex_rgba("#F0C946"))

    bar_y = int(ss * 0.74)
    bar_h = max(6, ss // 42)
    draw.rounded_rectangle(
        [int(ss * 0.28), bar_y, int(ss * 0.46), bar_y + bar_h],
        radius=bar_h // 2,
        fill=_hex_rgba("#74AEEB"),
    )
    draw.rounded_rectangle(
        [int(ss * 0.50), bar_y, int(ss * 0.62), bar_y + bar_h],
        radius=bar_h // 2,
        fill=_hex_rgba("#63C794"),
    )
    draw.rounded_rectangle(
        [int(ss * 0.66), bar_y, int(ss * 0.72), bar_y + bar_h],
        radius=bar_h // 2,
        fill=_hex_rgba("#E86A74"),
    )

    final = img.resize((size, size), Image.Resampling.LANCZOS)
    final.save(out_path, format="PNG", optimize=True)


# Tokenized real TypeScript/React code specimen (same crisp style as editor window captures)
HERO_CODE_LINES: list[list[tuple[str, str]]] = [
    [("violet", "import"), ("fg", " { "), ("fg", "useState"), ("fg", " } "), ("violet", "from"), ("fg", " "), ("emerald", "'react'")],
    [],
    [("violet", "interface"), ("fg", " "), ("gold", "SignalProps"), ("fg", " {")],
    [("fg", "  "), ("cyan", "sector"), ("cyan", ":"), ("fg", " "), ("gold", "string")],
    [("fg", "  "), ("cyan", "activeNodes"), ("cyan", ":"), ("fg", " "), ("gold", "number")],
    [("fg", "  "), ("cyan", "alertMode"), ("cyan", "?:"), ("fg", " "), ("gold", "boolean")],
    [("fg", "}")],
    [],
    [("muted", "// Keeps telemetry badges compact: 120 becomes 99+")],
    [("violet", "const"), ("fg", " "), ("blue", "formatNodes"), ("fg", " "), ("cyan", "="), ("fg", " ("), ("amber", "count"), ("cyan", ":"), ("fg", " "), ("gold", "number"), ("fg", ") "), ("cyan", "=>"), ("fg", " "), ("amber", "count"), ("fg", " "), ("cyan", ">"), ("fg", " "), ("amber", "99"), ("fg", " "), ("cyan", "?"), ("fg", " "), ("emerald", "'99+'"), ("fg", " "), ("cyan", ":"), ("fg", " "), ("gold", "String"), ("fg", "("), ("amber", "count"), ("fg", ")")],
    [],
    [("violet", "export function"), ("fg", " "), ("blue", "SignalBadge"), ("fg", "({ "), ("amber", "sector"), ("fg", ", "), ("amber", "activeNodes"), ("fg", ", "), ("amber", "alertMode"), ("fg", " "), ("cyan", "="), ("fg", " "), ("amber", "false"), ("fg", " }: "), ("gold", "SignalProps"), ("fg", ") {")],
    [("fg", "  "), ("violet", "const"), ("fg", " ["), ("fg", "isOpen"), ("fg", ", "), ("blue", "setIsOpen"), ("fg", "] "), ("cyan", "="), ("fg", " "), ("blue", "useState"), ("fg", "("), ("amber", "false"), ("fg", ")")],
    [],
    [("fg", "  "), ("violet", "return"), ("fg", " (")],
    [("fg", "    <"), ("blue", "button"), ("fg", " "), ("cyan", "className"), ("cyan", "="), ("emerald", '"signal-badge"'), ("fg", " "), ("cyan", "onClick"), ("cyan", "="), ("fg", "{() "), ("cyan", "=>"), ("fg", " "), ("blue", "setIsOpen"), ("fg", "("), ("cyan", "!"), ("fg", "isOpen))}>")],
    [("fg", "      <"), ("gold", "Icon"), ("fg", " "), ("cyan", "name"), ("cyan", "="), ("emerald", '"radar"'), ("fg", " />")],
    [("fg", "      <"), ("blue", "span"), ("fg", ">{"), ("amber", "sector"), ("fg", "}</"), ("blue", "span"), ("fg", ">")],
    [("fg", "      {"), ("amber", "alertMode"), ("fg", " "), ("cyan", "&&"), ("fg", " <"), ("gold", "Count"), ("fg", " "), ("cyan", "value"), ("cyan", "="), ("fg", "{"), ("blue", "formatNodes"), ("fg", "("), ("amber", "activeNodes"), ("fg", ")} />}")],
    [("fg", "    </"), ("blue", "button"), ("fg", ">")],
    [("fg", "  )")],
    [("fg", "}")],
]

COMPACT_CODE_LINES: list[list[tuple[str, str]]] = [
    [("violet", "interface"), ("fg", " "), ("gold", "NodeHealth"), ("fg", " { "), ("cyan", "ok"), ("cyan", ":"), ("fg", " "), ("gold", "boolean"), ("fg", "; "), ("cyan", "ms"), ("cyan", ":"), ("fg", " "), ("gold", "number"), ("fg", " }")],
    [("muted", "// OKLCH balanced syntax + anti-halation surface")],
    [("violet", "export async function"), ("fg", " "), ("blue", "probe"), ("fg", "("), ("amber", "host"), ("cyan", ":"), ("fg", " "), ("gold", "string"), ("fg", "): "), ("gold", "Promise"), ("fg", "<"), ("gold", "NodeHealth"), ("fg", "> {")],
    [("fg", "  "), ("violet", "const"), ("fg", " "), ("fg", "url"), ("fg", " "), ("cyan", "="), ("fg", " "), ("emerald", "`https://${"), ("amber", "host"), ("emerald", "}/healthz`")],
    [("fg", "  "), ("violet", "const"), ("fg", " "), ("fg", "res"), ("fg", " "), ("cyan", "="), ("fg", " "), ("violet", "await"), ("fg", " "), ("blue", "fetch"), ("fg", "("), ("fg", "url"), ("fg", ")")],
    [("fg", "  "), ("violet", "if"), ("fg", " ("), ("cyan", "!"), ("fg", "res."), ("cyan", "ok"), ("fg", ") "), ("violet", "throw new"), ("fg", " "), ("crimson", "Error"), ("fg", "("), ("emerald", "'probe failed'"), ("fg", ")")],
    [("fg", "  "), ("violet", "return"), ("fg", " { "), ("cyan", "ok"), ("cyan", ":"), ("fg", " "), ("amber", "true"), ("fg", ", "), ("cyan", "ms"), ("cyan", ":"), ("fg", " "), ("amber", "14"), ("fg", " }")],
    [("fg", "}")],
]


def _draw_code_tokens(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    tokens: list[tuple[str, str]],
    pal: dict,
    font_reg: ImageFont.FreeTypeFont | ImageFont.ImageFont,
    font_ital: ImageFont.FreeTypeFont | ImageFont.ImageFont,
) -> None:
    ui = pal["ui"]
    syn = pal["syntax"]
    cx = x
    for role, text in tokens:
        color = ui["fg"] if role == "fg" else syn[role]
        f = font_ital if role == "muted" else font_reg
        draw.text((cx, y), text, fill=_hex_rgba(color), font=f)
        bbox = draw.textbbox((cx, y), text, font=f)
        cx = bbox[2]


def generate_code_window_png(pal: dict, out_path: Path, filename: str = "SignalBadge.tsx") -> None:
    """Render a crisp 2x macOS editor code window specimen (non-AI, real syntax tokens)."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    w, h = 1440, 880
    ui = pal["ui"]
    syn = pal["syntax"]

    img = Image.new("RGBA", (w, h), _hex_rgba(ui["bgDeep"]))
    draw = ImageDraw.Draw(img)

    # Outer macOS window frame
    m = 32
    wx0, wy0, wx1, wy1 = m, m, w - m, h - m
    draw.rounded_rectangle(
        [wx0, wy0, wx1, wy1],
        radius=18,
        fill=_hex_rgba(ui["bg"]),
        outline=_hex_rgba(ui["border"]),
        width=2,
    )

    # Title bar
    tb_h = 56
    draw.rounded_rectangle([wx0 + 2, wy0 + 2, wx1 - 2, wy0 + tb_h], radius=16, fill=_hex_rgba(ui["bgSide"]))
    draw.rectangle([wx0 + 2, wy0 + 36, wx1 - 2, wy0 + tb_h], fill=_hex_rgba(ui["bgSide"]))
    draw.line([(wx0 + 2, wy0 + tb_h), (wx1 - 2, wy0 + tb_h)], fill=_hex_rgba(ui["borderSubtle"]), width=1)

    # macOS traffic lights (toned cleanly to palette)
    dots = [("#E86A74", 0), ("#F0C946", 1), ("#63C794", 2)]
    for col, idx in dots:
        dx = wx0 + 28 + idx * 24
        dy = wy0 + tb_h // 2
        draw.ellipse([dx - 7, dy - 7, dx + 7, dy + 7], fill=_hex_rgba(col))

    title_font = _load_font(18, bold=False)
    code_font = _load_font(21, bold=False)
    ital_font = _load_font(21, italic=True)
    small_font = _load_font(15, bold=False)

    title = f"{filename}  -  {pal['name']}"
    tb = draw.textbbox((0, 0), title, font=title_font)
    tw = tb[2] - tb[0]
    draw.text(((w - tw) // 2, wy0 + 18), title, fill=_hex_rgba(ui["fgMuted"]), font=title_font)

    # Active line highlight on line 12 (export function SignalBadge)
    code_top = wy0 + tb_h + 24
    line_h = 31
    active_idx = 11
    ay0 = code_top + active_idx * line_h - 4
    draw.rectangle([wx0 + 2, ay0, wx1 - 2, ay0 + line_h], fill=_hex_rgba(ui["lineHighlightBg"]))

    # Code lines + line numbers
    for idx, tokens in enumerate(HERO_CODE_LINES):
        ly = code_top + idx * line_h
        lnum = f"{idx + 1:>2}"
        lcol = ui["accent"] if idx == active_idx else ui["gutterFg"]
        draw.text((wx0 + 34, ly), lnum, fill=_hex_rgba(lcol), font=code_font)
        if tokens:
            _draw_code_tokens(draw, wx0 + 96, ly, tokens, pal, code_font, ital_font)

    # Subtle bottom status bar with hex metrics & swatches
    sb_y = wy1 - 44
    draw.line([(wx0 + 2, sb_y), (wx1 - 2, sb_y)], fill=_hex_rgba(ui["borderSubtle"]), width=1)
    draw.text(
        (wx0 + 32, sb_y + 13),
        f"Canvas {ui['bg']}   |   Text {ui['fg']}   |   Accent {ui['accent']}   |   OKLCH + APCA Verified",
        fill=_hex_rgba(ui["fgMuted"]),
        font=small_font,
    )
    sw_keys = ["gold", "blue", "emerald", "cyan", "amber", "violet", "crimson", "rose"]
    for i, k in enumerate(sw_keys):
        sx = wx1 - 32 - (len(sw_keys) - i) * 26
        draw.rounded_rectangle([sx, sb_y + 14, sx + 18, sb_y + 30], radius=4, fill=_hex_rgba(syn[k]))

    img.save(out_path, format="PNG", optimize=True)


def generate_palette_preview_png(palettes: list[dict], out_path: Path) -> None:
    """Render a crisp 1600x920 2x2 real-code specimen card showing all 4 dark variants."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    w, h = 1600, 920
    img = Image.new("RGBA", (w, h), _hex_rgba("#0C0E11"))
    draw = ImageDraw.Draw(img)

    hdr_font = _load_font(22, bold=True)
    sub_font = _load_font(15, bold=False)
    card_title_font = _load_font(18, bold=True)
    card_meta_font = _load_font(14, bold=False)
    code_font = _load_font(15, bold=False)
    ital_font = _load_font(15, italic=True)

    draw.text((44, 24), "GOTHAM NOIR  |  4 ANTI-HALATION DARK VARIANTS", fill=_hex_rgba("#ECEAE4"), font=hdr_font)
    draw.text(
        (44, 54),
        "OKLCH perceptual balance  |  WCAG 2.1 AAA + APCA Lc verified  |  Zero #000/#fff halation",
        fill=_hex_rgba("#878D96"),
        font=sub_font,
    )

    cols, rows = 2, 2
    margin_x, margin_y = 44, 92
    gap = 26
    card_w = (w - 2 * margin_x - gap) // cols
    card_h = (h - margin_y - 36 - gap) // rows

    syntax_keys = ["gold", "blue", "emerald", "cyan", "amber", "violet", "crimson", "muted"]

    for idx, pal in enumerate(palettes[:4]):
        r_idx, c_idx = divmod(idx, cols)
        x0 = margin_x + c_idx * (card_w + gap)
        y0 = margin_y + r_idx * (card_h + gap)
        x1 = x0 + card_w
        y1 = y0 + card_h
        ui = pal["ui"]
        syn = pal["syntax"]

        draw.rounded_rectangle(
            [x0, y0, x1, y1],
            radius=14,
            fill=_hex_rgba(ui["bg"]),
            outline=_hex_rgba(ui["border"]),
            width=2,
        )
        # Window header bar
        draw.rounded_rectangle([x0 + 2, y0 + 2, x1 - 2, y0 + 54], radius=12, fill=_hex_rgba(ui["bgSide"]))
        draw.rectangle([x0 + 2, y0 + 38, x1 - 2, y0 + 54], fill=_hex_rgba(ui["bgSide"]))
        draw.line([(x0 + 2, y0 + 54), (x1 - 2, y0 + 54)], fill=_hex_rgba(ui["borderSubtle"]), width=1)

        # Traffic light dots
        for di, dcol in enumerate(("#E86A74", "#F0C946", "#63C794")):
            dx = x0 + 22 + di * 18
            dy = y0 + 28
            draw.ellipse([dx - 5, dy - 5, dx + 5, dy + 5], fill=_hex_rgba(dcol))

        draw.text((x0 + 82, y0 + 11), pal["name"], fill=_hex_rgba(ui["fgStrong"]), font=card_title_font)
        draw.text(
            (x0 + 82, y0 + 33),
            f"bg {ui['bg']}  |  fg {ui['fg']}  |  accent {ui['accent']}",
            fill=_hex_rgba(ui["fgMuted"]),
            font=card_meta_font,
        )

        # Real syntax-highlighted code lines
        code_y = y0 + 72
        line_step = 28
        for li, tokens in enumerate(COMPACT_CODE_LINES):
            cy = code_y + li * line_step
            lcol = ui["accent"] if li == 2 else ui["gutterFg"]
            draw.text((x0 + 20, cy), f"{li + 1:>2}", fill=_hex_rgba(lcol), font=code_font)
            _draw_code_tokens(draw, x0 + 52, cy, tokens, pal, code_font, ital_font)

        # Clean swatch bar at bottom
        sw_y = y1 - 46
        sw_x = x0 + 20
        sw_w = (card_w - 40 - (len(syntax_keys) - 1) * 10) // len(syntax_keys)
        for si, skey in enumerate(syntax_keys):
            sx0 = sw_x + si * (sw_w + 10)
            draw.rounded_rectangle(
                [sx0, sw_y, sx0 + sw_w, sw_y + 26],
                radius=6,
                fill=_hex_rgba(syn[skey]),
            )

    img.save(out_path, format="PNG", optimize=True)
