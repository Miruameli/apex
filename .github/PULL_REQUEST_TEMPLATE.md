# Pull Request Template

## Problem Statement

**Masalah:** apa yang diperbaiki/ditambah?
**Dampak:** siapa yang terpengaruh? (user, kontributor, CI, dll.)
**Bukti:** link issue, log, screenshot, benchmark

---

## Approach

**Pendekatan:** deskripsi singkat solusi yang diambil
**File utama yang diubah:**
- `path/to/file.rs` — alasan
- `path/to/file.py` — alasan

---

## Alternatives Considered

- **Alternatif 1:** ... — alasan ditolak
- **Alternatif 2:** ... — alasan ditolak

---

## Risks & Mitigations

| Risiko | Mitigasi | Rollback Plan |
|--------|----------|---------------|
| Contoh: Breaking change protocol | Version bump, migration guide | Revert commit, tag hotfix |

---

## Verification

- [ ] **Test lulus** — `./scripts/verify.sh` hijau lokal
- [ ] **CI hijau** — semua job di GitHub Actions pass
- [ ] **Security scan lulus** — gitleaks, cargo audit, pip-audit bersih
- [ ] **Self-review selesai** — baca ulang diff, cek bug/security/perf/estetika
- [ ] **Dokumentasi diperbarui** — README, docs, CHANGELOG, comment kode
- [ ] **Comment lengkap** — file header, doc comment public API, inline untuk logika kompleks
- [ ] **Modularisasi OK** — max 5 file/folder, max 150 SLOC, distribusi merata
- [ ] **Distribusi file merata** — tidak menumpuk di satu layer
- [ ] **Memory di-update** — jika ada pembelajaran baru / pola baru

---

## Related Issues

- Closes #XXX
- Refs #YYY

---

## Screenshots / Demo (jika UI)

<!-- Drag & drop screenshot atau link asciinema -->

---

## Checklist Tambahan (opsional)

- [ ] Breaking change terdokumentasi di CHANGELOG + ADR jika arsitektur
- [ ] Migration guide ditulis (jika breaking)
- [ ] Benchmark dijalankan (jika perf-sensitive)
- [ ] Test flaky tidak ditambahkan
- [ ] Dependency baru: lisensi OK, audit bersih, ADR jika signifikan