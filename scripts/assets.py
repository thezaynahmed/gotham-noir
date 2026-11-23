"""Generate crisp, studio-grade PNG icons, multi-pane IDE+terminal screenshots, and 4-variant hero banners."""

from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

from contrast import apca_contrast, wcag_contrast


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


TokenRun = tuple[str, str]
CodeLine = tuple[str | None, list[TokenRun]]  # (git_marker: 'add' | 'mod' | 'del' | None, runs)

VARIANT_SCENES: dict[str, dict] = {
    "gotham-noir-year-one": {
        "filename": "bat-signal-operator.ts",
        "language": "TypeScript + Kubernetes",
        "active_line": 4,
        "code": [
            (None, [("muted", "// gotham-ops // Kubernetes Rooftop Beacon Operator")]),
            (None, [("violet", "@KubeController"), ("fg", "({ "), ("cyan", "namespace"), ("cyan", ": "), ("emerald", '"gotham-ops"'), ("fg", ", "), ("cyan", "ttl"), ("cyan", ": "), ("amber", "30"), ("fg", " })")]),
            (None, [("violet", "export class"), ("fg", " "), ("gold", "WayneMeshOperator"), ("fg", " "), ("violet", "implements"), ("fg", " "), ("gold", "Reconciler"), ("fg", "<"), ("gold", "BeaconSpec"), ("fg", "> {")]),
            ("mod", [("fg", "  "), ("violet", "readonly"), ("fg", " "), ("fg", "cfg"), ("cyan", " = "), ("fg", "{ "), ("cyan", "id"), ("cyan", ": "), ("emerald", '"year-one"'), ("fg", ", "), ("cyan", "surface"), ("cyan", ": "), ("emerald", '"#15171A"'), ("fg", " };")]),
            ("add", [("fg", "  "), ("violet", "readonly"), ("fg", " "), ("amber", "apcaLc"), ("cyan", ": "), ("gold", "number"), ("cyan", " = "), ("amber", "80.7"), ("fg", "; "), ("muted", "// >= 11:1 anti-halation")]),
            (None, [("fg", "  "), ("violet", "async"), ("fg", " "), ("blue", "reconcile"), ("fg", "("), ("amber", "pods"), ("cyan", ": "), ("gold", "PodState"), ("fg", "[]): "), ("gold", "Promise"), ("fg", "<"), ("gold", "BeaconStatus"), ("fg", "> {")]),
            (None, [("fg", "    "), ("violet", "const"), ("fg", " "), ("fg", "ready"), ("cyan", " = "), ("fg", "pods."), ("blue", "filter"), ("fg", "(("), ("amber", "p"), ("fg", ") "), ("cyan", "=>"), ("fg", " "), ("cyan", "!"), ("fg", "/^arkham-/.test("), ("fg", "p."), ("cyan", "name"), ("fg", "));")]),
            ("del", [("fg", "    "), ("violet", "if"), ("fg", " (ready."), ("cyan", "length"), ("cyan", " < "), ("amber", "3"), ("fg", ") "), ("violet", "throw new"), ("fg", " "), ("crimson", "SignalFault"), ("fg", "("), ("emerald", '"quorum lost"'), ("fg", ");")]),
            ("add", [("fg", "    "), ("violet", "return await"), ("fg", " "), ("blue", "syncSuite"), ("fg", "("), ("rose", "this"), ("fg", ".cfg, ready);")]),
            (None, [("fg", "  }")]),
            (None, [("fg", "}")]),
        ],
        "terminal_prompt": "zain@batcomputer ~/gotham-ops $ kubectl get pods -n gotham-ops && theme-sync year-one --all",
        "terminal_lines": [
            [("muted", "POD                       STATUS             READY   AGE")],
            [("fg", "bat-signal-ingress        "), ("emerald", "Running            "), ("fg", "2/2     14d")],
            [("fg", "oracle-telemetry-7c4f     "), ("emerald", "Running            "), ("fg", "1/1     09d")],
            [("fg", "arkham-ward-proxy         "), ("crimson", "CrashLoopBackOff   "), ("fg", "0/1     03m")],
            [("gold", "[OK] Synchronized 16 targets -> Gotham Noir - Year One (#15171A | Lc 80.7)")],
        ],
    },
    "gotham-noir-batcomputer": {
        "filename": "oracle_pipeline.py",
        "language": "Python 3.13 + MLOps",
        "active_line": 4,
        "code": [
            (None, [("muted", "# batcomputer // OLED Telemetry & Agent Evaluation Pipeline")]),
            (None, [("violet", "from"), ("fg", " dataclasses "), ("violet", "import"), ("fg", " dataclass")]),
            (None, [("violet", "@dataclass"), ("fg", "(frozen="), ("amber", "True"), ("fg", ")")]),
            ("add", [("violet", "class"), ("fg", " "), ("gold", "AgentTrace"), ("fg", ": "), ("cyan", "node"), ("cyan", ": "), ("gold", "str"), ("fg", "; "), ("cyan", "apca_lc"), ("cyan", ": "), ("gold", "float"), ("cyan", " = "), ("amber", "87.0")]),
            (None, [("violet", "async def"), ("fg", " "), ("blue", "dispatch_eval"), ("fg", "("), ("amber", "batch"), ("cyan", ": "), ("gold", "list"), ("fg", "[AgentTrace]) -> "), ("gold", "dict"), ("fg", "[str, float]:")]),
            (None, [("fg", "    "), ("violet", "if not"), ("fg", " batch: "), ("violet", "raise"), ("fg", " "), ("crimson", "ValueError"), ("fg", "("), ("emerald", '"empty telemetry batch"'), ("fg", ")")]),
            ("mod", [("fg", "    active "), ("cyan", "="), ("fg", " [t."), ("cyan", "apca_lc"), ("fg", " "), ("violet", "for"), ("fg", " t "), ("violet", "in"), ("fg", " batch "), ("violet", "if"), ("fg", " t."), ("cyan", "apca_lc"), ("cyan", " >= "), ("amber", "75.0"), ("fg", "]")]),
            (None, [("fg", "    "), ("violet", "return"), ("fg", " {"), ("emerald", '"nodes"'), ("cyan", ": "), ("blue", "float"), ("fg", "("), ("blue", "len"), ("fg", "(active)), "), ("emerald", '"min_lc"'), ("cyan", ": "), ("blue", "min"), ("fg", "(active)}")]),
            (None, []),
            (None, [("muted", "# Verified: 14.15:1 WCAG contrast on #101215 OLED obsidian ground")]),
            (None, [("fg", "result "), ("cyan", "="), ("fg", " "), ("violet", "await"), ("fg", " "), ("blue", "dispatch_eval"), ("fg", "([AgentTrace("), ("emerald", '"gcpd-04"'), ("fg", ", "), ("amber", "87.0"), ("fg", ")])")]),
        ],
        "terminal_prompt": "zain@batcomputer ~/ml-eval $ pytest -q tests/test_oracle.py && kubectl logs deploy/oracle-eval --tail=2",
        "terminal_lines": [
            [("emerald", "18 passed in 0.42s"), ("fg", "  |  APCA guard: Lc 87.0  |  R/G sep: 148.2deg")],
            [("fg", "2026-11-23T17:04Z "), ("gold", "INFO  "), ("fg", "oracle.eval: batch converged (latency_ms=11.4)")],
            [("fg", "2026-11-23T17:04Z "), ("crimson", "WARN  "), ("fg", "arkham-shard-02: retry budget 1/3")],
            [("gold", "[OK] Gotham Noir - Batcomputer active (#101215 OLED Obsidian)")],
        ],
    },
    "gotham-noir-arkham-slate": {
        "filename": "arkham_mesh.rs",
        "language": "Rust + Terraform HCL",
        "active_line": 3,
        "code": [
            (None, [("muted", "// arkham-slate // Zero-Glare Late-Night Infrastructure Mesh")]),
            (None, [("violet", "#[derive("), ("gold", "Debug"), ("fg", ", "), ("gold", "Clone"), ("violet", ")]")]),
            ("add", [("violet", "pub struct"), ("fg", " "), ("gold", "WatchtowerSpec"), ("fg", "<'a> { "), ("violet", "pub"), ("fg", " "), ("cyan", "zone"), ("cyan", ": &"), ("gold", "'a str"), ("fg", ", "), ("violet", "pub"), ("fg", " "), ("cyan", "replicas"), ("cyan", ": "), ("gold", "u8"), ("fg", " }")]),
            (None, [("violet", "pub fn"), ("fg", " "), ("blue", "plan_reconcile"), ("fg", "("), ("amber", "spec"), ("cyan", ": &"), ("gold", "WatchtowerSpec"), ("fg", ") -> "), ("gold", "Result"), ("fg", "<"), ("gold", "u8"), ("fg", ", &'static "), ("gold", "str"), ("fg", "> {")]),
            (None, [("fg", "    "), ("violet", "if"), ("fg", " spec."), ("cyan", "replicas"), ("cyan", " < "), ("amber", "2"), ("fg", " { "), ("violet", "return"), ("fg", " "), ("crimson", "Err"), ("fg", "("), ("emerald", '"ha quorum requires >= 2"'), ("fg", "); }")]),
            ("mod", [("fg", "    "), ("blue", "println!"), ("fg", "("), ("emerald", '"reconciling zone={} nodes={}"'), ("fg", ", spec."), ("cyan", "zone"), ("fg", ", spec."), ("cyan", "replicas"), ("fg", ");")]),
            (None, [("fg", "    "), ("emerald", "Ok"), ("fg", "(spec."), ("cyan", "replicas"), ("fg", ")")]),
            (None, [("fg", "}")]),
            (None, []),
            (None, [("muted", "# infra/watchtower.tf: module \"gotham_edge\" { min_wcag = 11.28 }")]),
            (None, [("gold", "resource"), ("fg", " "), ("emerald", '"kubernetes_namespace_v1"'), ("fg", " "), ("emerald", '"arkham"'), ("fg", " { "), ("cyan", "name"), ("cyan", " = "), ("emerald", '"arkham-slate"'), ("fg", " }")]),
        ],
        "terminal_prompt": "zain@watchtower ~/infra $ terraform plan -no-color && cargo test -q",
        "terminal_lines": [
            [("emerald", "  + resource \"kubernetes_namespace_v1\" \"arkham\" { metadata.name = \"arkham-slate\" }")],
            [("gold", "  ~ module.gotham_edge.service: replicas = 2 -> 3")],
            [("crimson", "  - deprecated_ingress_rule: port 80 disabled")],
            [("gold", "Plan: 1 to add, 1 to change, 1 to destroy. | cargo test: 12 passed")],
        ],
    },
    "gotham-noir-vengeance": {
        "filename": "sentinel_proxy.go",
        "language": "Go 1.24 + Git Diff",
        "active_line": 4,
        "code": [
            (None, [("muted", "// vengeance // High-Visibility Edge Proxy + Git Diff Verification")]),
            (None, [("violet", "package"), ("fg", " sentinel")]),
            (None, [("violet", "type"), ("fg", " "), ("gold", "FlareGate"), ("fg", " "), ("violet", "struct"), ("fg", " { "), ("cyan", "ThresholdMs"), ("fg", " "), ("gold", "int"), ("fg", "; "), ("cyan", "CrimsonAlert"), ("fg", " "), ("gold", "bool"), ("fg", " }")]),
            ("add", [("violet", "func"), ("fg", " (g "), ("gold", "FlareGate"), ("fg", ") "), ("blue", "Verify"), ("fg", "("), ("amber", "latency"), ("fg", " "), ("gold", "int"), ("fg", ") "), ("gold", "error"), ("fg", " {")]),
            (None, [("fg", "    "), ("violet", "if"), ("fg", " latency "), ("cyan", ">"), ("fg", " g."), ("cyan", "ThresholdMs"), ("fg", " {")]),
            ("del", [("fg", "        "), ("violet", "return"), ("fg", " fmt."), ("blue", "Errorf"), ("fg", "("), ("emerald", '"edge spike %dms"'), ("fg", ", latency)")]),
            ("add", [("fg", "        "), ("violet", "return"), ("fg", " fmt."), ("blue", "Errorf"), ("fg", "("), ("emerald", '"critical alert %dms > %dms"'), ("fg", ", latency, g."), ("cyan", "ThresholdMs"), ("fg", ")  "), ("muted", "// #E5535C")]),
            (None, [("fg", "    }")]),
            (None, [("fg", "    "), ("violet", "return"), ("fg", " "), ("amber", "nil")]),
            (None, [("fg", "}")]),
            (None, [("muted", "// Circular red/green ANSI separation verified across all 16 slots")]),
        ],
        "terminal_prompt": "zain@gcpd-edge ~/proxy $ git diff --stat && go test ./... -v",
        "terminal_lines": [
            [("fg", " proxy/sentinel_proxy.go | 6 "), ("emerald", "++++"), ("crimson", "--")],
            [("emerald", "PASS"), ("fg", " TestFlareGateThreshold (0.01s)  |  "), ("emerald", "PASS"), ("fg", " TestDiffContrast")],
            [("crimson", "--- FAIL legacy_route_timeout: deprecated fallback removed in commit 9c4e")],
            [("gold", "[OK] Gotham Noir - Vengeance (#151417 Night Chrome | #E5535C Flare)")],
        ],
    },
}

COMPACT_SPLIT_CODE: dict[str, tuple[str, list[list[TokenRun]]]] = {
    "gotham-noir-year-one": (
        "bat-signal.ts (TS + K8s)",
        [
            [("violet", "@KubeController"), ("fg", "("), ("emerald", '"gotham-ops"'), ("fg", ")")],
            [("violet", "class"), ("fg", " "), ("gold", "WayneOperator"), ("fg", " {")],
            [("fg", "  "), ("cyan", "lc"), ("cyan", ": "), ("gold", "number"), ("cyan", " = "), ("amber", "80.7"), ("fg", ";")],
            [("fg", "  "), ("violet", "async"), ("fg", " "), ("blue", "reconcile"), ("fg", "(p) {")],
            [("fg", "    "), ("violet", "if"), ("fg", " (!ok) "), ("crimson", "SignalFault"), ("fg", "();")],
            [("fg", "    "), ("violet", "return"), ("fg", " "), ("blue", "sync"), ("fg", "("), ("rose", "this"), ("fg", ");")],
            [("fg", "  }")],
            [("fg", "}")],
        ],
    ),
    "gotham-noir-batcomputer": (
        "oracle_eval.py (Python)",
        [
            [("violet", "@dataclass"), ("fg", "(frozen="), ("amber", "True"), ("fg", ")")],
            [("violet", "class"), ("fg", " "), ("gold", "AgentTrace"), ("fg", ":")],
            [("fg", "  "), ("cyan", "node"), ("cyan", ": "), ("gold", "str"), ("fg", "; "), ("cyan", "lc"), ("cyan", "="), ("amber", "87.0")],
            [("violet", "async def"), ("fg", " "), ("blue", "run"), ("fg", "(b):")],
            [("fg", "  "), ("violet", "if not"), ("fg", " b: "), ("crimson", "raise"), ("fg", " "), ("emerald", '"err"')],
            [("fg", "  s "), ("cyan", "="), ("fg", " [x "), ("violet", "for"), ("fg", " x "), ("violet", "in"), ("fg", " b]")],
            [("fg", "  "), ("violet", "return"), ("fg", " "), ("blue", "score"), ("fg", "(s)")],
            [("muted", "# 14.15:1 OLED contrast")],
        ],
    ),
    "gotham-noir-arkham-slate": (
        "arkham.rs (Rust + HCL)",
        [
            [("violet", "#[derive("), ("gold", "Debug"), ("violet", ")]")],
            [("violet", "struct"), ("fg", " "), ("gold", "MeshSpec"), ("fg", "<'a> {")],
            [("fg", "  "), ("cyan", "zone"), ("cyan", ": &"), ("gold", "'a str"), ("fg", ",")],
            [("fg", "  "), ("cyan", "nodes"), ("cyan", ": "), ("gold", "u8"), ("fg", ",")],
            [("fg", "}")],
            [("violet", "fn"), ("fg", " "), ("blue", "plan"), ("fg", "(n: "), ("gold", "u8"), ("fg", ") -> "), ("gold", "Result"), ("fg", " {")],
            [("fg", "  "), ("violet", "if"), ("fg", " n<"), ("amber", "2"), ("fg", " { "), ("crimson", "Err"), ("fg", "("), ("emerald", '"min"'), ("fg", ") }")],
            [("fg", "  "), ("blue", "println!"), ("fg", "("), ("emerald", '"zone={}"'), ("fg", ") }")],
        ],
    ),
    "gotham-noir-vengeance": (
        "proxy.go (Go + Diff)",
        [
            [("violet", "package"), ("fg", " sentinel")],
            [("violet", "type"), ("fg", " "), ("gold", "Gate"), ("fg", " "), ("violet", "struct"), ("fg", " {")],
            [("fg", "  "), ("cyan", "ms"), ("fg", " "), ("gold", "int"), ("fg", "; "), ("cyan", "alert"), ("fg", " "), ("gold", "bool")],
            [("fg", "}")],
            [("violet", "func"), ("fg", " (g "), ("gold", "Gate"), ("fg", ") "), ("blue", "Check"), ("fg", "() {")],
            [("fg", "  "), ("violet", "if"), ("fg", " g."), ("cyan", "ms"), ("cyan", ">"), ("amber", "50"), ("fg", " {")],
            [("fg", "    "), ("violet", "return"), ("fg", " "), ("crimson", "Err"), ("fg", "("), ("emerald", '"spike"'), ("fg", ")")],
            [("fg", "  } "), ("violet", "return"), ("fg", " "), ("amber", "nil"), ("fg", " }")],
        ],
    ),
}


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


def _draw_ansi_tokens(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    tokens: list[tuple[str, str]],
    pal: dict,
    font_reg: ImageFont.FreeTypeFont | ImageFont.ImageFont,
) -> None:
    ui = pal["ui"]
    syn = pal["syntax"]
    cx = x
    for role, text in tokens:
        color = ui["fg"] if role == "fg" else syn.get(role, ui["fgMuted"])
        draw.text((cx, y), text, fill=_hex_rgba(color), font=font_reg)
        bbox = draw.textbbox((cx, y), text, font=font_reg)
        cx = bbox[2]


def generate_code_window_png(pal: dict, out_path: Path) -> None:
    """Render a 1600x960 multi-pane IDE + integrated Ghostty terminal specimen screenshot."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    w, h = 1600, 960
    ui = pal["ui"]
    syn = pal["syntax"]
    ansi = pal["ansi"]
    scene = VARIANT_SCENES[pal["id"]]

    fg_wcag = wcag_contrast(ui["fg"], ui["bg"])
    fg_apca = abs(apca_contrast(ui["fg"], ui["bg"]))

    img = Image.new("RGBA", (w, h), _hex_rgba(ui["bgDeep"]))
    draw = ImageDraw.Draw(img)

    title_font = _load_font(16, bold=True)
    ui_font = _load_font(14, bold=False)
    ui_bold = _load_font(14, bold=True)
    code_font = _load_font(18, bold=False)
    ital_font = _load_font(18, italic=True)
    term_font = _load_font(16, bold=False)
    small_font = _load_font(14, bold=False)

    # Outer frame
    m = 24
    wx0, wy0, wx1, wy1 = m, m, w - m, h - m
    draw.rounded_rectangle(
        [wx0, wy0, wx1, wy1],
        radius=16,
        fill=_hex_rgba(ui["bg"]),
        outline=_hex_rgba(ui["border"]),
        width=2,
    )

    # Title bar
    tb_h = 50
    draw.rounded_rectangle([wx0 + 2, wy0 + 2, wx1 - 2, wy0 + tb_h], radius=14, fill=_hex_rgba(ui["bgSide"]))
    draw.rectangle([wx0 + 2, wy0 + 30, wx1 - 2, wy0 + tb_h], fill=_hex_rgba(ui["bgSide"]))
    draw.line([(wx0 + 2, wy0 + tb_h), (wx1 - 2, wy0 + tb_h)], fill=_hex_rgba(ui["borderSubtle"]), width=1)

    for idx, dcol in enumerate((ansi["red"], syn["gold"], syn["emerald"])):
        dx = wx0 + 26 + idx * 22
        dy = wy0 + tb_h // 2
        draw.ellipse([dx - 6, dy - 6, dx + 6, dy + 6], fill=_hex_rgba(dcol))

    title = f"{scene['filename']}  -  {pal['name']}"
    tb_box = draw.textbbox((0, 0), title, font=title_font)
    draw.text(((w - (tb_box[2] - tb_box[0])) // 2, wy0 + 16), title, fill=_hex_rgba(ui["fgStrong"]), font=title_font)

    badge_txt = f"{scene['language']}  |  Lc {fg_apca:.1f}"
    bb = draw.textbbox((0, 0), badge_txt, font=small_font)
    bw = bb[2] - bb[0] + 22
    bx0, by0, bx1, by1 = wx1 - bw - 18, wy0 + 12, wx1 - 18, wy0 + 38
    draw.rounded_rectangle([bx0, by0, bx1, by1], radius=8, fill=_hex_rgba(ui["surface"]), outline=_hex_rgba(ui["border"]), width=1)
    draw.text((bx0 + 11, by0 + 5), badge_txt, fill=_hex_rgba(ui["accent"]), font=small_font)

    # Status bar bottom geometry
    sb_h = 42
    sb_y = wy1 - sb_h
    draw.rectangle([wx0 + 2, sb_y, wx1 - 2, wy1 - 2], fill=_hex_rgba(ui["bgSide"]))
    draw.line([(wx0 + 2, sb_y), (wx1 - 2, sb_y)], fill=_hex_rgba(ui["borderSubtle"]), width=1)

    # Left Explorer Sidebar
    side_w = 272
    side_x1 = wx0 + side_w
    draw.rectangle([wx0 + 2, wy0 + tb_h + 1, side_x1, sb_y - 1], fill=_hex_rgba(ui["bgSide"]))
    draw.line([(side_x1, wy0 + tb_h + 1), (side_x1, sb_y - 1)], fill=_hex_rgba(ui["borderSubtle"]), width=1)

    draw.text((wx0 + 20, wy0 + tb_h + 18), "WORKSPACE // GOTHAM-OPS", fill=_hex_rgba(ui["fgMuted"]), font=ui_bold)

    tree_files = [
        ("operator/", None, 0),
        ("bat-signal-operator.ts", syn["gold"], 1),
        ("ml/", None, 0),
        ("oracle_pipeline.py", syn["blue"], 1),
        ("infra/", None, 0),
        ("arkham_mesh.rs", syn["amber"], 1),
        ("main.tf", syn["violet"], 1),
        ("proxy/", None, 0),
        ("sentinel_proxy.go", syn["cyan"], 1),
        ("k8s/", None, 0),
        ("deployment.yaml", syn["emerald"], 1),
    ]
    ty = wy0 + tb_h + 52
    for label, dot_col, indent in tree_files:
        is_cur = label == scene["filename"]
        if is_cur:
            draw.rectangle([wx0 + 8, ty - 5, side_x1 - 8, ty + 23], fill=_hex_rgba(ui["selectionBg"]))
            draw.rectangle([wx0 + 8, ty - 5, wx0 + 11, ty + 23], fill=_hex_rgba(ui["accent"]))
        lx = wx0 + 22 + indent * 16
        if dot_col:
            draw.ellipse([lx, ty + 5, lx + 8, ty + 13], fill=_hex_rgba(dot_col))
            lx += 15
        text_col = ui["fgStrong"] if is_cur else (ui["fg"] if dot_col else ui["fgMuted"])
        draw.text((lx, ty), label, fill=_hex_rgba(text_col), font=ui_bold if is_cur else ui_font)
        ty += 31

    # Editor tab strip
    ed_x0 = side_x1 + 1
    ed_y0 = wy0 + tb_h + 1
    tab_h = 38
    draw.rectangle([ed_x0, ed_y0, wx1 - 2, ed_y0 + tab_h], fill=_hex_rgba(ui["bgSide"]))
    draw.line([(ed_x0, ed_y0 + tab_h), (wx1 - 2, ed_y0 + tab_h)], fill=_hex_rgba(ui["borderSubtle"]), width=1)
    draw.rectangle([ed_x0, ed_y0, ed_x0 + 240, ed_y0 + tab_h], fill=_hex_rgba(ui["bg"]))
    draw.line([(ed_x0, ed_y0), (ed_x0 + 240, ed_y0)], fill=_hex_rgba(ui["accent"]), width=3)
    draw.text((ed_x0 + 18, ed_y0 + 10), scene["filename"], fill=_hex_rgba(ui["fgStrong"]), font=ui_bold)

    # Code area + integrated terminal split
    term_h = 248
    term_y0 = sb_y - term_h
    code_y0 = ed_y0 + tab_h + 22
    line_h = 40
    active_idx = scene["active_line"] - 1

    ay0 = code_y0 + active_idx * line_h - 6
    draw.rectangle([ed_x0, ay0, wx1 - 2, ay0 + line_h], fill=_hex_rgba(ui["lineHighlightBg"]))

    for idx, (git_kind, tokens) in enumerate(scene["code"]):
        ly = code_y0 + idx * line_h
        if git_kind == "add":
            draw.rectangle([ed_x0 + 8, ly - 2, ed_x0 + 11, ly + 26], fill=_hex_rgba(syn["emerald"]))
        elif git_kind == "mod":
            draw.rectangle([ed_x0 + 8, ly - 2, ed_x0 + 11, ly + 26], fill=_hex_rgba(syn["blue"]))
        elif git_kind == "del":
            draw.rectangle([ed_x0 + 8, ly - 2, ed_x0 + 11, ly + 26], fill=_hex_rgba(syn["crimson"]))

        lcol = ui["accent"] if idx == active_idx else ui["gutterFg"]
        draw.text((ed_x0 + 24, ly), f"{idx + 1:>2}", fill=_hex_rgba(lcol), font=code_font)
        if tokens:
            _draw_code_tokens(draw, ed_x0 + 70, ly, tokens, pal, code_font, ital_font)

    # Integrated Terminal Pane
    draw.rectangle([ed_x0, term_y0, wx1 - 2, sb_y - 1], fill=_hex_rgba(ui["bgDeep"]))
    draw.line([(ed_x0, term_y0), (wx1 - 2, term_y0)], fill=_hex_rgba(ui["border"]), width=2)
    draw.rectangle([ed_x0, term_y0 + 1, wx1 - 2, term_y0 + 36], fill=_hex_rgba(ui["bgSide"]))
    draw.line([(ed_x0, term_y0 + 36), (wx1 - 2, term_y0 + 36)], fill=_hex_rgba(ui["borderSubtle"]), width=1)
    draw.text((ed_x0 + 18, term_y0 + 10), "TERMINAL  //  ghostty  |  16 ANSI OKLCH", fill=_hex_rgba(ui["fgStrong"]), font=ui_bold)

    # 16 ANSI swatches in terminal header
    ansi_keys = [
        "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white",
        "brightBlack", "brightRed", "brightGreen", "brightYellow", "brightBlue", "brightMagenta", "brightCyan", "brightWhite",
    ]
    for ai, akey in enumerate(ansi_keys):
        sx = wx1 - 24 - (16 - ai) * 16
        draw.rounded_rectangle([sx, term_y0 + 12, sx + 11, term_y0 + 24], radius=3, fill=_hex_rgba(ansi[akey]))

    py = term_y0 + 50
    draw.text((ed_x0 + 20, py), scene["terminal_prompt"], fill=_hex_rgba(syn["cyan"]), font=term_font)
    py += 34
    for runs in scene["terminal_lines"]:
        _draw_ansi_tokens(draw, ed_x0 + 20, py, runs, pal, term_font)
        py += 32

    # Bottom status bar
    draw.text(
        (wx0 + 22, sb_y + 13),
        f"{pal['name']}   |   Canvas {ui['bg']}   |   Text {ui['fg']}   |   Accent {ui['accent']}   |   WCAG {fg_wcag:.2f}:1   |   APCA Lc {fg_apca:.1f}",
        fill=_hex_rgba(ui["fgMuted"]),
        font=small_font,
    )
    sw_keys = ["gold", "blue", "emerald", "cyan", "amber", "violet", "crimson", "rose"]
    for i, k in enumerate(sw_keys):
        sx = wx1 - 24 - (len(sw_keys) - i) * 24
        draw.rounded_rectangle([sx, sb_y + 13, sx + 16, sb_y + 29], radius=4, fill=_hex_rgba(syn[k]))

    img.save(out_path, format="PNG", optimize=True)


def generate_split_hero_png(palettes: list[dict], out_path: Path) -> None:
    """Render 1600x920 4-column studio hero showcasing all four Gotham Noir atmospheres side-by-side."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    w, h = 1600, 920
    img = Image.new("RGBA", (w, h), _hex_rgba("#0C0E11"))
    draw = ImageDraw.Draw(img)

    hdr_font = _load_font(28, bold=True)
    sub_font = _load_font(16, bold=False)
    col_title_font = _load_font(18, bold=True)
    meta_font = _load_font(13, bold=False)
    file_font = _load_font(13, bold=True)
    code_font = _load_font(13, bold=False)
    ital_font = _load_font(13, italic=True)

    draw.text((40, 26), "GOTHAM NOIR", fill=_hex_rgba("#F0C946"), font=hdr_font)
    draw.text((248, 28), "Darkness, engineered for developers.", fill=_hex_rgba("#ECEAE4"), font=hdr_font)
    draw.text(
        (40, 66),
        "One identity. Four atmospheres. OKLCH perceptual balance + APCA contrast across TypeScript, Python, Rust, Go & K8s.",
        fill=_hex_rgba("#878D96"),
        font=sub_font,
    )

    margin_x = 40
    top_y = 108
    gap = 16
    card_w = (w - 2 * margin_x - 3 * gap) // 4
    card_h = h - top_y - 36
    swatch_keys = ["gold", "blue", "emerald", "cyan", "amber", "violet", "crimson", "rose"]

    for idx, pal in enumerate(palettes[:4]):
        x0 = margin_x + idx * (card_w + gap)
        y0 = top_y
        x1 = x0 + card_w
        y1 = y0 + card_h
        ui = pal["ui"]
        syn = pal["syntax"]
        fg_wcag = wcag_contrast(ui["fg"], ui["bg"])
        fg_apca = abs(apca_contrast(ui["fg"], ui["bg"]))

        draw.rounded_rectangle(
            [x0, y0, x1, y1],
            radius=14,
            fill=_hex_rgba(ui["bg"]),
            outline=_hex_rgba(ui["border"]),
            width=2,
        )
        # Card top accent rule
        draw.line([(x0 + 16, y0 + 2), (x1 - 16, y0 + 2)], fill=_hex_rgba(ui["accent"]), width=3)

        # Header band
        draw.rectangle([x0 + 2, y0 + 4, x1 - 2, y0 + 84], fill=_hex_rgba(ui["bgSide"]))
        draw.line([(x0 + 2, y0 + 84), (x1 - 2, y0 + 84)], fill=_hex_rgba(ui["borderSubtle"]), width=1)
        draw.text((x0 + 18, y0 + 16), pal["shortName"], fill=_hex_rgba(ui["fgStrong"]), font=col_title_font)
        draw.text(
            (x0 + 18, y0 + 42),
            pal["lore"]["protocol"],
            fill=_hex_rgba(ui["accent"]),
            font=meta_font,
        )
        draw.text(
            (x0 + 18, y0 + 62),
            f"bg {ui['bg']} | Lc {fg_apca:.1f} | {fg_wcag:.1f}:1",
            fill=_hex_rgba(ui["fgMuted"]),
            font=meta_font,
        )

        # Recessed code well
        fname, code_rows = COMPACT_SPLIT_CODE[pal["id"]]
        well_x0, well_y0, well_x1, well_y1 = x0 + 14, y0 + 102, x1 - 14, y1 - 126
        draw.rounded_rectangle(
            [well_x0, well_y0, well_x1, well_y1],
            radius=10,
            fill=_hex_rgba(ui["bgDeep"]),
            outline=_hex_rgba(ui["borderSubtle"]),
            width=1,
        )
        draw.text((well_x0 + 14, well_y0 + 14), fname, fill=_hex_rgba(ui["fgMuted"]), font=file_font)
        draw.line([(well_x0 + 10, well_y0 + 38), (well_x1 - 10, well_y0 + 38)], fill=_hex_rgba(ui["borderSubtle"]), width=1)

        cy = well_y0 + 54
        for li, runs in enumerate(code_rows):
            lcol = ui["accent"] if li == 3 else ui["gutterFg"]
            draw.text((well_x0 + 12, cy), f"{li + 1}", fill=_hex_rgba(lcol), font=code_font)
            _draw_code_tokens(draw, well_x0 + 32, cy, runs, pal, code_font, ital_font)
            cy += 48

        # Contrast readout + 8 syntax chips
        draw.text(
            (x0 + 18, y1 - 104),
            f"fg {ui['fg']}  |  accent {ui['accent']}",
            fill=_hex_rgba(ui["fg"]),
            font=meta_font,
        )
        sw_y = y1 - 68
        sw_x = x0 + 16
        sw_w = (card_w - 32 - (len(swatch_keys) - 1) * 6) // len(swatch_keys)
        for si, skey in enumerate(swatch_keys):
            sx0 = sw_x + si * (sw_w + 6)
            draw.rounded_rectangle([sx0, sw_y, sx0 + sw_w, sw_y + 34], radius=5, fill=_hex_rgba(syn[skey]))

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

    syntax_keys = ["gold", "blue", "emerald", "cyan", "amber", "violet", "crimson", "rose"]

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
        draw.rounded_rectangle([x0 + 2, y0 + 2, x1 - 2, y0 + 54], radius=12, fill=_hex_rgba(ui["bgSide"]))
        draw.rectangle([x0 + 2, y0 + 38, x1 - 2, y0 + 54], fill=_hex_rgba(ui["bgSide"]))
        draw.line([(x0 + 2, y0 + 54), (x1 - 2, y0 + 54)], fill=_hex_rgba(ui["borderSubtle"]), width=1)

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

        code_y = y0 + 72
        line_step = 28
        _, code_rows = COMPACT_SPLIT_CODE[pal["id"]]
        for li, tokens in enumerate(code_rows):
            cy = code_y + li * line_step
            lcol = ui["accent"] if li == 3 else ui["gutterFg"]
            draw.text((x0 + 20, cy), f"{li + 1:>2}", fill=_hex_rgba(lcol), font=code_font)
            _draw_code_tokens(draw, x0 + 52, cy, tokens, pal, code_font, ital_font)

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
