"""WCAG 2.1, APCA-W3, and HSV hue/saturation verification helpers."""

from __future__ import annotations

import colorsys


def hex_to_rgb01(hex_color: str) -> tuple[float, float, float]:
    """Convert #RRGGBB or #RRGGBBAA hex string into (r, g, b) floats in [0, 1]."""
    h = hex_color.lstrip("#")
    if len(h) not in (6, 8):
        raise ValueError(f"Invalid hex color: {hex_color}")
    return (
        int(h[0:2], 16) / 255.0,
        int(h[2:4], 16) / 255.0,
        int(h[4:6], 16) / 255.0,
    )


def relative_luminance(hex_color: str) -> float:
    """Compute WCAG 2.1 relative luminance for a hex color."""
    def chan(c: float) -> float:
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (chan(v) for v in hex_to_rgb01(hex_color))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def wcag_contrast(c1: str, c2: str) -> float:
    """Compute WCAG 2.1 contrast ratio between two hex colors."""
    l1, l2 = relative_luminance(c1), relative_luminance(c2)
    return (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)


def apca_contrast(fg: str, bg: str) -> float:
    """Compute APCA-W3 0.0.98G-4g Lc contrast (signed; light-on-dark is negative)."""
    def y_apca(h: str) -> float:
        r, g, b = hex_to_rgb01(h)
        y = 0.2126729 * (r ** 2.4) + 0.7151522 * (g ** 2.4) + 0.0721750 * (b ** 2.4)
        return y if y >= 0.022 else y + (0.022 - y) ** 1.414

    yt, yb = y_apca(fg), y_apca(bg)
    if abs(yb - yt) < 0.0005:
        return 0.0
    if yb > yt:
        sapc = (yb ** 0.56 - yt ** 0.57) * 1.14
        return (sapc - 0.027) * 100.0 if sapc >= 0.1 else 0.0
    sapc = (yb ** 0.65 - yt ** 0.62) * 1.14
    return (sapc + 0.027) * 100.0 if sapc <= -0.1 else 0.0


def rgb_hsv_deg(hex_color: str) -> tuple[float, float, float]:
    """Return (hue_deg [0, 360), saturation [0, 1], value [0, 1])."""
    r, g, b = hex_to_rgb01(hex_color)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return h * 360.0, s, v


def hue_distance_deg(c1: str, c2: str) -> float:
    """Return circular hue distance in degrees [0, 180]."""
    h1 = rgb_hsv_deg(c1)[0]
    h2 = rgb_hsv_deg(c2)[0]
    diff = abs(h1 - h2) % 360.0
    return min(diff, 360.0 - diff)


def verify_palette(palette: dict) -> list[str]:
    """Validate WCAG 2.1, APCA Lc, anti-halation, and ANSI separation rules.

    Raises AssertionError if any required contrast or color gate fails.
    Returns formatted human-readable report lines.
    """
    name = palette["name"]
    ui = palette["ui"]
    syntax = palette["syntax"]
    ansi = palette["ansi"]
    bg = ui["bg"]

    assert bg.lower() != "#000000", f"{name}: bg must not be pure #000000 (halation)"
    assert ui["fg"].lower() != "#ffffff", f"{name}: fg must not be pure #ffffff (halation)"
    assert ui["fgStrong"].lower() != "#ffffff", f"{name}: fgStrong must not be pure #ffffff"

    fg_wcag = wcag_contrast(ui["fg"], bg)
    fg_apca = abs(apca_contrast(ui["fg"], bg))
    assert fg_wcag >= 10.0, f"{name}: fg WCAG {fg_wcag:.2f} < 10.0"
    assert fg_apca >= 75.0, f"{name}: fg APCA |Lc| {fg_apca:.1f} < 75.0"

    muted_wcag = wcag_contrast(syntax["muted"], bg)
    muted_apca = abs(apca_contrast(syntax["muted"], bg))
    assert muted_wcag >= 4.5, f"{name}: muted WCAG {muted_wcag:.2f} < 4.5"
    assert muted_apca >= 38.0, f"{name}: muted APCA |Lc| {muted_apca:.1f} < 38.0"

    for key in ("gold", "amber", "crimson", "emerald", "blue", "cyan", "violet", "rose"):
        val = syntax[key]
        cr = wcag_contrast(val, bg)
        lc = abs(apca_contrast(val, bg))
        min_cr = 5.0 if key == "crimson" else 6.5
        assert cr >= min_cr, f"{name}: syntax.{key} ({val}) WCAG {cr:.2f} < {min_cr}"
        assert lc >= 42.0, f"{name}: syntax.{key} ({val}) APCA |Lc| {lc:.1f} < 42.0"

    btn_cr = wcag_contrast(ui["buttonFg"], ui["buttonBg"])
    assert btn_cr >= 7.0, f"{name}: buttonFg/buttonBg WCAG {btn_cr:.2f} < 7.0"

    sug_fg_cr = wcag_contrast(ui["suggestSelectedFg"], ui["suggestSelectedBg"])
    sug_hi_cr = wcag_contrast(ui["suggestHighlightFg"], ui["suggestSelectedBg"])
    assert sug_fg_cr >= 4.5, f"{name}: suggestSelectedFg contrast {sug_fg_cr:.2f} < 4.5"
    assert sug_hi_cr >= 4.5, f"{name}: suggestHighlightFg contrast {sug_hi_cr:.2f} < 4.5"

    rg_dist = hue_distance_deg(ansi["red"], ansi["green"])
    assert rg_dist > 60.0, f"{name}: ANSI red/green hue distance {rg_dist:.1f}° <= 60°"

    for slot in ("blue", "magenta", "cyan"):
        color = ansi[slot]
        _, sat, _ = rgb_hsv_deg(color)
        cr = wcag_contrast(color, bg)
        assert sat >= 0.25, f"{name}: ANSI {slot} ({color}) saturation {sat:.2f} < 0.25 (too gray)"
        assert cr >= 4.5, f"{name}: ANSI {slot} ({color}) WCAG {cr:.2f} < 4.5"

    return [
        f"{name:22s} | bg={bg} fg={ui['fg']} ({fg_wcag:.2f}:1 / Lc {fg_apca:.1f}) | "
        f"btn={btn_cr:.2f}:1 | rg_hue_sep={rg_dist:.1f}°"
    ]
