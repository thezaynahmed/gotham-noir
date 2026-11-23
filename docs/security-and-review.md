# Security, Merge Protection, and Advisory AI Review

This document records the merge-gate controls, deterministic security baseline, and third-party app scope for `thezaynahmed/gotham-noir`.

## 1. Deterministic CI & Security Baseline (Public Repo, $0)

- **CI Validation:** `.github/workflows/validate.yml` (`validate` job) rebuilds all Single Source of Truth outputs, enforces WCAG 2.1 + APCA Lc + red/green hue separation contrast gates, packages the `.vsix` with zero SVGs, runs `tests/test_themes.py`, and verifies zero uncommitted text drift.
- **Secret Scanning & Push Protection:** Enabled on GitHub.
- **CodeQL Code Scanning:** Enabled via GitHub default setup (`actions`, `python`).
- **Dependabot Alerts & Security Updates:** Enabled on GitHub.

## 2. Advisory AI Pull Request Review (CodeRabbit)

- **Repository scope:** When installed, the CodeRabbit GitHub App (`coderabbitai`) is restricted to **Only select repositories** (`thezaynahmed/ghostty-config` and `thezaynahmed/gotham-noir`), never broad "All repositories" access.
- **Advisory only:** `.coderabbit.yaml` sets `reviews.request_changes_workflow: false` and `reviews.disable_cache: true`. Merge decisions always depend on deterministic CI and security checks, never LLM approval.

## 3. Private Repository Baseline ($0)

For private repositories under GitHub Free, rely on Dependabot alerts/security updates plus open-source GitHub Actions (`gitleaks`, `semgrep` / `bandit`, `trivy`) for deterministic gates, and local CLI/agent review or self-hosted BYOK `PR-Agent` for advisory AI review.
