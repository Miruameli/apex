# 24 — System: Security (detail)

## Key custody

- LLM key: `env` (`APEX_KEY`) atau OS keyring (V1)
- No proxy default: key tidak pernah dikirim ke server Apex
- `.env` di-ignore git, `.env.example` boleh di-commit
- Relay hosted: opt-in + warning banner

## Approval & safety gates

| Aksi | Gate |
|---|---|
| Edit file | Diff preview → `a/r` per-hunk → confirm |
| Shell command | Show command → `y/n` confirm |
| Skill run | Permission check → spawn |
| MCP tool call | Permission check → route |
| `apex ship` | PR description review → create |
| `apex commit` | Message preview → confirm |

## Sandbox levels

| Level | Mekanisme | Status |
|---|---|---|
| 0 | None (percaya skill) | Tidak dipakai |
| 1 | Permission check + subprocess isolation | MVP |
| 2 | cgroups/seccomp | V1 |
| 3 | Docker container | V1 |
| 4 | VM | V2 |

## Audit log (future)

- Setiap file edit, shell exec, skill run dicatat di `.apex/logs/audit.jsonl`
- Format: `{timestamp, action, target, approved_by, result}`
- Tidak log secret/PII

## Threat mitigations

| Threat | Mitigasi |
|---|---|
| Secret bocor via commit | `.env` ignored, CI scan `gitleaks` (V1) |
| Malicious skill edit file | Permission `fs` eksplisit + approval + undo |
| LLM halusinasi edit | Diff preview + approval + tests before commit |
| Supply chain MCP | Pin versi, review manifest, no auto-install |
| Code injection via skill args | Parameterized args, no shell interpolation |

## Rollback

- Setiap edit punya undo stack
- `apex undo` → revert last edit
- File backup otomatis sebelum edit (`.apex/cache/backup/`)
