# 53 — RFC Process & Template

## Kapan butuh RFC

- Ubah protocol (breaking change)
- Ubah stack/tech major
- Rename produk/command
- Pivot produk direction
- Decision yang affect banyak subsystem

Tidak butuh RFC: bug fix, doc update, typo, minor feature dalam scope MVP.

## Template RFC

```markdown
# RFC-NNN: <Title>

## Status
Draft / Accepted / Rejected / Superseded

## Context
<Masalah apa yang dipecahkan? Data/bukti?>

## Options considered
1. Option A: ...
2. Option B: ...
3. Option C: (do nothing)

## Decision
<Option mana yang dipilih + alasan>

## Trade-offs
| Option | Pro | Kontra |
|---|---|---|

## Implementation plan
- [ ] Task 1
- [ ] Task 2

## Impact
- Breaking change? (ya/tidak)
- Migration path?
- Docs untuk update?

## Discussion
<Link ke GitHub issue>
```

## Proses

1. Tulis RFC di `docs/community/rfc/NNN-title.md` (status `Draft`)
2. Label `rfc` di GitHub issue
3. Diskusi minimal 7 hari
4. Accepted: buat ADR di `docs/operations/adr/` dan issue implementasi
5. Implementasi sesuai plan
6. Update `docs/operations/decisions/31-decisions.md`

## Lokasi

```
docs/community/rfc/       # proposal yang sedang dibahas
docs/operations/adr/      # keputusan yang sudah final
```
