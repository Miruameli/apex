# 09 — Security & Key Custody

## Prinsip key-custody

1. **Key LLM hidup di local** — `env` / OS keyring. Tidak pernah di-proxy lewat server Apex.
2. **Hosted relay opsional + warning** — jika nanti ada relay, wajib opt-in dan warning visible.
3. **`.env` di-ignore git** — `.env.example` boleh di-commit, `.env` tidak.
4. **Tidak ada telemetri diam-diam** — analytics opt-in jika ada.

## Approval & safety

| Fitur | Status |
|---|---|
| Approval sebelum edit file | Wajib MVP |
| Diff per hunk (accept/reject) | Wajib MVP |
| Undo/rollback | Wajib MVP |
| Sandbox command | Wajib MVP (minimal: subprocess isolation; Docker V1) |
| Audit log | V1 |
| Budget limit | V1 |

## Trust model untuk skill

- Skill pihak ketiga = subprocess terisolasi, bukan in-process.
- Permission eksplisit di manifest (`fs`, `shell`, `net`).
- Host Rust validasi sebelum jalan. Permission violation = abort.
- MCP server = proses terpisah, token via env.

## Threat model singkat

| Threat | Mitigasi |
|---|---|
| Key bocor via commit | `.env` di-ignore, scan `gitleaks` di CI (V1) |
| Skill malicious edit file | Permission `fs` eksplisit, approval wajib, undo |
| LLM halusinasi edit berbahaya | Diff preview + approval + tests jalan sebelum commit |
| Supply chain (MCP) | Pin versi, review manifest, no auto-install |
