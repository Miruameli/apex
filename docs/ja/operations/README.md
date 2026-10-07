# Operations Docs

Governance, decisions, and runbooks for operating and releasing Apex.

## Subfolders

| Folder | Scope |
|---|---|
| [`governance/`](governance/) | Roadmap, release policy, governance, security & privacy policy |
| [`decisions/`](decisions/) | Decision log and open questions |
| [`adr/`](adr/) | Architecture Decision Records — one file per significant decision |
| [`runbook/`](runbook/) | Step-by-step operational procedures |
| [`blueprint/`](blueprint/) | Master system blueprint and finalized CLI surface |

## Decision flow

```
community/rfc/53-rfc-process.md  →  operations/adr/NNNN-*.md  →  decisions/31-decisions.md
          (propose)                       (record)                   (log summary)
```

1. Small change that fits an existing rule: edit the relevant doc directly.
2. Change that alters architecture: open an RFC first.
3. Accepted RFC becomes an ADR. ADRs are immutable; supersede instead of editing.
4. Record the one-line summary in [`decisions/31-decisions.md`](decisions/31-decisions.md).

## Architecture Decision Records

| ADR | Domain | Decision |
|---|---|---|
| [0001 — Polyglot runtime stack](adr/architecture/0001-polyglot-runtime-stack.md) | Architecture | Three languages with explicit, non-overlapping responsibility |
| [0002 — JSONL over stdio](adr/architecture/0002-jsonl-stdio-ipc.md) | Architecture | IPC contract between TUI, CLI, and the Python agent |
| [0003 — Protocol fixtures as contract](adr/contract/0003-protocol-fixtures-as-contract.md) | Contract | JSON fixtures are the single source of truth for three languages |
| [0004 — PyO3 bound bridge](adr/architecture/0004-pyo3-bound-bridge.md) | Architecture | Rust exposed to Python through an `apex_py` extension module |
| [0005 — Skill host subprocess isolation](adr/extensibility/0005-skill-host-subprocess-isolation.md) | Extensibility | Skills run as subprocesses; MCP is a skill type |
| [0006 — Deno-native TypeScript toolchain](adr/toolchain/0006-deno-native-toolchain.md) | Toolchain | `deno fmt` and `deno lint` replace prettier and eslint |

### ADR folder layout

ADRs are grouped by the domain they decide, not by the date they were written.
Grouping by domain keeps related decisions together for a reader asking how IPC
works, regardless of when each was accepted. Grouping by year would scatter
them.

Each domain folder stays at or under five direct files. A domain that reaches
six records gets its own subfolder inside it rather than a rule exception:

```text
docs/operations/adr/
  architecture/    0001 polyglot stack, 0002 stdio IPC, 0004 PyO3 bridge
  contract/        0003 protocol fixtures as contract
  extensibility/   0005 skill host subprocess isolation
  toolchain/       0006 Deno-native TypeScript toolchain
```

## Runbooks

| Runbook | Use when |
|---|---|
| [`runbook/build-and-verify.md`](runbook/build-and-verify.md) | Clean build fails, bridge import fails, tests red |
| [`runbook/bridge-sync.md`](runbook/bridge-sync.md) | `import apex_py` fails after a Rust change |
| [`runbook/release.md`](runbook/release.md) | Cutting a tagged release with binaries and checksums |
