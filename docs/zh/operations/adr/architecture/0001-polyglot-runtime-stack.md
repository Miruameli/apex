<!--
ADR 0001 — Why Apex runs on three languages instead of one.

File purpose: record the accepted architectural decision that splits Apex
across Python (brain), Rust (speed core), and TypeScript (TUI), together with
the alternatives that were rejected and the costs this choice imposes.

An accepted ADR is immutable. Do not edit it to change its decision. Supersede
it with a new ADR that references this file number instead.
-->

# ADR 0001 — Polyglot Runtime Stack

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-10-07 |
| Author | Apex Contributors |
| Review Date | 2027-01-07 |

## Konteks

Apex adalah terminal AI coding agent. Beban kerjanya tidak seragam, dan tiga
beban itu punya kebutuhan yang berbeda:

1. **Orkestrasi LLM.** Memanggil model, menyusun prompt, melakukan streaming
   token, memakai pustaka client yang sudah matang. Ekosistem Python untuk
   ini paling lengkap.
2. **Pekerjaan berat.** Memindai file, mem-parse, membangun index, membaca
   `git diff`, memvalidasi protokol. Butuh cepat pada banyak file, dengan
   keamanan tipe.
3. **UI interaktif terminal.** Butuh event loop, redraw, dan input keyboard yang
   responsif di dalam terminal.

Memilih satu bahasa berarti memaksa salah satu beban untuk memakai alat yang
tidak dirancang untuknya, atau membawa toolchain kedua lewat FFI tanpa batas
tanggung jawab yang jelas.

## Keputusan

Apex memakai tiga bahasa, dengan batas tanggung jawab yang eksplisit dan tidak
tumpang tindih:

| Bahasa | Peran | Yang menjadi tanggung jawabnya | Yang dilarang |
|---|---|---|---|
| Python 3.12 | Otak (brain) | Orkestrasi LLM, prompt, streaming, registry tool di `apex/tools/` | Loop IO berat dan pemindaian file besar |
| Rust (`edition 2024`, `resolver = "3"`) | Speed core | Pemindaian konteks, protokol, session, skill host | Panggilan LLM dan terminal I/O |
| TypeScript no-build (Deno) | UI | TUI interaktif, render event, input keyboard | Logika agent yang berat |

Batas "Rust bebas dari panggilan LLM" ditegakkan di source: modul
`crates/apex-core/src/lib.rs` mendeklarasikan bahwa `apex-core` harus tetap
bebas dari panggilan LLM dan terminal I/O. Batas ini mencegah core perlahan
menjadi otak kedua, yang akan memaksa kontrak protokol dipelihara di dua
orchestrator.

Registry tool tetap tunggal di Python. Host Rust hanya melakukan empat hal:
validasi manifest, enforce permission, spawn subprocess, dan routing protokol.
Tidak ada registry tool kedua di Rust yang bisa drift.

Workspace Rust berisi tiga crate, yaitu `apex-core`, `apex-cli`, dan `apex-py`
(lihat `Cargo.toml` di root). TUI TypeScript berdiri sendiri di `tui/` dengan
`deno.json`.

## Alternatif yang Dipertimbangkan

**Python saja.** Toolchain paling sedikit, dan orkestrasi LLM berjalan secara
alami. Ditolak karena pemindaian konteks dan diff adalah jalur panas yang
berjalan setiap permintaan; membawanya ke Python berarti lambat tepat di tempat
yang dirasakan pengguna. UI terminal di Python juga tidak punya model interaktif
yang baik.

**Rust saja.** Satu toolchain, satu binary, performa terbaik. Ditolak karena
ada dua hal yang akan mengikis waktu solo developer lebih besar daripada biaya
toolchain tambahan: klien LLM berdataran tinggi, dan iterasi cepat saat prompt
diubah. Klien tersebut terus berubah, dan produktivitas di loop prompt adalah
inti produk ini.

**Go + Rust.** Go untuk daemon, Rust untuk core. Ditolak karena menambahkan
bahasa keempat tanpa lapisan baru yang nyata, sebab daemon sudah bisa berjalan
menjadi satu subprocess Python yang mengeluarkan JSONL.

**Dua bahasa, Rust + TypeScript tanpa Python.** Ditolak karena orkestrasi LLM
tidak masuk akal di Rust. Alternatifnya memanggil model lewat HTTP mentah,
yang mengulang pekerjaan yang sudah selesai dan dikerjakan pustaka Python.

**Tidak melakukan apa-apa, tetap mono-bahasa.** Ditolak karena menarik ketiga
beban ke satu bahasa membuat toolchain lebih murah, tetapi risiko penulisan
ulang yang jauh lebih besar saat kebutuhan berubah.

## Konsekuensi

**Biaya yang diterima:**

- **Tiga toolchain.** Rust, Python via `uv`, dan Deno harus terpasang dengan
  versi yang cocok. CI memasang ketiganya dan menjalankan tiga suite test
  terpisah, sebagaimana terlihat di `.github/workflows/quality.yml`.
- **Pemeliharaan kontrak lintas bahasa.** Protokol harus dicerminkan di
  `protocol.rs`, `protocol.py`, dan `protocol.ts`. ADR-0003 menjelaskan bagaimana
  drift ini ditangkap secara otomatis.
- **Batas tanggung jawab ditegakkan lewat kode dan review.** Aturan "Rust tidak
  memanggil LLM" bukan alat otomatis, melainkan aturan yang dijaga oleh
  struktur crate dan review kode.
- **Titik integrasi tambahan.** Python mencapai Rust lewat bridge PyO3, yang
  membutuhkan build step; lihat ADR-0004.

**Manfaat yang didapat:**

- Jalur panas berada di bahasa yang memang cepat untuk tugas itu.
- Bahasa yang tepat untuk orkestrasi LLM.
- Iterasi UI tanpa build step.

**Resiko yang harus diawasi:** dibanding proyek mono-bahasa, satu fitur sering
menyentuh lebih dari satu bahasa. Onboarding dan review kode menjadi lebih
berat, dan itu adalah harga yang dibayar untuk kecepatan di jalur panas.