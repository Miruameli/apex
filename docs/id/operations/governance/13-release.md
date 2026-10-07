# 13 — Release & Distribusi

## Distribusi

Belum ada rilis yang dipublikasikan. Tabel ini adalah target, bukan kondisi nyata:

| Channel | Artifak | Cara install | Status |
|---|---|---|---|
| GitHub Releases | Binary `apex` (Rust) | Berkas checksum + SBOM | Direncanakan |
| PyPI / uv | `apex` Python package | `uv pip install apex` | Direncanakan |
| Homebrew | Formula | `brew install apex` | V1 |
| Cargo | `apex-cli` | `cargo install apex-cli` | V1 |
| Source | Workspace repo | `./scripts/build.sh` | Aktif |

## Versioning

- Semantic: `MAJOR.MINOR.PATCH`
- `0.x` = MVP/development, breaking allowed
- `1.0` = MVP stabil, DoD terpenuhi
- Changelog: `CHANGELOG.md` per release, grouped by breaking/feat/fix/docs

## Auto-Release (tanpa manual version edit)

- Auto-release via [`release-please`](https://github.com/googleapis/release-please)
  (`.github/workflows/release-please.yml`). Pushes to `main` with conventional
  commits trigger an automatic version bump, `CHANGELOG.md` rewrite, and a
  release PR. Merging the PR cuts the git tag, which fires
  `.github/workflows/release.yml` to build and publish artifacts.
- Version strings live in exactly one place per ecosystem: the workspace
  `Cargo.toml` (`version.workspace = true` on all crates), `pyproject.toml`,
  and `tui/deno.json`. `scripts/checks/check_versions.py` (run by `verify.sh`)
  enforces they stay in sync.
- Conventional commit parsing:
  - `feat:` → minor bump
  - `fix:` → patch bump
  - `BREAKING CHANGE:` or `!:` → major bump

## Release checklist (auto-release)

Setelah `release-please` membuka release PR dan PR sudah merged ke `main`:

- [x] `./scripts/verify.sh` hijau (quality gate)
- [x] Tests 3 bahasa hijau
- [x] Docs di-update
- [x] `CHANGELOG.md` di-update oleh release-please
- [x] Tag git created otomatis oleh release-please
- [ ] Binary + Python package built oleh `release.yml`
- [ ] `sha256` checksum dan SBOM dibuat oleh `release.yml`
- [ ] Install smoke test di environment bersih

## Channel

- Stable: tag `vX.Y.Z`
- Nightly: `main` branch build (V1)
- Beta: `vX.Y.Z-beta.N` (V1)
