# Security Policy

## Supported Versions

This repository currently supports security updates on the default branch.

## Reporting a Vulnerability

If you discover a security vulnerability, please open a private security advisory in GitHub:

1. Go to the repository.
2. Open the **Security** tab.
3. Click **Report a vulnerability**.
4. Provide details, impact, and reproducible steps.

Please do not open public issues for unpatched vulnerabilities.

## Repository Protection Baseline

This repository includes:

- CodeQL analysis workflow (`.github/workflows/codeql.yml`)
- Secret scanning workflow (`.github/workflows/secret-scanning.yml`)
- Dependabot update automation (`.github/dependabot.yml`)

Recommended repository settings in GitHub:

- Require pull request reviews before merge
- Require status checks to pass before merge
- Restrict direct pushes to the default branch
- Enable secret scanning and push protection
