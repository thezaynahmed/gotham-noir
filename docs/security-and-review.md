# Security, Merge Protection, and Advisory AI Review

This document records the merge-gate controls, deterministic security baseline, and third-party app scope for `thezaynahmed/gotham-noir`.

## 1. Required Merge Protection (`main`)

Protected by GitHub branch ruleset `27903827` (**Main: required CI and pull requests**):

- **Pull request required:** Direct pushes, force pushes, and branch deletions on `main` are blocked.
- **Required status check:** `validate` (`.github/workflows/validate.yml`) must pass on an up-to-date branch (`strict_required_status_checks_policy: true`).
- **Conversation resolution:** All pull request review threads must be resolved before merge (`required_review_thread_resolution: true`).
- **Bypass actors:** None (`bypass_actors: []`). Nobody, including the repository owner or third-party apps, can override or bypass this ruleset.

## 2. Deterministic CI & Security Baseline (Public Repo, $0)

- **CI Validation:** `.github/workflows/validate.yml` (`validate` job) rebuilds all Single Source of Truth outputs, enforces WCAG 2.1 + APCA Lc + red/green hue separation contrast gates, packages the `.vsix` with zero SVGs, runs `tests/test_themes.py`, and verifies zero uncommitted text drift.
- **Secret Scanning & Push Protection:** Enabled on GitHub.
- **CodeQL Code Scanning:** Enabled via GitHub default setup (`actions`, `python`), kept advisory until observed stable across pull requests.
- **Dependabot Alerts & Security Updates:** Enabled on GitHub.

## 3. Advisory AI Pull Request Review (CodeRabbit)

- **Repository scope (`Only select repositories`):** The CodeRabbit GitHub App (`coderabbitai`) is installed with access restricted to 4 explicitly selected repositories (public `thezaynahmed/gotham-noir` and `thezaynahmed/ghostty-config` for full OSS advisory reviews, plus private `thezaynahmed/portfolio` and `thezaynahmed/k8s-lecture-notes` under Free-plan PR summaries), never broad "All repositories" access.
- **Advisory only:** `.coderabbit.yaml` sets `reviews.request_changes_workflow: false` and `reviews.disable_cache: true`. CodeRabbit approval is not a hard merge gate; merge decisions always depend on deterministic CI (`validate` + security scans), never LLM approval.

## 4. Private Repository Baseline ($0)

For private repositories under GitHub Free, rely on Dependabot alerts/security updates plus open-source GitHub Actions (`gitleaks`, `semgrep` / `bandit`, `trivy`) for deterministic gates, and local CLI/agent review or self-hosted BYOK `PR-Agent` for advisory AI review.
