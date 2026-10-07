# 14 — Governance

## Pengambilan keputusan

- **Keputusan kecil** (bug fix, doc, typo): langsung PR, 1 maintainer approve.
- **Keputusan menengah** (fitur baru di scope MVP): issue discussion, minimal 1 maintainer + 1 kontributor aktif setuju.
- **Keputusan besar** (ubah stack, rename, ubah protocol, pivot produk): RFC di `docs/community/rfc/`, diskusi minimal 7 hari, mayoritas maintainer setuju.

## Maintainer

- Saat ini: Solo founder (lu).
- Open untuk contributors. Path: kontributor aktif → co-maintainer → maintainer.

## RFC process

1. Tulis RFC di `docs/community/rfc/NNN-title.md` dengan: masalah, opsi, trade-off, keputusan, dampak.
2. Label `rfc` di GitHub.
3. Diskusi minimal 7 hari.
4. Final: merge RFC, tulis ADR di `docs/operations/adr/`, buat issue implementasi.

## Transparansi

- Semua diskusi teknis di GitHub issues/PRs, bukan DM privat (kecuali keamanan).
- Keputusan yang mempengaruhi user dicatat di `CHANGELOG.md` dan docs.
- Roadmap di-update per release.
