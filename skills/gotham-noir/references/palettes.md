# Gotham Noir Palette Reference

All 4 canonical dark palettes compile from `palettes/*.json` and pass automated WCAG 2.1 + APCA Lc verification in `scripts/contrast.py`.

## Primary Contrast Metrics

| Variant | Canvas | Foreground | Accent | WCAG Ratio | APCA Lc | R/G Hue Sep |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Year One** | `#15171A` | `#D8D6CF` | `#F0C946` | `12.35:1` | `Lc 80.7` | `154.2 deg` |
| **Batcomputer** | `#101215` | `#DCE0E5` | `#F5D042` | `14.15:1` | `Lc 87.0` | `163.6 deg` |
| **Arkham Slate** | `#1D1F21` | `#DAD5C7` | `#E6C15A` | `11.28:1` | `Lc 79.2` | `112.6 deg` |
| **Vengeance** | `#151417` | `#DDD8D5` | `#E5535C` | `12.98:1` | `Lc 82.7` | `152.0 deg` |

## Year One Semantic Syntax Tokens

| Role | Hex | CSS Variable (`gotham-noir.css`) |
| :--- | :--- | :--- |
| Canvas | `#15171A` | `--gn-bg` |
| Primary Text | `#D8D6CF` | `--gn-fg` |
| Muted / Comments | `#878D96` | `--gn-fg-muted` |
| Types / Classes / Cursor | `#F0C946` | `--gn-gold` |
| Functions / Methods | `#74AEEB` | `--gn-blue` |
| Strings / Diff + | `#63C794` | `--gn-emerald` |
| Operators / YAML Keys | `#68C5CE` | `--gn-cyan` |
| Constants / Parameters | `#E29754` | `--gn-amber` |
| Keywords / Decorators | `#B695E8` | `--gn-violet` |
| Errors / Diff - | `#E86A74` | `--gn-crimson` |
| Language Vars (`self`/`this`) | `#E0A4B8` | `--gn-rose` |
