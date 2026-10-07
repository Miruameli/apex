# 35 — System: Git Integration

## Tujuan

Apex ngerti git: status, diff, commit, branch, PR.

## Commands

| Command | Git equivalent | Output |
|---|---|---|
| `apex context` | `git ls-files` + history | JSON context index |
| `apex review` | `git diff` / `git diff --cached` | JSON issues list |
| `apex commit` | `git commit` | Atomic message + commit |
| `apex ship` | `git push` + PR | PR URL / markdown |
| `apex undo` | `git checkout` / stash | Revert last edit |

## Git flow

1. `apex context` → scan file + `git log` terbaru → relevance score
2. `apex review` → `git diff --cached` → LLM review → JSON issues
3. `apex commit` → `git diff --cached` → LLM generate message → `git commit -m`
4. `apex ship` → `git log main..HEAD` → PR description → MCP GitHub create PR

## Git integration tech

- MVP: shell out ke `git` binary
- V1: `git2` crate (Rust) untuk performa + struktur
- V1: `pygit2` (Python) untuk agent logic

## Branch strategy

- `main` = protected
- `feature/<name>` = development
- `apex ship` hanya dari branch non-main

## Undo stack

- Sebelum setiap file edit, backup ke `.apex/cache/backup/<timestamp>/<path>`
- `apex undo` → restore dari backup terakhir
- `apex undo --all` → revert semua edit session

## PR shipment

- MCP GitHub server (V1 nyata, MVP mock)
- PR description template:

```markdown
## Summary
<LLM-generated dari commits>

## Changes
- <commit 1 message>
- <commit 2 message>

## Checklist
- [ ] Tests pass
- [ ] Docs updated
- [ ] No secrets
```
