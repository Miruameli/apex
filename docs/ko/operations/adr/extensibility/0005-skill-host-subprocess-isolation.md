<!--
ADR 0005 — Why skills are SKILL.md plus a script run as a subprocess, and why
MCP is a skill type rather than a separate runtime.

File purpose: record the accepted extension model for Apex: a Rust host that
validates a manifest, enforces permissions, and spawns the skill as an
isolated subprocess, with MCP expressed as `type: "mcp"` inside the same
manifest format instead of a second plugin system.

An accepted ADR is immutable. Do not edit it to change its decision. Supersede
it with a new ADR that references this file number instead.
-->

# ADR 0005 — Skill host berbasis subprocess

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-10-07 |
| Author | Apex Contributors |
| Review Date | 2027-01-07 |

## Konteks

Apex perlu bisa diperluas tanpa mengubah binary inti: connector ke layanan
eksternal, skill khusus proyek, dan integrasi MCP. Pertanyaannya adalah batas
plugin.

Dua batasan menentukan bentuknya. Pertama, solo developer harus bisa menulis
skill tanpa harus menyiapkan toolchain kompilasi Rust. Kedua, kode skill adalah
kode pihak ketiga yang berjalan dengan hak akses pengguna; ia tidak boleh bisa
menjatuhkan agent dan tidak boleh bisa melewati permission yang dideklarasikan.

Dua model awal saling bertentangan: satu memilih `skills_runtime` sebagai Rust
native plugin, satu lagi `skills_format` sebagai `SKILL.md` plus script.
Keduanya tidak bisa berlaku bersamaan, jadi harus dipilih satu arah.

## Keputusan

**Host = Rust. Authoring = `SKILL.md` plus script. Eksekusi = subprocess.**

Satu skill adalah folder dengan tiga jenis file:

```
skills/<nama>/
  SKILL.md        # deskripsi manusia dan instruksi untuk agent
  apex.skill.json # manifest mesin: nama, versi, entrypoint, runtime, permission
  main.py         # atau main.ts, atau binary
```

`SKILL.md` dibaca model sebagai konteks; `apex.skill.json` dibaca host sebagai
kontrak. Pemisahan ini disengaja: deskripsi ditulis orang, mesin tidak perlu
memahami markdown, dan model tidak perlu memvalidasi JSON.

**Tanggung jawab host Rust, tanpa registry kedua.** Urutannya adalah validasi
manifest, enforcement permission, spawn subprocess, lalu routing JSONL dengan
protokol yang sama seperti agent. Registry skill tetap milik satu tempat,
sehingga tidak ada salinan yang bisa drift antara Rust dan Python.

**Permission dideklarasikan di manifest dan diperiksa sebelum menjalankan.**
Manifest menyebut scope `fs`, `shell`, dan `net`. Host memeriksanya sebelum
spawn; pelanggaran menghasilkan event `Error` dan skill dibunuh, bukan dijalankan
lalu diawasi. Pada MVP, batas isolasi adalah level 1, yaitu pemeriksaan
permission plus isolasi subprocess. Level yang lebih ketat, yaitu cgroups,
seccomp, container, lalu VM, dicadangkan untuk versi berikutnya.

**MCP adalah tipe skill, bukan runtime terpisah.** Field `type` pada manifest
membedakan `"skill"` dari `"mcp"`. Untuk `type: "mcp"`, host tetap melakukan
langkah yang sama dan tetap menjalankan MCP server sebagai subprocess, hanya
sasarannya adalah server JSON-RPC di stdio, bukan script milik skill.

## Alternatif yang Dipertimbangkan

**Plugin Rust native sebagai cdylib.** Plugin dimuat lewat PyO3, sama seperti
bridge. Ditolak karena setiap skill wajib dikompilasi terhadap toolchain yang
sama dengan `apex-py`, jadi penulis skill tidak bisa memakai bahasa pilihan
mereka, dan satu plugin yang error menjatuhkan seluruh agent karena berada di
proses yang sama.

**Skill Python in-process.** Skill dipanggil sebagai fungsi Python biasa.
Ditolak karena tidak ada batas proses yang bisa dilanggar, sehingga
enforcement permission hanya berupa konvensi, dan skill yang crash berarti
agent ikut crash.

**Runtime MCP terpisah.** MCP connector menjadi subsistem sendiri dengan
manajemen proses, skema, dan daftarnya sendiri. Ditolak karena mengulang
mekanisme yang sudah ada: manifest, permission, spawn, JSONL. Satu format
manifest membuat skill biasa dan MCP connector berbeda hanya pada nilai `type`,
sehingga tidak ada konsep yang harus dipelajari dua kali.

**WASM untuk plugin.** Terisolasi dan tidak butuh toolchain. Ditolak karena
membawa runtime-nya sendiri beserta model isolasi yang harus ditulis ulang,
padahal subprocess sudah memberi batas proses dengan harga nol.

**Tidak melakukan apa-apa, memakai konfigurasi saja.** Ditolak karena
konfigurasi saja tidak bisa menjalankan kode yang benar-benar perlu, misalnya
menjalankan deploy atau memanggil layanan internal.

## Konsekuensi

**Biaya yang diterima:**

- **Overhead proses per skill.** Spawn subprocess jauh lebih mahal daripada
  panggilan fungsi, jadi kerja yang harus tetap di dalam proses dilakukan di
  core, bukan di skill.
- **Redundansi format.** Penulis skill harus menghasilkan dua file yang
  konsisten, `SKILL.md` dan `apex.skill.json`. Validasi manifest di host
  menjaga kedua file itu tetap sinkron.
- **Isolasi belum impenetrabel pada MVP.** Pemeriksaan permission plus
  subprocess menahan kegagalan, tetapi proses skill masih punya hak akses
  filesystem pengguna. Batas yang lebih kuat belum ada, dan itu harus
  disadari pengguna sebelum skill pihak ketiga dipasang.
- **Runtime skill harus ada di mesin.** Skill Python butuh Python; skill
  TypeScript butuh Deno atau Node. Host resolve runtime dari manifest, tetapi
  kegagalan runtime adalah kesalahan konfigurasi lingkungan.

**Manfaat yang didapat:**

- Satu format untuk skill biasa dan MCP connector.
- Penulisan skill tanpa toolchain Rust.
- Kegagalan skill terisolasi dari agent.
- Permission yang bisa divalidasi sebelum kode berjalan.