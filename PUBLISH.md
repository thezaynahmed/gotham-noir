# Publishing Guide — Gotham Noir

Everything in this repository is built and validated locally from [`palettes/`](palettes/) via `python3 scripts/build.py`. Use this checklist when you are ready to publish publicly.

---

## 0. Create & Push GitHub Repo (`thezaynahmed/gotham-noir`)

```bash
cd /Users/zain/gotham-noir
gh repo create thezaynahmed/gotham-noir --public --source=. --remote=origin --push
```

---

## 1. VS Code Marketplace (`code`)

**Requirements:**
- PNG icon only (`packages/vscode/images/icon.png` — 128x128 PNG, already generated; zero SVGs in `package.json` or `README.md`).
- Publisher `thezaynahmed` created at [Visual Studio Marketplace Management Portal](https://marketplace.visualstudio.com/manage).
- Azure DevOps PAT with **Marketplace (Manage)** scope (or GitHub Actions `VSCE_PAT` secret).

```bash
cd /Users/zain/gotham-noir/packages/vscode
npx --yes @vscode/vsce package -o gotham-noir-1.0.0.vsix
npx --yes @vscode/vsce login thezaynahmed
npx --yes @vscode/vsce publish --packagePath gotham-noir-1.0.0.vsix
```

---

## 2. Open VSX Registry (Cursor, Windsurf, Antigravity IDE)

**Requirements:**
- GitHub account linked to Eclipse Foundation at [open-vsx.org](https://open-vsx.org/) + signed Publisher Agreement.
- Unscoped `name` (`"gotham-noir"` — already configured).
- Access token generated from Open VSX user settings.

```bash
cd /Users/zain/gotham-noir/packages/vscode
npx --yes ovsx create-namespace thezaynahmed -p "$OVSX_PAT"
npx --yes ovsx publish gotham-noir-1.0.0.vsix -p "$OVSX_PAT"
```

---

## 3. Zed Extensions Registry (`zed-industries/extensions`)

1. Fork `zed-industries/extensions` on GitHub.
2. Add this repo (or copy `packages/zed/` into a dedicated standalone repo `thezaynahmed/zed-gotham-noir`) as a submodule under `extensions/gotham-noir` via HTTPS URL.
   - Note: Zed's extension PR requires `extension.toml` at the submodule root (`thezaynahmed/zed-gotham-noir`) or pointing to a repo whose root contains `extension.toml`. If publishing from a monorepo, create a lightweight mirror repo containing the contents of `packages/zed/` + `LICENSE`.
3. Update `extensions.toml` in `zed-industries/extensions` and open a PR (1 extension per PR).

---

## 4. Ghostty, iTerm2 & 20+ Terminals (`mbadolato/iTerm2-Color-Schemes`)

Ghostty pulls its built-in themes from `mbadolato/iTerm2-Color-Schemes`!
1. Fork and clone `mbadolato/iTerm2-Color-Schemes`.
2. Copy the 4 XML `.itermcolors` files from `ports/iterm2/*.itermcolors` into `schemes/`:
   - `Gotham Noir - Year One.itermcolors`
   - `Gotham Noir - Batcomputer.itermcolors`
   - `Gotham Noir - Arkham Slate.itermcolors`
   - `Gotham Noir - Vengeance.itermcolors`
3. Run their repo generator script (`tools/gen.py`) per their `CONTRIBUTING.md` and open a PR.

---

## 5. Warp (`warpdotdev/themes`)

1. Fork and clone `warpdotdev/themes`.
2. Copy `ports/warp/*.yaml` into `standard/`.
3. Regenerate Warp preview thumbnails:
   ```bash
   python3 ./scripts/gen_theme_previews.py standard
   ```
4. Commit and open a PR against `warpdotdev/themes`.

---

## 6. Kitty (`kovidgoyal/kitty-themes`)

1. Fork and clone `kovidgoyal/kitty-themes`.
2. Copy `ports/kitty/gotham_noir*.conf` into `themes/` (all 4 already include `## name:`, `## author:`, `## license: MIT`, `## blurb:` headers).
3. Test locally via `kitty +kitten themes` and open a PR.

---

## 7. Alacritty (`alacritty/alacritty-theme`)

1. Fork and clone `alacritty/alacritty-theme`.
2. Copy `ports/alacritty/gotham-noir*.toml` into `themes/`.
3. Commit and open a PR.
