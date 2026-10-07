# Apex — Docs Index

Blueprint and engineering reference for Apex, the terminal AI coding agent.

## Domains

| Folder | Scope |
|---|---|
| [`product/`](product/) | Product spec, user journey, feature matrix |
| [`engineering/`](engineering/) | Stack, architecture, protocol, subsystems, quality, build |
| [`community/`](community/) | Setup, contributing, code of conduct, RFC process |
| [`operations/`](operations/) | Governance, decisions, ADRs, runbooks, master blueprint |

Each domain has its own `README.md` with a reading order and per-folder index.

## Tree

```
docs/
├── README.md                  # this index
├── product/
│   ├── README.md
│   ├── 01-product-spec.md
│   ├── 02-user-journey.md
│   └── 03-feature-matrix.md
├── engineering/
│   ├── README.md
│   ├── stack/
│   │   ├── 04-tech-stack.md
│   │   ├── 05-architecture.md
│   │   ├── 06-protocol.md
│   │   └── 07-skills-mcp.md
│   ├── data-model/
│   │   ├── 26-data-model.md
│   │   ├── 27-error-handling.md
│   │   └── 46-system-error-recovery.md
│   ├── quality/
│   │   ├── 28-testing-strategy.md
│   │   ├── 30-i18n.md
│   │   ├── 51-code-style.md
│   │   └── 52-testing-guide.md
│   ├── build-release/
│   │   ├── 29-build-release.md
│   │   └── 47-system-build-sync.md
│   └── subsystems/
│       ├── core/             # context, rust core, bridge, memory, security
│       ├── agent/            # agent loop, python agent, provider, tool registry
│       ├── workflow/         # review, commit/ship, git, init, workflow
│       ├── extensibility/    # skills, skill runtime, MCP, marketplace, LSP
│       └── interface/        # TUI, TUI detail, CLI, IPC contract
├── community/
│   ├── README.md
│   ├── setup/                # dev setup, installation, customization
│   ├── practice/             # contributing, CoC, key custody
│   └── rfc/                  # RFC process
└── operations/
    ├── README.md
    ├── governance/           # roadmap, release, governance, security, privacy
    ├── decisions/            # decision log, open questions
    ├── adr/                  # architecture decision records
    ├── runbook/              # operational procedures
    └── blueprint/            # master blueprint, CLI final
```

## Numbering

File numbers are stable identifiers inherited from the original blueprint sequence.
They are **not** positional: a number never changes when a file moves. New files take
the next free number in their domain.

## Principles

1. No assumptions — verify before writing code.
2. Bilingual-ready: docs are written in Indonesian, UI and code comments in English.
3. Machine-checkable — protocol fixtures in `tests/fixtures/protocol/` are the contract.
4. `[OPEN]` marks anything not yet decided; see
   [`operations/decisions/32-open-questions.md`](operations/decisions/32-open-questions.md).
5. ADRs are immutable — supersede, never edit.
