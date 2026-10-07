# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| main (dev) | ✅ |
| Future releases | ✅ |

## Reporting a Vulnerability

**Jangan buka issue publik untuk kerentanan keamanan.**

Kirim laporan ke: **security@apex.dev** (atau via [GitHub Security Advisories](https://github.com/apex-org/apex/security/advisories/new)).

Sertakan:
- Deskripsi kerentanan
- Langkah reproduksi (jika memungkinkan)
- Dampak potensial
- Versi/komit yang terpengaruh

Kami akan merespons dalam 48 jam dan mengkoordinasikan perbaikan.

## Key Custody Principles

1. **Key LLM hidup di local** — `env` / OS keyring. Tidak pernah di-proxy lewat server Apex.
2. **Hosted relay opsional + warning** — jika nanti ada relay, wajib opt-in dan warning visible.
3. **`.env` di-ignore git** — `.env.example` boleh di-commit, `.env` tidak.
4. **Tidak ada telemetri diam-diam** — analytics opt-in jika ada.

## Approval & Safety

| Fitur | Status |
|-------|--------|
| Approval sebelum edit file | Wajib MVP |
| Diff per hunk (accept/reject) | Wajib MVP |
| Undo/rollback | Wajib MVP |
| Sandbox command | Wajib MVP (minimal: subprocess isolation; Docker V1) |
| Audit log | V1 |
| Budget limit | V1 |

## Trust Model untuk Skill

- Skill pihak ketiga = subprocess terisolasi, bukan in-process.
- Permission eksplisit di manifest (`fs`, `shell`, `net`).
- Host Rust validasi sebelum jalan. Permission violation = abort.
- MCP server = proses terpisah, token via env.

## Threat Model Singkat

| Threat | Mitigasi |
|--------|----------|
| Key bocor via commit | `.env` di-ignore, scan `gitleaks` di CI |
| Skill malicious edit file | Permission `fs` eksplisit, approval wajib, undo |
| LLM halusinasi edit berbahaya | Diff preview + approval + tests jalan sebelum commit |
| Supply chain (MCP) | Pin versi, review manifest, no auto-install |

## Security Gates in CI

- `gitleaks` — secret detection (pre-commit + CI)
- `cargo audit` — Rust dependency vulnerabilities
- `pip-audit` — Python dependency vulnerabilities
- `trivy` — Container image scanning (when Docker used)
- `dependabot` — Automated dependency updates

## Disclosure Policy

- Coordinated disclosure: kami meminta waktu 90 hari untuk memperbaiki sebelum publikasi.
- Credit diberikan kepada pelapor (kecuali anonime).
- CVE dimintakan untuk kerentanan yang memenuhi syarat.