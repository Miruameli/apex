# 22 — System: CLI

## Command surface (standar Apex)

```
apex <command> [options]

Commands:
  chat <msg>       Chat dengan agent (streaming)
  context [root]   Scan codebase → index
  review           Review diff (staged/branch)
  commit           Generate atomic commit message
  ship             Buat PR + update changelog
  skill add <name> Scaffold skill
  skill list       List skills
  skill run <name> Run skill
  skill validate   Validate manifest
  tui              Launch TUI (default jika no args)
  init             Scan project, tulis APEX.md + apex.json
  config           Edit apex.json
```

## Flags global

- `--config <path>` — path ke apex.json custom
- `--verbose` / `-v` — debug log ke stderr
- `--quiet` / `-q` — hanya output essential
- `--json` — machine-readable output

## Output konvensi

- stdout = data (JSONL events atau plain result)
- stderr = log, banner, debug
- Exit code: 0 ok, 1 error, 2 usage error

## Parsing

Rust `clap` derive (apex-cli). Subcommand struct per command.

## Embedding

- `apex-cli` binary Rust
- Python `apex.agent` sebagai library untuk `ApexAgent.handle()`
- TS TUI sebagai separate process (JSONL IPC ke Python agent)
