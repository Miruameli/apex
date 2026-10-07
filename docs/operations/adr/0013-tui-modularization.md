# ADR-0013: TUI Source Modularization

## Status
Accepted

## Context

The `tui/src/` directory contained four flat TypeScript files with no
layered separation of concerns:

```
tui/src/
├── parse.ts      (157 SLOC — exceeds 150 SLOC limit)
├── parse_test.ts (122 SLOC)
├── protocol.ts   (70 SLOC)
└── main.ts        (6 SLOC)
```

Two violations of the Apex modularization rules:

1. `parse.ts` exceeded the 150 SLOC maximum by 7 lines.
2. The flat structure placed domain types, validation logic, and entry
   point in the same folder, violating "one folder = one domain."

## Decision

Restructure `tui/src/` into a 5-layer architecture following the Apex
7-layer standard, colocating tests with their source module:

```
tui/src/
├── domain/                    (pure interface types)
│   └── protocol.ts            ~68 SLOC
├── application/               (public parse API + tests)
│   ├── parser.ts              ~25 SLOC
│   └── parser_test.ts         ~95 SLOC
├── infrastructure/            (validation implementation)
│   └── validation/
│       ├── contract.ts        ~66 SLOC (Field, USAGE_FIELDS, REQUEST_FIELDS, EVENT_FIELDS)
│       └── rules.ts           ~65 SLOC (lookupFields, hasKind, firstViolation, parseLine)
├── shared/                    (cross-cutting error type)
│   └── error.ts               ~10 SLOC (ProtocolError)
└── interfaces/                (entry point)
    └── main.ts                ~8 SLOC
```

**Layer mapping (Apex 7-layer standard):**

| Layer           | Folder             | Responsibility                          |
|-----------------|--------------------|-----------------------------------------|
| Domain          | `domain/`          | Pure wire-type definitions              |
| Application     | `application/`     | Public parse API, orchestration        |
| Infrastructure  | `infrastructure/`  | Validation primitives & contract data   |
| Shared          | `shared/`          | Cross-cutting error types              |
| Interfaces      | `interfaces/`      | TUI entry point                         |

### Splitting rationale for `parse.ts` (157 → 4 files)

| Segment              | Destination                     | SLOC |
|----------------------|---------------------------------|------|
| `ProtocolError`      | `shared/error.ts`               | 10   |
| `Field` + field tables | `infrastructure/validation/contract.ts` | 66 |
| `lookupFields`, `hasKind`, `firstViolation`, `parseLine` | `infrastructure/validation/rules.ts` | 65 |
| `parseRequest`, `parseEvent` | `application/parser.ts`     | 25   |

### Colocated tests

`parser_test.ts` lives in `application/` alongside `parser.ts`, matching
Deno convention of `<module>_test.ts` colocated with its source. The test
path changed from `../../tests/fixtures/protocol/` to
`../../../tests/fixtures/protocol/` to reflect the deeper nesting.

### Import path updates

- `tui/deno.json` `exports` updated to `./src/interfaces/main.ts`.
- `scripts/verify.sh` `deno check` target updated to
  `tui/src/interfaces/main.ts`.

## Alternatives Considered

1. **Keep flat structure, split parse.ts only** — Would fix the SLOC
   violation but perpetuate the "one folder = one domain" violation.

2. **Add index.ts barrel files** — Would centralize re-exports but
   adds indirection and increases file count per folder, risking the
   5-file limit in smaller layers. Rejected: direct imports are
   explicit and searchable.

## Consequences

- Each file has a single, clear responsibility.
- No file exceeds 150 SLOC (max: `parser_test.ts` at ~95 SLOC).
- No folder exceeds 5 direct files or 5 direct subfolders.
- Files are distributed across 5 layers (not concentrated in one).
- Import paths are one level deeper but semantically clear.
- Tests are colocated with source (Deno convention).
- `deno.json`, `verify.sh` updated to reference new paths.

## Verification

- `deno fmt --check tui/src` → ok
- `deno lint tui/src` → ok
- `deno check tui/src/interfaces/main.ts` → ok
- `deno test --allow-all tui/src` → 20 passed, 0 failed
- `check_modularization.py` → Modularization OK

## Date: 2026-10-08
## Author: Apex (autonomous)
## Review Date: 2026-11-08
