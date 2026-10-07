# Changelog

Semua perubahan penting pada proyek ini didokumentasikan di file ini.

Format berdasarkan [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
dan proyek ini mengikuti [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
