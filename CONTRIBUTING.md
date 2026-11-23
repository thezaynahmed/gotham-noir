# Contributing to Gotham Noir

Contributions, contrast audits, bug fixes, and new app/editor ports are welcome. This project follows strict engineering hygiene: small focused changes, single-source-of-truth generation, automated verification, and explicit maintainer review.

## Governance & Pull Request Approval

- Every pull request is reviewed and approved by the maintainer (`@thezaynahmed`, [zainahmed.net](https://zainahmed.net/)) via `.github/CODEOWNERS`.
- Keep each PR focused on one clear change (one new port, one palette fix, or one doc improvement).
- Write clear commit messages explaining **why** the change exists, not just what files moved.
- Do not submit hand-edited generated outputs without updating the canonical source in [`palettes/`](palettes/) or [`scripts/`](scripts/).

## Single-Source-of-Truth Workflow

Every extension, CSS token file, and terminal/app port compiles from [`palettes/`](palettes/):

1. Edit palettes in [`palettes/`](palettes/) or generators in [`scripts/`](scripts/).
2. Regenerate all outputs and run the automated contrast gate:
   ```bash
   python3 scripts/build.py
   ```
3. Run the full test suite and verify `.vsix` packaging:
   ```bash
   python3 -m unittest discover -s tests -v
   cd packages/vscode && npx --yes @vscode/vsce package -o gotham-noir-1.0.0.vsix
   ```
4. Ensure `git diff -- . ':(exclude)*.png'` shows only intentional changes and all CI checks pass.

## Color Science & Quality Rules

- **No `#000000` / `#FFFFFF` halation:** Keep canvases in the anti-halation dark range (`#101215` to `#1D1F21`) and foreground ink softened (`#D8D6CF` to `#DCE0E5`).
- **Contrast gates:** Primary text must maintain WCAG 2.1 AAA / high AA and APCA Lc balance across syntax roles.
- **Semantic separation:** Keep ANSI red and green separated by at least 110 degrees so diffs and CI logs stay unmistakable.
- **Marketplace rules:** Never add `.svg` references to `packages/vscode/package.json` or `packages/vscode/README.md`.

## Community Standards

Participation is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). Security issues must be reported privately per [SECURITY.md](SECURITY.md).

## License

By contributing, you agree that your contributions are released under the [MIT License](LICENSE).
