# 54 — Security Policy

## Laporan vulnerability

- JANGAN buat public issue untuk security bug
- Email ke: security@apex.dev (TBD) atau DM maintainer
- Sertakan: deskripsi, repro steps, impact assessment

## SLA

| Severity | Response | Fix target |
|---|---|---|
| Critical | ≤ 24 jam | ≤ 72 jam |
| High | ≤ 72 jam | ≤ 1 minggu |
| Medium | ≤ 1 minggu | ≤ 1 bulan |
| Low | ≤ 1 bulan | backlog |

## Scope

In-scope:
- Semua komponen Apex (Rust, Python, TS)
- Protocol IPC
- Skill runtime
- MCP client
- Bridge PyO3

Out-of-scope:
- Vulnerability di dependency upstream (laporkan ke mereka)
- Social engineering
- Physical access

## Supported versions

| Version | Supported |
|---|---|
| 0.x (current) | ✅ |
| 1.x (future) | TBD |

## Security updates

- Critical/High: immediate patch release
- Medium/Low: next scheduled release
- Public advisory setelah fix deployed

## Bug bounty

TBD — tidak ada di fase awal.
