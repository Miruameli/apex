<!--
ADR 0003 — Why tests/fixtures/protocol/ is the single source of truth.

File purpose: record the accepted decision that the JSON fixtures, not any
language module, define the protocol contract, and that all three language
implementations must round-trip those same fixtures with a deep-equal
comparison on parsed JSON rather than on raw strings.

An accepted ADR is immutable. Do not edit it to change its decision. Supersede
it with a new ADR that references this file number instead.
-->

# ADR 0003 — Protocol fixtures sebagai kontrak

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-10-07 |
| Author | Apex Contributors |
| Review Date | 2027-01-07 |

## Konteks

ADR-0001 memutuskan bahwa Apex memakai tiga bahasa. Konsekuensinya, satu kontrak
protokol harus punya tiga implementasi: `protocol.rs` di Rust, `protocol.py` di
Python, dan `protocol.ts` di TypeScript. Tiga salinan definisi yang sama adalah
tiga tempat drift bisa dimulai, dan drift pada kontrak protokol berarti TUI
menampilkan state yang salah tanpa error yang terlihat.

Ada dua pertanyaan yang harus dijawab. Pertama, apa yang menjadi sumber
kebenaran kontrak itu. Kedua, bagaimana cara membuktikan ketiga implementasi
tetap konsisten dengan sumber itu secara otomatis.

## Keputusan

**`tests/fixtures/protocol/` adalah satu-satunya sumber kebenaran.** Fixture
adalah data, bukan kode, sehingga tidak ada bias implementasi di dalamnya. Isi
folder saat ini:

```
tests/fixtures/protocol/
  requests/            chat, fix, review, context
  events/stream/       thinking, toolcall, diff, message
  events/terminal/     done, error
```

Modul `protocol.rs`, `protocol.py`, dan `protocol.ts` adalah mirror, bukan
definisi. Kalau bentuk payload berubah, fixture yang diubah lebih dulu; modul
yang belum menyesuaikan akan gagal test.

**Bukti kesetaraan: round-trip dengan deep-equal pada JSON yang sudah di-parse.**
Setiap fixture diuji dengan urutan yang sama di ketiga bahasa:

1. Baca file fixture sebagai JSON.
2. Parse dengan parser milik bahasa itu sendiri.
3. Serialize ulang.
4. Parse ulang hasil serialisasi.
5. Bandingkan dengan nilai JSON asli memakai deep-equal.

Urutannya penting. Langkah kedua membuktikan parser bisa menerima fixture,
langkah ketiga sampai kelima membuktikan bentuk data yang dihasilkan parser
sama dengan yang diminta kontrak.

**Perbandingan dilakukan pada JSON hasil parse, bukan pada string mentah.**
Alasan ini praktis, bukan sekadar selera. Dua objek dengan kunci yang sama tetapi
urutan berbeda adalah nilai yang sama, dan urutan kunci tidak pernah menjadi
bagian dari kontrak. Membandingkan string mentah akan membuat test gagal karena
hal yang tidak pernah penting, lalu mendorong orang untuk memperbarui snapshot
tanpa memperbaiki apa pun.

Implementasi saat ini: test Rust berada di unit test `protocol.rs`, test Python
di `tests/python/test_protocol.py`, dan test TypeScript di
`tui/src/protocol_test.ts`. Ketiganya membaca folder fixture yang sama, dan
ketiganya dijalankan sebagai bagian dari CI.

## Alternatif yang Dipertimbangkan

**Test yang ditulis tangan per bahasa.** Setiap bahasa punya test sendiri dengan
contoh sendiri. Ditolak karena tidak ada yang membuktikan ketiganya konsisten.
Tiga test yang sama-sama hijau tetap bisa tidak kompatibel satu sama lain,
sehingga bug yang paling mahal justru lolos tanpa terdeteksi.

**Schema-first dengan codegen.** Tulis JSON Schema sekali, generate tipe untuk
ketiga bahasa. Ditolak karena menambah toolchain codegen, langkah generated code
dalam build, dan kompleksitas yang berbeda per runtime. Untuk payload sekecil
`{"type": "Chat", "message": "..."}`, harga itu tidak sepadan dengan
manfaatnya. Fixture plus test memberi jaminan yang sama dengan dependensi jauh
lebih sedikit.

**Snapshot file per bahasa.** Simpan output yang diharapkan untuk setiap
implementasi. Ditolak karena membuat tiga sumber kebenaran baru, dan karena
snapshot bisa diperbarui tanpa disadari, persis jenis drift yang paling sulit
dilacak.

**Tidak melakukan apa-apa, andalkan review kode saja.** Ditolak karena review
tidak menangkap perubahan yang tidak konsisten di file berbeda pada PR yang
sama.

## Konsekuensi

**Biaya yang diterima:**

- **Pemeliharaan fixture.** Menambah varian payload berarti menambah file fixture
  di subfolder yang sesuai. Ini biaya berulang setiap kali kontrak berkembang.
- **Tiga implementasi tetap harus sinkron.** Fixture mendeteksi drift, tetapi
  tidak menghilangkannya; masih ada tiga file yang harus diubah per perubahan
  kontrak.
- **Kontrak diuji, bukan disimulasikan.** Test membuktikan bentuk data benar,
  bukan bahwa alur TUI menampilkannya dengan benar. Lapisan di atas fixture
  tetap perlu pengujian sendiri.

**Manfaat yang didapat:**

- Drift kontrak gagal di CI, bukan di tangan pengguna.
- Sumber kebenaran dapat dibaca manusia tanpa menjalankan kode apa pun.
- Menambah request atau event baru adalah operasi yang jelas: tambah fixture,
  tambah tipe, tambah asersi.
- Ukuran kontrak terlihat langsung di `git diff`.