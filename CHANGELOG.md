# Changelog

Semua perubahan penting pada proyek ini didokumentasikan di file ini.

Format berdasarkan [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
dan proyek ini mengikuti [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
## [0.1.1](https://github.com/Miruameli/apex/compare/v0.1.0...v0.1.1) (2026-10-08)


### Bug Fixes

* **ci:** fix cargo fmt flag and add bridge build to Python Quality Gate job ([85d597a](https://github.com/Miruameli/apex/commit/85d597ad60abedab83acbc39c99760e43b56c804))
* **ci:** fix Quality Gate failures (fmt, bridge, TS test path, PyO3 vuln) ([ba8dfef](https://github.com/Miruameli/apex/commit/ba8dfef6d425910d97176160778114b8dbbfcbb0))
* **ci:** pin gitleaks action to full commit SHA ([#11](https://github.com/Miruameli/apex/issues/11)) ([974697e](https://github.com/Miruameli/apex/commit/974697ef03a07e0f362294ae323d4694d795ca59))
* **ci:** update TUI entry point path in release.yml ([#13](https://github.com/Miruameli/apex/issues/13)) ([38498f8](https://github.com/Miruameli/apex/commit/38498f80f6da286f678def2dfa2acab9c4757440)), closes [#12](https://github.com/Miruameli/apex/issues/12)
* **release:** fetch-tags=true in release-please workflow checkout ([a96688d](https://github.com/Miruameli/apex/commit/a96688d1ce8c55bab3678c70410c93d31f7539c0))
* **release:** remove invalid v4.1.1 inputs and add v0.1.0 CHANGELOG ([9d882e9](https://github.com/Miruameli/apex/commit/9d882e9f01e2934d73be00383944830690d1f184)), closes [#1](https://github.com/Miruameli/apex/issues/1)
* **release:** separate config and manifest files to fix release-please crash ([963871d](https://github.com/Miruameli/apex/commit/963871d97b592c829cdd25ea87ffd905a9a40c59))
* **release:** switch to python release-type for version reading ([45efb83](https://github.com/Miruameli/apex/commit/45efb8328d0230db87f398de6c2ecd444a1c2d0e))
* **release:** use simple release-type for workspace-compatible version bumping ([eecc2c8](https://github.com/Miruameli/apex/commit/eecc2c8b39059ffee2b8da3b427ee3c4144ef593))
* **release:** use simple release-type with typed extra-files ([4a63f93](https://github.com/Miruameli/apex/commit/4a63f933022600a7ec6d2c6855667813875f1176))

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
- `release-please-config.json` — config file: `release-type: "rust"` with
    `extra-files` for `pyproject.toml` and `tui/deno.json` (Rust plugin reads
    version from `[package]` in root `Cargo.toml`); `.release-please-manifest.json`
    tracks released versions per path
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
