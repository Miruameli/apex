# ADR-0008: TUI Library Selection — OpenTUI

## Status
Accepted

## Context
Apex requires a terminal UI library for the `apex` TUI command (lazygit-style split-panel interface). The TUI must support:
- Split panels (file tree, diff view, chat, status bar)
- Flexbox/Yoga-based layout
- Keyboard-driven navigation
- Themeable components
- In-memory testing for CI
- Deno 2.x native support
- Zero npm dependencies (per ADR-0006)

Three options evaluated:

| Option | Type | Layout Engine | Split Panels | Deno 2.x | Testing | Production Use |
|--------|------|---------------|--------------|----------|---------|----------------|
| **OpenTUI** | Zig core + TS bindings | Yoga/Flexbox (native) | ✅ Built-in | ✅ Native | ✅ In-memory | ✅ OpenCode |
| Cliffy | TS CLI framework | None (prompts only) | ❌ | ✅ | ❌ | CLI tools only |
| Deno stdlib (raw ANSI) | Manual | Manual | Manual | ✅ | Manual | None |

## Decision
**Select OpenTUI** (`@opentui/core`, `@opentui/react`, `@opentui/solid`) as the TUI library.

- Core imperative API for full control
- React/Solid bindings for component-based UI
- Native Zig core via FFI — performant, no WASM overhead in Deno 2.x
- Flexbox layout via Yoga — lazygit-style split panels native
- In-memory renderer for snapshot testing in CI
- Powers OpenCode in production — proven at scale
- Deno 2.x compatible via JSR (`jsr:@opentui/*`)

## Alternatives Considered

### Cliffy (`@cliffy/*`)
- **Pros**: Deno-native, mature prompt library, command parsing built-in
- **Cons**: No layout engine, no split panels, no flexbox — only prompts/CLI. Would require building entire layout system from scratch (months of work).

### Deno Standard Library (raw ANSI)
- **Pros**: Zero dependencies, full control, minimal
- **Cons**: Building split-panel layout, input handling, focus management, theme system = reinventing OpenTUI. 3-6 months to reach parity. No testing utilities.

## Consequences

### Positive
- LazyGit-style UI achievable in weeks, not months
- Production-proven core (OpenCode)
- In-memory testing = reliable CI
- Themeable via CSS-like styling
- React/Solid bindings match team skills

### Negative
- Zig FFI dependency — but Deno 2.x handles this natively
- Newer ecosystem — smaller community than Cliffy
- Learning curve for Yoga/Flexbox layout model

## Justification
OpenTUI is the **only** option providing native split-panel flexbox layout — the core requirement for lazygit-style TUI. Cliffy and stdlib lack layout primitives entirely. Building layout from scratch violates "progress > speed" (months of infra before features).

## Date
2026-10-07

## Author
Apex Executive

## Review Date
2026-11-07