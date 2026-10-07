# 03 — Feature Matrix

## MVP (dikunci)

| Fitur | Command | Status | Keterangan |
|---|---|---|---|
| Chat agent | `apex chat` | MVP | Streaming, konteks codebase, approval sebelum edit |
| Context scan | `apex context` | MVP | Index file + git history + LSP hint |
| Review | `apex review` | MVP | Security/perf/clean code, output diff + rekomendasi |
| Commit | `apex commit` | MVP | Atomic message dari staged diff |
| Ship/PR | `apex ship` | MVP | PR mock lokal (GitHub connector nyusul) |
| Skills | `apex skill add/run` | MVP | SKILL.md + script subprocess, Rust host |
| MCP | connector | MVP | GitHub/DB/Notion/Linear sebagai skill khusus |
| TUI | `apex` / `apex tui` | MVP | Full lazygit split-panel, diff per-hunk |
| Safety | approval, undo, sandbox | MVP | Approval wajib, undo rollback, sandbox command optional |

## V1 (nyusul)

| Fitur | Alasan |
|---|---|
| Auto-fix error | Perlu LSP stabil + LLM function calling |
| Plan mode autonomous | Perlu approval gate + undo lengkap |
| Local LLM default | Perlu benchmark + UX Ollama |
| Marketplace plugin | Perlu registry, trust, review process |
| Cost tracker | Perlu token usage instrumentation |
| Tema custom | Perlu theme engine + user-defined palette |

## V2 (masa depan)

| Fitur | Alasan |
|---|---|
| Voice input | Perlu ASR integration |
| `apex share` kolaborasi | Perlu backend + auth |
| Multi-agent orchestrator | Perlu task decomposition + merge strategy |
| Sandbox Docker default | Perlu image management + resource limits |

## Open decision `[OPEN]`

- Nama command CLI pasti (tentukan di RFC #001)
- TUI library (Cliffy / OpenTUI / stdlib)
- Posisi marketplace plugin (MVP/V1/V2)
- Bahasa default UI (Indonesia vs English) — bilingual ready, default TBD
