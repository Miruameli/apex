# Runbook: Release

Apex uses **automatic release versioning** via
[`release-please`](https://github.com/googleapis/release-please).
Version bumps, changelog updates, and tag creation happen automatically from
conventional commits — no manual version editing required.

A source-only release is **not** a release: binaries, checksums, and an SBOM
are mandatory and are produced by `.github/workflows/release.yml` on every tag
push.

## Objective

Publish a reproducible release for every supported platform, with verifiable
artifacts and signed provenance.

## Prerequisites

- [ ] `main` is green on CI (quality gate)
- [ ] All commits use conventional-commit format (`feat:`, `fix:`, `BREAKING CHANGE:`)
- [ ] `CHANGELOG.md` will be rewritten by release-please (no manual edit needed)

## How it works

```
push to main → release-please.yml
    → analyze conventional commits since last tag
    → determine SemVer bump (breaking! / feat / fix)
    → bump Cargo.toml, pyproject.toml, tui/deno.json
    → rewrite CHANGELOG.md [Unreleased] → [vX.Y.Z]
    → open release PR
    → merge PR → create git tag vX.Y.Z
        → release.yml triggers on tag push
            → build Rust release binary per platform
            → sync PyO3 bridge (Python package)
            → compile Deno TUI binary
            → generate sha256 checksums + SBOM
            → publish GitHub Release with artifacts
```

## Steps (manual override)

Use these only when release-please is unavailable or you need to cut a hotfix
manually.

### 1. Confirm the version

```sh
uv run python scripts/checks/check_versions.py
```

All three manifests must report the same version.

### 2. Verify before tagging

```sh
./scripts/verify.sh
cargo test --workspace
```

### 3. Bump version (if releasing manually)

```sh
# Edit all three files, then:
uv run python scripts/checks/check_versions.py
git add Cargo.toml pyproject.toml tui/deno.json
git commit -m "chore(release): bump version to v0.1.0"
```

### 4. Tag and push

```sh
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
```

Never force-push a tag.

### 5. Build release artifacts

```sh
cargo build --workspace --release --locked
```

Binaries are produced per target in CI, not on one machine.

### 6. Generate checksums

```sh
cd dist
sha256sum * > checksums.txt
```

### 7. Generate the SBOM

```sh
cargo cyclonedx --workspace > apex-<version>.cdx.json
```

### 8. Publish

Attach to the GitHub release: binaries per platform, the checksum file, the
SBOM, and the changelog section.

## Release checklist

- [ ] Tag exists and points at a commit on `main`
- [ ] CI green on that commit
- [ ] Binary for each supported platform
- [ ] `sha256` checksum file published
- [ ] SBOM published
- [ ] Release notes match `CHANGELOG.md`
- [ ] Migration notes if the release has a breaking change

## Rollback plan

Releases are immutable. To withdraw a release:

1. Mark it as a prerelease on GitHub.
2. Publish a patch release with the fix.
3. Do **not** delete or move the tag — that breaks anyone who already pinned it.

## Escalation

| Symptom | Action |
|---|---|
| CI red on the release commit | Stop. Do not tag a red build. |
| One platform failed to build | Publish nothing; fix and rerun. Partial releases are worse than delayed ones. |
| Checksum mismatch reported by a user | Treat as a supply-chain incident; revoke and investigate immediately |

## Last Updated: 2026-10-07
