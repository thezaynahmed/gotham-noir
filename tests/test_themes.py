"""Comprehensive validation tests for Gotham Noir lore palettes and generated ports."""

from __future__ import annotations

import json
import plistlib
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from build import load_palettes
from contrast import verify_palette

EXPECTED_NAMES = [
    "Gotham Noir - Year One",
    "Gotham Noir - Batcomputer",
    "Gotham Noir - Arkham Slate",
    "Gotham Noir - Vengeance",
]


class GothamNoirTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.palettes = load_palettes(ROOT / "palettes")

    def test_lore_metadata_and_no_stale_files(self) -> None:
        self.assertEqual([p["name"] for p in self.palettes], EXPECTED_NAMES)
        for pal in self.palettes:
            lore = pal.get("lore", {})
            for key in ("era", "reference", "protocol", "quote"):
                self.assertTrue(lore.get(key), f"{pal['name']} missing lore.{key}")
            token_lore = pal.get("tokenLore", {})
            for key in ("gold", "blue", "emerald", "cyan", "amber", "violet", "crimson", "rose"):
                self.assertTrue(token_lore.get(key), f"{pal['name']} missing tokenLore.{key}")

        # Ensure old un-lored filenames were purged
        self.assertFalse((ROOT / "ports" / "ghostty" / "Gotham Noir").exists())
        self.assertFalse((ROOT / "ports" / "ghostty" / "Gotham Noir Obsidian").exists())
        self.assertFalse((ROOT / "packages" / "vscode" / "themes" / "gotham-noir-color-theme.json").exists())

    def test_contrast_and_color_science_gates(self) -> None:
        for pal in self.palettes:
            with self.subTest(variant=pal["name"]):
                report = verify_palette(pal)
                self.assertEqual(len(report), 1)

    def test_vscode_package_and_themes_are_valid(self) -> None:
        pkg_path = ROOT / "packages" / "vscode" / "package.json"
        pkg = json.loads(pkg_path.read_text(encoding="utf-8"))
        self.assertEqual(pkg["name"], "gotham-noir")
        self.assertFalse(pkg["name"].startswith("@"))
        self.assertTrue(pkg["icon"].endswith(".png"))
        self.assertNotIn(".svg", pkg_path.read_text(encoding="utf-8").lower())

        readme = (ROOT / "packages" / "vscode" / "README.md").read_text(encoding="utf-8")
        self.assertNotIn(".svg", readme.lower())

        labels = [entry["label"] for entry in pkg["contributes"]["themes"]]
        self.assertEqual(labels, EXPECTED_NAMES)

        for entry in pkg["contributes"]["themes"]:
            theme_path = ROOT / "packages" / "vscode" / entry["path"]
            self.assertTrue(theme_path.exists(), f"Missing {theme_path}")
            data = json.loads(theme_path.read_text(encoding="utf-8"))
            self.assertTrue(data["semanticHighlighting"])
            colors = data["colors"]
            for idx in range(1, 7):
                self.assertIn(f"editorBracketHighlight.foreground{idx}", colors)
                self.assertIn(f"editorBracketPairGuide.activeBackground{idx}", colors)
            for req in (
                "inlineChat.background",
                "inlineChatDiff.inserted",
                "inlineChatDiff.removed",
                "chat.requestBackground",
                "agentsChatInput.placeholderForeground",
                "editorGhostText.foreground",
                "editorStickyScroll.background",
                "editorInlayHint.background",
                "terminalCommandDecoration.successBackground",
                "terminalCommandDecoration.errorBackground",
            ):
                self.assertIn(req, colors, f"Missing 2027 token {req}")

            self.assertNotEqual(
                colors["notificationsErrorIcon.foreground"],
                colors["notificationsWarningIcon.foreground"],
            )
            self.assertNotEqual(
                colors["notificationsWarningIcon.foreground"],
                colors["notificationsInfoIcon.foreground"],
            )
            self.assertNotEqual(colors["editorError.foreground"], colors["diffEditor.insertedTextBackground"][:7])

            token_names = " | ".join(r.get("name", "") for r in data["tokenColors"])
            for lore_label in ("GCPD Signal", "Detective Mode", "Oracle Emerald", "Cryo Sonar", "Ace Chemicals Violet"):
                self.assertIn(lore_label, token_names)

            for rule in data["tokenColors"]:
                scopes = rule["scope"] if isinstance(rule["scope"], list) else [rule["scope"]]
                for s in scopes:
                    self.assertEqual(s, s.strip(), f"Whitespace in scope: {s!r}")

    def test_zed_schema_v020_compliance(self) -> None:
        self.assertTrue((ROOT / "packages" / "zed" / "LICENSE").exists(), "Missing packages/zed/LICENSE")
        zed_path = ROOT / "packages" / "zed" / "themes" / "gotham-noir.json"
        zed = json.loads(zed_path.read_text(encoding="utf-8"))
        self.assertEqual(zed["$schema"], "https://zed.dev/schema/themes/v0.2.0.json")
        self.assertEqual([t["name"] for t in zed["themes"]], EXPECTED_NAMES)
        hex8_re = re.compile(r"^#[0-9a-f]{8}$")
        for t in zed["themes"]:
            self.assertEqual(t["appearance"], "dark")
            st = t["style"]
            self.assertGreaterEqual(len(st["players"]), 6)
            for k in ("syntax", "players"):
                self.assertIn(k, st)
            for k, v in st.items():
                if isinstance(v, str):
                    self.assertRegex(v, hex8_re, f"{t['name']} style.{k} must be #rrggbbaa")
            for ansi_key in (
                "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white",
                "bright_black", "bright_red", "bright_green", "bright_yellow",
                "bright_blue", "bright_magenta", "bright_cyan", "bright_white",
            ):
                self.assertIn(f"terminal.ansi.{ansi_key}", st)

    def test_toml_json_yaml_and_plist_ports(self) -> None:
        for pal in self.palettes:
            tomllib.loads((ROOT / "ports" / "alacritty" / f"{pal['slug']}.toml").read_text(encoding="utf-8"))
            tomllib.loads((ROOT / "ports" / "wezterm" / f"{pal['name']}.toml").read_text(encoding="utf-8"))
            warp_text = (ROOT / "ports" / "warp" / f"{pal['warpSlug']}.yaml").read_text(encoding="utf-8")
            self.assertIn(f"name: \"{pal['name']}\"", warp_text)
            self.assertIn("details: darker", warp_text)

            iterm_bytes = (ROOT / "ports" / "iterm2" / f"{pal['itermName']}.itermcolors").read_bytes()
            iterm_pl = plistlib.loads(iterm_bytes)
            self.assertIn("Background Color", iterm_pl)
            self.assertIn("Ansi 15 Color", iterm_pl)

            term_bytes = (ROOT / "ports" / "macos-terminal" / f"{pal['name']}.terminal").read_bytes()
            term_pl = plistlib.loads(term_bytes)
            self.assertEqual(term_pl["name"], pal["name"])
            for k in ("BackgroundColor", "TextColor", "CursorColor", "ANSIRedColor", "ANSIGreenColor", "Font"):
                decoded = plistlib.loads(term_pl[k])
                self.assertEqual(decoded["$archiver"], "NSKeyedArchiver")

        tomllib.loads((ROOT / "ports" / "alacritty" / "alacritty.toml").read_text(encoding="utf-8"))
        json.loads((ROOT / "ports" / "windows-terminal" / "gotham-noir-schemes.json").read_text(encoding="utf-8"))
        json.loads((ROOT / "ports" / "iterm2" / "gotham-noir-dynamic-profiles.json").read_text(encoding="utf-8"))

        paradev_doc = json.loads((ROOT / "ports" / "paradev" / "gotham-noir-themes.json").read_text(encoding="utf-8"))
        self.assertEqual([t["name"] for t in paradev_doc["themes"]], EXPECTED_NAMES)
        req_ui = {
            "background", "foreground", "card", "cardForeground", "popover", "popoverForeground",
            "primary", "primaryForeground", "secondary", "secondaryForeground", "muted", "mutedForeground",
            "accent", "accentForeground", "tertiary", "tertiaryActive", "destructive", "destructiveForeground",
            "border", "input", "ring", "sidebar", "sidebarForeground", "sidebarPrimary",
            "sidebarPrimaryForeground", "sidebarAccent", "sidebarAccentForeground", "sidebarBorder",
            "sidebarRing", "chart1", "chart2", "chart3", "chart4", "chart5",
            "highlightMatch", "highlightActive",
        }
        req_term = {
            "background", "foreground", "cursor", "black", "red", "green", "yellow", "blue", "magenta",
            "cyan", "white", "brightBlack", "brightRed", "brightGreen", "brightYellow", "brightBlue",
            "brightMagenta", "brightCyan", "brightWhite",
        }
        for pt in paradev_doc["themes"]:
            self.assertEqual(pt["type"], "dark")
            self.assertTrue(req_ui.issubset(pt["ui"].keys()))
            self.assertTrue(req_term.issubset(pt["terminal"].keys()))

    @unittest.skipUnless(shutil.which("ghostty"), "ghostty CLI not available")
    def test_ghostty_validates_all_variants(self) -> None:
        for pal in self.palettes:
            theme_file = ROOT / "ports" / "ghostty" / pal["name"]
            self.assertTrue(theme_file.exists())
            with tempfile.NamedTemporaryFile("w", suffix=".conf", delete=False) as tf:
                tf.write(theme_file.read_text(encoding="utf-8"))
                tf_path = Path(tf.name)
            try:
                res = subprocess.run(
                    ["ghostty", "+validate-config", f"--config-file={tf_path}"],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(res.returncode, 0, f"Ghostty validation failed for {pal['name']}: {res.stderr}\n{res.stdout}")
            finally:
                tf_path.unlink(missing_ok=True)

    def test_fontconfig_xml_shell_wezterm_and_vsix_e2e(self) -> None:
        fc_xml = (ROOT / "ports" / "linux-fontconfig" / "70-gotham-noir-fonts.conf").read_text(encoding="utf-8")
        tree = ET.fromstring(fc_xml)
        self.assertEqual(tree.tag, "fontconfig")

        apply_sh = ROOT / "ports" / "macos-terminal" / "apply-macos-terminal.sh"
        subprocess.run(["bash", "-n", str(apply_sh)], check=True)
        if shutil.which("zsh"):
            subprocess.run(["zsh", "-n", str(ROOT / "ports" / "zsh" / "gotham-noir-zsh.zsh")], check=True)

        wez_lua = (ROOT / "ports" / "wezterm" / "wezterm.lua").read_text(encoding="utf-8")
        self.assertIn("#15171a", wez_lua)
        self.assertIn("#f0c946", wez_lua)

        vsix_path = ROOT / "packages" / "vscode" / "gotham-noir-1.0.0.vsix"
        if vsix_path.exists():
            with zipfile.ZipFile(vsix_path, "r") as zf:
                names = set(zf.namelist())
                self.assertIn("extension/package.json", names)
                self.assertIn("extension/images/icon.png", names)
                self.assertIn("extension/images/palette-preview.png", names)
                self.assertFalse(any(n.lower().endswith(".svg") for n in names))
                pkg = json.loads(zf.read("extension/package.json").decode("utf-8"))
                for entry in pkg["contributes"]["themes"]:
                    rel = entry["path"].lstrip("./")
                    full = f"extension/{rel}"
                    self.assertIn(full, names)
                    theme_doc = json.loads(zf.read(full).decode("utf-8"))
                    self.assertEqual(theme_doc["name"], entry["label"])

    def test_build_is_idempotent_for_text_outputs(self) -> None:
        targets = [
            ROOT / "packages" / "vscode" / "themes" / "gotham-noir-year-one-color-theme.json",
            ROOT / "packages" / "zed" / "themes" / "gotham-noir.json",
            ROOT / "ports" / "paradev" / "gotham-noir-themes.json",
            ROOT / "ports" / "ghostty" / "Gotham Noir - Year One",
        ]
        before = {p: p.read_text(encoding="utf-8") for p in targets}
        subprocess.run([sys.executable, str(ROOT / "scripts" / "build.py")], check=True, capture_output=True)
        after = {p: p.read_text(encoding="utf-8") for p in targets}
        self.assertEqual(before, after)

    def test_web_browser_design_system_oss_and_skill_ports(self) -> None:
        # Herdr (4 dark + 1 daylight light + syntax helper)
        for slug in ("gotham-noir-year-one", "gotham-noir-batcomputer", "gotham-noir-arkham-slate", "gotham-noir-vengeance", "gotham-noir-daylight"):
            doc = json.loads((ROOT / "ports" / "herdr" / f"{slug}.json").read_text(encoding="utf-8"))
            self.assertEqual(len(doc["ansi"]), 16)
            self.assertIn("accent", doc["colors"])
        self.assertTrue((ROOT / "ports" / "herdr" / "gotham-noir-syntax.js").exists())

        # GitHub UserStyle
        gh_css = (ROOT / "ports" / "github" / "gotham-noir.user.css").read_text(encoding="utf-8")
        self.assertIn('domain("github.com")', gh_css)
        self.assertIn("#15171A", gh_css)

        # Linear LCH JSON + UserStyle
        for pal in self.palettes:
            lin = json.loads((ROOT / "ports" / "linear" / f"{pal['slug']}.json").read_text(encoding="utf-8"))
            self.assertEqual(len(lin["base"]), 4)
            self.assertEqual(len(lin["accent"]), 4)
            self.assertIn("sidebar", lin)
        self.assertIn('domain("linear.app")', (ROOT / "ports" / "linear" / "gotham-noir.user.css").read_text(encoding="utf-8"))

        # Slack sidebar strings
        for pal in self.palettes:
            txt = (ROOT / "ports" / "slack" / f"{pal['slug']}.txt").read_text(encoding="utf-8").strip()
            self.assertEqual(len(txt.split(",")), 10)

        # Chrome MV3 browser themes
        for pal in self.palettes:
            mpath = ROOT / "ports" / "chrome" / pal["slug"] / "manifest.json"
            m = json.loads(mpath.read_text(encoding="utf-8"))
            self.assertEqual(m["manifest_version"], 3)
            self.assertEqual(len(m["theme"]["colors"]["frame"]), 3)
            self.assertTrue((ROOT / "ports" / "chrome" / pal["slug"] / "icon-128.png").exists())

        # shadcn/ui CSS + registry JSON
        sh_reg = json.loads((ROOT / "ports" / "shadcn" / "r" / "gotham-noir.json").read_text(encoding="utf-8"))
        self.assertEqual(sh_reg["type"], "registry:theme")
        self.assertIn("dark", sh_reg["cssVars"])
        self.assertIn(".dark", (ROOT / "ports" / "shadcn" / "gotham-noir.css").read_text(encoding="utf-8"))

        # Palette CSS (both gotham-noir.css & gotham.css) + W3C tokens.json
        gn_css = (ROOT / "ports" / "palette" / "gotham-noir.css").read_text(encoding="utf-8")
        g_css = (ROOT / "ports" / "palette" / "gotham.css").read_text(encoding="utf-8")
        self.assertEqual(gn_css, g_css)
        self.assertIn("--gn-bg: #15171A;", gn_css)
        tokens = json.loads((ROOT / "ports" / "palette" / "tokens.json").read_text(encoding="utf-8"))
        self.assertIn("year-one", tokens)
        self.assertTrue(tokens["year-one"]["syntax"]["gold"]["oklch"].startswith("oklch("))

        # Fonts doc, real-code hero PNGs, OSS community health files, and Agent Skill
        for rel in (
            "ports/fonts/README.md",
            "assets/hero-year-one.png",
            "CODE_OF_CONDUCT.md",
            "SECURITY.md",
            "CONTRIBUTING.md",
            ".github/CODEOWNERS",
            "skills/gotham-noir/SKILL.md",
            "skills/gotham-noir/references/palettes.md",
            "llms.txt",
        ):
            self.assertTrue((ROOT / rel).exists(), f"Missing required file {rel}")


if __name__ == "__main__":
    unittest.main()
