# Engineering Docs

Technical reference for Apex: stack, architecture, contracts, and per-subsystem detail.

## Subfolders

| Folder | Scope |
|---|---|
| [`stack/`](stack/) | Tech stack, architecture, protocol, skills/MCP design |
| [`data-model/`](data-model/) | Data model, error handling, error recovery |
| [`quality/`](quality/) | Testing strategy, testing guide, code style, i18n |
| [`build-release/`](build-release/) | Build pipeline, bridge sync, release mechanics |
| [`subsystems/`](subsystems/) | Per-component detail (core, agent, workflow, extensibility, interface) |

## Subsystem groups

| Group | Components |
|---|---|
| `core/` | context scan, rust core, PyO3 bridge, memory, security |
| `agent/` | agent loop, python agent, provider, provider LLM, tool registry |
| `workflow/` | review, commit/ship, git, init, workflow engine |
| `extensibility/` | skills, skill runtime, MCP, marketplace, LSP |
| `interface/` | TUI, TUI detail, CLI, IPC contract |

## Reading order

1. [`stack/04-tech-stack.md`](stack/04-tech-stack.md) — apa yang dipakai dan kenapa
2. [`stack/05-architecture.md`](stack/05-architecture.md) — bagaimana komponen terhubung
3. [`stack/06-protocol.md`](stack/06-protocol.md) — kontrak JSONL antar 3 bahasa
4. [`subsystems/core/43-system-rust-core.md`](subsystems/core/43-system-rust-core.md) — isi speed core
5. [`subsystems/interface/22-system-cli.md`](subsystems/interface/22-system-cli.md) — surface CLI
