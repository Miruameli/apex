# Changelog

Semua perubahan penting pada proyek ini didokumentasikan di file ini.

Format berdasarkan [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
dan proyek ini mengikuti [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
## [0.1.0] - 2026-10-07

### Added
- Repository initialized with git (branch: main)
- SHA-pinned GitHub Actions workflows (`release-please.yml`, `release.yml`, `quality.yml`)
- Auto-release versioning via `release-please` — bumps version across `Cargo.toml`, `pyproject.toml`, and `tui/deno.json` from conventional commits
- Multi-language documentation mirrors (en, id, ko, ja, zh) synced with auto-release content
- `scripts/checks/` module — `check_versions.py`, `check_modularization.py`, `check_docs_links.py`

### Changed
- Pinned `release-please-action` from `@v4` mutable tag to full commit SHA `e4dc86ba9405554aeba3c6bb2d169500e7d3b4ee` (v4.1.1) — resolves Semgrep `github-actions-mutable-action-tag` supply-chain finding
- Pinned `actions/checkout` to SHA `11d5960a326750d5838078e36cf38b85af677262` (already verified across all workflows)
- Crate `Cargo.toml` files now inherit version from workspace root via `version.workspace = true` — single source of truth

### Security
- Supply-chain hardening: 30/30 `uses:` references verified as 40-character commit SHAs (0 mutable tags)
- Semgrep SAST: 0 findings
- Gitleaks secret scan: 0 findings

## [Unreleased] - Development

### Added
- `release-please` auto-release workflow (`.github/workflows/release-please.yml`)
  — bumps version across `Cargo.toml`, `pyproject.toml`, and `tui/deno.json`
  from conventional commits, rewrites `CHANGELOG.md`, and opens a release PR
  on every push to `main`. Eliminates manual version editing for small fixes.
- `.release-please-manifest.json` — manifest mapping all three language
  manifests into a single version-bump operation
- `scripts/checks/check_versions.py` — verifies version strings are consistent across
  all three language manifests; added to `scripts/verify.sh` quality gate
- Release checklist auto-release note

### Changed
- `Cargo.lock` is no longer gitignored; the binary workspace commits it for
  reproducible release builds (required by `release-please` rust release-type)
- Crate `Cargo.toml` files (`apex-core`, `apex-cli`, `apex-py`) now inherit
  version from the workspace root via `version.workspace = true` — single
  source of truth so `release-please` only updates one location

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A

### Security
- N/A

---

## Template untuk Rilis Baru

### Added
- Fitur baru

### Changed
- Perubahan pada fungsionalitas existing

### Deprecated
- Fitur yang akan dihapus

### Removed
- Fitur yang dihapus

### Fixed
- Perbaikan bug

### Security
- Perbaikan keamanan
