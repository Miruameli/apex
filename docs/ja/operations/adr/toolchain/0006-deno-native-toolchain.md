<!--
ADR 0006 — Why the TypeScript toolchain is deno fmt + deno lint, not prettier + eslint.

File purpose: record the accepted decision that the formatter and linter of
record for the TUI are the ones built into Deno, that TypeScript dependencies
are declared in tui/deno.json rather than inline, and that a root deno.json
workspace exists so root-relative commands resolve the same imports CI sees.

An accepted ADR is immutable. Do not edit it to change its decision. Supersede
it with a new ADR that references this file number instead.
-->

# ADR 0006 — Toolchain TypeScript Bawaan Deno

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-10-07 |
| Author | Apex Contributors |
| Review Date | 2027-01-07 |

## Konteks

ADR-0001 menetapkan TUI sebagai TypeScript no-build dengan Deno sebagai
runtime. "No-build" berarti tidak ada bundler, tidak ada `tsc`, dan tidak ada
`node_modules`. Pertanyaan yang harus diputuskan: formatter dan linter apa yang
menjadi sumber kebenaran gaya kode TypeScript di repo ini.

Dua kandidat tersedia, dan keduanya lazim dipakai:

| Kandidat | Path | Konsekuensi |
|---|---|---|
| `prettier` + `eslint` | `npm i -D` sehingga muncul `node_modules` | Memunculkan pohon dependensi npm |
| `deno fmt` + `deno lint` | Bawaan binary Deno | Tanpa dependensi tambahan |

Yang menentukan bukan selera, melainkan konsekuensi terhadap ADR-0001.
`prettier` hanya bisa dijalankan lewat npm, dan npm selalu memasang tree
`node_modules` beserta lockfile-nya. Memakainya berarti mengembalikan dependensi
yang justru dihapus oleh keputusan "no-build".

Ada bukti langsung dari kegagalan nyata. Sebelum keputusan ini diambil,
`deno lint` gagal pada `tui/src/protocol_test.ts` dengan dua aturan yang hanya
aktif di Deno: `no-unversioned-import` dan `no-import-prefix`. Kedua aturan itu
justru mencegah dependensi yang tidak terpin dan import inline yang
bertentangan dengan aturan penguncian versi. Perbaikannya — memindahkan
`jsr:@std/assert@1.0.19` ke peta `imports` di `tui/deno.json` — adalah idiom
Deno, bukan idiom npm.

## Keputusan

**`deno fmt` adalah formatter TypeScript yang sahih, dan `deno lint` adalah
linter yang sahih.** Keduanya datang dari binary Deno yang sama dengan runtime
TUI, jadi tidak ada tool kedua yang bisa berbeda pendapat tentang hasil format.

**Tidak ada konfigurasi prettier atau eslint di repo ini.** Berkas
`.prettierrc.json` dan `.prettierignore` pernah ada lalu dihapus, karena
mendokumentasikan tool yang tidak dijalankan gate mana pun hanya memunculkan
konfigurasi tanpa pemanggil.

**Dependency TypeScript dideklarasikan di `tui/deno.json`, bukan inline di
baris import.** Specifier inline ditolak oleh `no-import-prefix`. Peta `imports`
membuat versi terlihat di satu tempat dan menghasilkan `deno.lock` dengan hash
integritas:

```json
{
  "imports": {
    "@std/assert": "jsr:@std/assert@1.0.19"
  }
}
```

Baris import lalu memakai bare specifier:

```typescript
import { assertEquals } from "@std/assert";
```

**`deno.json` di root mendeklarasikan workspace `tui`.** Tanpa ini, perintah
Deno yang dijalankan dari root — termasuk yang dipakai CI — tidak membaca
`imports` milik `tui/deno.json`, karena Deno mencari konfigurasi berdasarkan
direktori kerja, bukan lokasi entry point. Gejalanya adalah
`TS2307: Import "@std/assert" not a dependency` yang muncul secara lokal
maupun di CI.

**Gate TypeScript masuk ke `./scripts/verify.sh`.** Sebelumnya `verify.sh` tidak
menjalankan satu pun perintah Deno, sehingga CI memverifikasi kode yang tidak
pernah diverifikasi secara lokal. Local dan CI sekarang menjalankan gate yang
sama persis:

```sh
deno lint tui/src
deno fmt --check tui/src
deno check tui/src/main.ts
deno test --allow-all tui/src
```

## Alternatif yang Dipertimbangkan

**Node 24 dengan type stripping.** Node 24 sudah ada di workstation dan bisa
menjalankan TypeScript tanpa build. Ditolak karena Node tidak punya formatter
maupun linter bawaan, sehingga jalur itu tetap menuntut npm dan kehilangan
semua keuntungan no-build. Selain itu, keputusan runtime sudah dikunci di
ADR-0001, dan mengubahnya berarti melakukan supersede terhadap ADR tersebut.

**Tetap memakai prettier di samping `deno fmt`.** Ditolak karena dua formatter
untuk satu bahasa hampir pasti berbeda pada kasus tepi, dan setiap perbedaan
menjadi PR format yang gagal. Mandat sendiri menyatakan bahwa formatter
adalah sumber kebenaran; dua formatter melanggar itu.

**Menambah eslint tanpa prettier.** Menambah satu tool tanpa gunanya:
`deno lint` sudah menutup lint, dan menambah dependency lint kedua hanya
memperbesar permukaan dependensi.

## Konsekuensi

**Biaya yang diterima:**

- **Toolchain TUI terikat pada Deno.** Kontributor tidak bisa menjalankan gate
  TUI tanpa memasang Deno. Ini disadari dan diterima: prasyarat Deno 2.x
  didokumentasikan di panduan instalasi dan panduan setup pengembangan.
- **Tidak ada interoperabilitas dengan tooling npm.** anybody yang membuka
  `tui/` di editor berbasis node murni memerlukan konfigurasi tambahan. Deno
  Language Server menutup kekurangan itu tanpa menambah dependency.

**Manfaat yang didapat:**

- Nol dependency npm: `tui/` tidak punya `node_modules` dan tidak memerlukan
  `npm install` sama sekali.
- Satu toolchain, satu sumber kebenaran format, tidak ada kemungkinan drift.
- Versi dependency terkunci di `deno.lock` dengan hash integritas.
- Gate lokal dan CI identik, sehingga hasil hijau di lokal bukan lagi
  artifacts yang hanya berlaku secara lokal.
