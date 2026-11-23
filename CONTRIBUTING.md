# Contributing to Gotham Noir

Pull requests, contrast audits, and new terminal/editor ports are welcome.

## Single-Source-of-Truth Workflow

Every extension and terminal port is generated from the canonical palettes in [`palettes/`](palettes/):

1. Edit or add tokens in [`palettes/`](palettes/) and generator logic in [`scripts/`](scripts/).
2. Regenerate all outputs and run the contrast gate:
   ```bash
   python3 scripts/build.py
   ```
3. Verify the full test suite and `.vsix` packaging:
   ```bash
   python3 -m unittest discover -s tests -v
   cd packages/vscode && npx --yes @vscode/vsce package -o gotham-noir-1.0.0.vsix
   ```

## Color Science & Accessibility Rules

- No `#000000` backgrounds or `#FFFFFF` foregrounds (anti-halation surface range).
- Maintain WCAG 2.1 AAA / high AA foreground contrast and OKLCH luminance balance across syntax roles.
- Keep ANSI red and green separated by at least 110 degrees so diffs and logs read cleanly.
- Never reference `.svg` assets in `packages/vscode/package.json` or `packages/vscode/README.md`.

## License

By contributing, you agree that your contributions are released under the [MIT License](LICENSE).
