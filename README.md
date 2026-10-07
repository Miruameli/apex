# Apex

[![CI](https://github.com/apex-org/apex/actions/workflows/quality.yml/badge.svg)](https://github.com/apex-org/apex/actions/workflows/quality.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Rust](https://img.shields.io/badge/Rust-2024%20Edition-orange.svg)](https://www.rust-lang.org)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org)
[![Deno](https://img.shields.io/badge/Deno-2.x-black.svg)](https://deno.land)

**Apex — All in terminal. Custom sendiri.**

Apex is a terminal AI coding agent for solo open-source developers. Chat, review, commit, ship, and extend — all in your terminal.

## ✨ Features (MVP)

| Feature | Command | Description |
|---------|---------|-------------|
| **Chat** | `apex chat` | Streaming chat with codebase context |
| **Context** | `apex context` | Scan & index your codebase |
| **Review** | `apex review` | Security, perf, clean-code review |
| **Commit** | `apex commit` | Atomic commit messages from diff |
| **Ship** | `apex ship` | Create PR with changelog |
| **Skills** | `apex skill add/run` | Extensible plugins (Python/TS/bin) |
| **MCP** | connector | GitHub, DB, Notion, Linear via MCP |
| **TUI** | `apex` | Full lazygit-style split-panel UI |

## 🚀 Quickstart

```bash
# Prerequisites: Rust, Python 3.12+ (via uv), Deno 2.x
# Clone and build
git clone https://github.com/apex-org/apex
cd apex
./scripts/build.sh
./scripts/verify.sh

# Run TUI
apex

# Or use CLI commands
apex chat "explain this codebase"
apex context
apex review --staged
apex commit
apex ship --push
```

## 📖 Documentation

- [Product Spec](docs/id/product/01-product-spec.md) — Vision, positioning, MVP scope
- [Architecture](docs/id/engineering/stack/05-architecture.md) — System diagram, data flows
- [Tech Stack](docs/id/engineering/stack/04-tech-stack.md) — Python/Rust/TypeScript roles
- [Protocol](docs/id/engineering/stack/06-protocol.md) — JSONL IPC contract
- [Skills & MCP](docs/id/engineering/stack/07-skills-mcp.md) — Extension system
- [Customization](docs/id/community/setup/08-customization.md) — apex.json, APEX.md, themes
- [Security](docs/id/operations/governance/54-security-policy.md) — Key custody, threat model
- [Contributing](docs/id/community/practice/10-contributing.md) — How to contribute

## 🏗️ Architecture

```
┌─────────────┐     JSONL stdio      ┌──────────────────┐
│  TUI (TS)   │ ◀──────────────────▶ │  Agent (Python)  │
│  CLI (Rust) │ ◀──────────────────▶ │  (orchestration) │
└──────┬──────┘                       └────────┬─────────┘
       │                                       │
       │              PyO3                     │
       └──────────────────────▶ ┌─────────────┘
                                ▼
                       ┌──────────────────┐
                       │  Core (Rust)     │
                       │  - context scan  │
                       │  - protocol      │
                       │  - session       │
                       │  - skill host    │
                       └──────────────────┘
```

**Three languages, clear boundaries** (ADR-0001):
- **Python** — LLM orchestration, prompt engineering, tool registry
- **Rust** — Hot paths: context scan, protocol, session, skill host
- **TypeScript (Deno)** — Interactive TUI, no build step

## 🔧 Configuration

```json
// apex.json — Project configuration
{
  "provider": { "name": "anthropic", "model": "claude-3-5-sonnet" },
  "ui": { "language": "en", "theme": "dark" },
  "review_rules": { "security": true, "performance": true },
  "skills": { "enabled": true }
}
```

```markdown
<!-- APEX.md — Project memory for the agent -->
# Project Rules
- Use snake_case for Rust, camelCase for TS
- Max 150 SLOC per file
- Write tests for all new logic
```

## 🛠️ Development

```bash
# Setup (one-time)
./scripts/setup_dev.sh

# Quality gate (run before commit)
./scripts/verify.sh

# Individual checks
cargo fmt --check --workspace
cargo clippy --workspace -- -D warnings
cargo test --workspace
uv run pytest
deno fmt --check tui/src
deno lint tui/src
deno test --allow-all tui/src
python scripts/checks/check_docs_links.py
python scripts/checks/check_modularization.py
```

## 📋 Standards

- **Modularization**: Max 5 files/folder, max 150 SLOC/file, even layer distribution
- **Security**: Zero trust, gitleaks, cargo audit, pip-audit, trivy in CI
- **Commits**: Conventional Commits, signed, no direct push to main
- **Reviews**: Self-review mandatory, CI must pass

## 🚀 Release (Auto)

Releases are fully automated via [`release-please`](.github/workflows/release-please.yml).
Every push to `main` bumps the version across `Cargo.toml`, `pyproject.toml`,
and `tui/deno.json` based on [Conventional Commits](https://www.conventionalcommits.org/):

| Commit prefix | Bump |
|---|---|
| `feat:` | minor |
| `fix:` | patch |
| `BREAKING CHANGE:` or `!:` | major |

The flow: `push → release-please PR → merge → tag → release.yml builds artifacts`.
`scripts/checks/check_versions.py` (in `verify.sh`) ensures all manifests stay in sync.
`Cargo.lock` is now tracked for reproducible binary builds.

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md).

1. Open an issue first (except trivial fixes)
2. Fork, branch, commit with conventional messages
3. Run `./scripts/verify.sh` locally
4. Open PR → CI passes → review → merge

## 📄 License

MIT © Apex Contributors — see [LICENSE](LICENSE).

---
**Status**: Phase 1 (Foundation) — complete. Rust workspace, PyO3 bridge, protocol fixtures, CLI/TUI stubs, CI quality gate, and auto-release all verified. Next: Phase 2 MVP features (chat, context scan, review).