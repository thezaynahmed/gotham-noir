"""Generate crisp PNG icons and palette showcase assets (strictly zero SVGs)."""

from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw


def _hex_rgba(hex_color: str, alpha: int = 255) -> tuple[int, int, int, int]:
    h = hex_color.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), alpha


def generate_icon_png(out_path: Path, size: int = 512) -> None:
    """Render an original geometric nocturnal obsidian + Bat-Signal Gold PNG icon."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    # Supersample 2x for anti-aliased edges
    ss = size * 2
    img = Image.new("RGBA", (ss, ss), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    pad = int(ss * 0.04)
    radius = int(ss * 0.20)
    # Matte obsidian badge + crisp tactical border
    draw.rounded_rectangle(
        [pad, pad, ss - pad, ss - pad],
        radius=radius,
        fill=_hex_rgba("#15171A"),
        outline=_hex_rgba("#2D323B"),
        width=max(4, ss // 64),
    )

    # Inner recessed frame
    inset = int(ss * 0.11)
    draw.rounded_rectangle(
        [inset, inset, ss - inset, ss - inset],
        radius=int(radius * 0.72),
        fill=_hex_rgba("#101215"),
        outline=_hex_rgba("#23272F"),
        width=max(2, ss // 128),
    )

    # Subtle horizon lines inside inner frame
    for frac in (0.30, 0.50, 0.70):
        y = int(ss * frac)
        draw.line(
            [(inset + 12, y), (ss - inset - 12, y)],
            fill=_hex_rgba("#1C1F24"),
            width=max(2, ss // 180),
        )

    # Original geometric nocturnal wing-chevron crest in Bat-Signal Gold (#F0C946)
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

    # Subtle code-prompt accent bars underneath crest
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


def generate_palette_preview_png(palettes: list[dict], out_path: Path) -> None:
    """Render a 1200x680 PNG specimen card showing all 4 dark-only variants."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    w, h = 1200, 680
    img = Image.new("RGBA", (w, h), _hex_rgba("#0C0E11"))
    draw = ImageDraw.Draw(img)

    # Outer header strip
    draw.text((40, 26), "GOTHAM NOIR  //  DETECTIVE #27  •  4 OKLCH + APCA DARK VARIANTS", fill=_hex_rgba("#ECEAE4"))
    draw.text((40, 48), "Nomex Kevlar canvases  •  Zero #000/#fff halation  •  VS Code / Open VSX / Zed / Ghostty / Warp / Paradev", fill=_hex_rgba("#878D96"))

    cols, rows = 2, 2
    margin_x, margin_y = 40, 84
    gap = 24
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

        # Card background & border
        draw.rounded_rectangle(
            [x0, y0, x1, y1],
            radius=12,
            fill=_hex_rgba(ui["bg"]),
            outline=_hex_rgba(ui["border"]),
            width=2,
        )
        # Top header bar inside card
        draw.rounded_rectangle(
            [x0 + 2, y0 + 2, x1 - 2, y0 + 46],
            radius=10,
            fill=_hex_rgba(ui["surface"]),
        )
        draw.rectangle([x0 + 2, y0 + 34, x1 - 2, y0 + 46], fill=_hex_rgba(ui["surface"]))
        draw.line([(x0 + 2, y0 + 46), (x1 - 2, y0 + 46)], fill=_hex_rgba(ui["border"]), width=1)

        # Accent pill & title
        draw.rounded_rectangle(
            [x0 + 16, y0 + 15, x0 + 30, y0 + 29],
            radius=4,
            fill=_hex_rgba(ui["accent"]),
        )
        proto = pal.get("lore", {}).get("protocol", "")
        draw.text((x0 + 42, y0 + 11), f"{pal['name']}", fill=_hex_rgba(ui["fgStrong"]))
        draw.text((x0 + 42, y0 + 26), f"{ui['bg']} / {ui['fg']}  •  {proto}", fill=_hex_rgba(ui["fgMuted"]))

        # Simulated code lines (crisp colored syntax bars)
        code_y = y0 + 68
        lines = [
            [(syn["violet"], 54), (syn["blue"], 92), (ui["fg"], 22), (syn["gold"], 78), (syn["fg"], 18)],
            [(syn["muted"], 180)],
            [(syn["blue"], 72), (syn["cyan"], 24), (syn["emerald"], 138), (syn["amber"], 52)],
            [(syn["violet"], 46), (ui["fg"], 68), (syn["cyan"], 18), (syn["amber"], 44), (syn["crimson"], 64)],
            [(syn["emerald"], 110), (syn["gold"], 88), (syn["violet"], 64)],
        ]
        for li, segs in enumerate(lines):
            cx = x0 + 20
            cy = code_y + li * 22
            # Line number tick
            draw.rectangle([cx, cy + 2, cx + 14, cy + 10], fill=_hex_rgba(ui["gutterFg"]))
            cx += 28
            for col, seg_w in segs:
                draw.rounded_rectangle([cx, cy + 1, cx + seg_w, cy + 11], radius=4, fill=_hex_rgba(col))
                cx += seg_w + 10

        # Swatch strip at bottom of card
        sw_y = y1 - 52
        sw_x = x0 + 20
        sw_w = (card_w - 40 - (len(syntax_keys) - 1) * 8) // len(syntax_keys)
        for si, skey in enumerate(syntax_keys):
            sx0 = sw_x + si * (sw_w + 8)
            draw.rounded_rectangle(
                [sx0, sw_y, sx0 + sw_w, sw_y + 30],
                radius=6,
                fill=_hex_rgba(syn[skey]),
            )

    img.save(out_path, format="PNG", optimize=True)
