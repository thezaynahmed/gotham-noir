# Security Policy

## Supported Versions

Only the latest release on the `main` branch receives security updates and build fixes.

| Version | Supported |
| :--- | :--- |
| `1.x` (`main`) | Yes |
| `< 1.0` | No |

## Reporting a Vulnerability

Please **do not** open a public GitHub Issue for security vulnerabilities (for example malicious generator scripts, supply-chain issues, unsafe shell adapters, or CI workflow injection).

Report vulnerabilities privately using [GitHub Security Advisories](https://github.com/thezaynahmed/gotham-noir/security/advisories/new) or contact the maintainer via [zainahmed.net](https://zainahmed.net/).

Include:
1. Affected file(s) or release artifact
2. Reproduction steps or proof of concept
3. Impact assessment and suggested remediation (if known)

You can expect an initial acknowledgement within 72 hours.

## Security Posture

- **Zero runtime telemetry:** Theme files, CSS tokens, and editor extensions contain static color/typography definitions only.
- **Deterministic gates:** Every pull request runs automated CI validation (`Validate Gotham Noir`), GitHub CodeQL (`actions`, `python`), Secret Scanning with Push Protection, and Dependabot security updates.
- **Maintainer review:** All pull requests require review and approval by the project maintainer (`@thezaynahmed`). See [`docs/security-and-review.md`](docs/security-and-review.md) for full details.
