<!--
ADR 0007 — Why the TypeScript parser validates strictly, and why allowlist lookup
uses Object.hasOwn.

File purpose: record the accepted decision that the TUI validates every JSONL
line against a field contract before casting it, that allowlist lookups consult
own keys only, and that parse.ts is split from protocol.ts.

An accepted ADR is immutable. Do not edit it to change its decision. Supersede
it with a new ADR that references this file number instead.
-->

# ADR 0007 — Validasi Ketat pada Parser Protokol

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-10-07 |
| Author | Apex Contributors |
| Review Date | 2027-01-07 |

## Konteks

ADR-0003 menetapkan fixture JSON sebagai satu sumber kebenaran untuk tiga
bahasa. Konsekuensi yang disengaja dari keputusan itu adalah ketiga bahasa
**harus** memberi hasil yang sama untuk input yang sama, karena TUI, CLI, dan
agent Python saling berbicara lewat JSONL stdio.

Pengukuran cakupan test baru saja menemukan bahwa jaminan itu
tidak benar. Implementasi TypeScript di `tui/src/protocol.ts` menerima payload
yang Rust dan Python tolak:

| Input `type` | Rust (serde) | Python (pydantic) | TypeScript (sebelum) |
|---|---|---|---|
| `Chat` | diterima | diterima | diterima |
| `Bogus` | ditolak | ditolak | ditolak |
| `constructor` | ditolak | ditolak | **diterima** |
| `toString` | ditolak | ditolak | **diterima** |
| `__proto__` | ditolak | ditolak | **diterima** |

Dua penyebab yang berbeda, keduanya nyata.

**1. Allowlist bocor lewat prototype chain.** Kode sebelumnya memeriksa tag
dengan operator `in`:

```typescript
if (!value.type || !(value.type in REQUEST_TYPES)) {
```

Operator `in` dan akses properti biasa sama-sama menelusuri
`Object.prototype`. Karena `REQUEST_TYPES` adalah object literal, setiap
anggota prototype — `constructor`, `toString`, `valueOf`, `hasOwnProperty`,
`__proto__` — terbaca sebagai tipe yang sah. `"Bogus"` ditolak hanya karena
nama itu tidak ada di prototype chain; penolakan itu hasilkan samping, bukan
desain. Secara efektif, allowlist ini berperilaku seperti blacklist terhadap
apa pun yang tidak dikenal.

**2. Tidak ada validasi field sama sekali.** Setelah tag lolos, kode
melakukan cast buta:

```typescript
return value as AgentRequest;
```

`{"type":"Chat"}` tanpa field `message` diterima, dan
`{"type":"Chat","message":123}` dengan `message` bertipe angka juga diterima.
Python dan Rust menolak keduanya. Di TUI, objek `ChatRequest` tanpa `message`
berarti `request.message` bernilai `undefined` di tempat yang mengharapkan
`string` — kegagalan yang muncul jauh dari penyebabnya.

Kerentanan ini berada di batas kepercayaan. Agen Python adalah satu-satunya
produsen baris JSONL, tetapi ia adalah **proses terpisah**; keluarannya adalah
input tak dipercaya bagi TUI. Mandat Zero Trust tidak menerima alasan
"produsennya sendiri".

## Keputusan

**Parser TypeScript memvalidasi, bukan hanya melakukan cast.** Setiap baris
JSONL melewati dua pemeriksaan: tag `type` terhadap allowlist, lalu setiap field
yang dideklarasikan terhadap tipe JSON-nya. Rust dan Python sudah melakukan ini
melalui enum tertutup dan model pydantic; TypeScript sekarang menyusul.

**Lookup allowlist memakai `Object.hasOwn`, tidak pernah `in`.** `Object.hasOwn`
memeriksa properti milik sendiri dan tidak menyentuh prototype chain, sehingga
anggota `Object.prototype` ditolak secara struktural, bukan karena sebuah guard
yang harus diingat:

```typescript
function lookupFields(
  table: Record<string, readonly Field[]>,
  tag: unknown,
): readonly Field[] | undefined {
  if (typeof tag !== "string") return undefined;
  return Object.hasOwn(table, tag) ? table[tag] : undefined;
}
```

**Kontrak field ditulis sebagai data, bukan sebagai rantai `if`.** Tabel
`REQUEST_FIELDS` dan `EVENT_FIELDS` menyebut field wajib beserta tipe JSON-nya.
Menambah tipe protocol berarti menambah satu baris tabel, bukan menambah
percabangan di dalam fungsi parse. `Done.usage` divalidasi satu level lebih
dalam lewat properti `nested`, sehingga `usage.prompt_tokens` yang hilang
ditolak sama seperti `prompt_tokens` yang bertipe salah.

**Satu tipe error, `ProtocolError`.** JSON rusak, baris bukan objek, tag tidak
dikenal, dan field tidak valid semuanya dilempar sebagai `ProtocolError`.
Pemanggil menangkap satu tipe, mencerminkan `Result` di Rust dan satu exception
di Python. Ini juga menghapus kebocoran `SyntaxError` dari `JSON.parse` yang
sebelumnya keluar dari API parser.

**Field tambahan yang tidak dikenal tetap diabaikan.** Pydantic dan serde
mengabaikannya, dan mengabaikannya menjaga paritas sekaligus membuat
penambahan field baru tidak merusak pembaca lama.

**`protocol.ts` dan `parse.ts` dipisah.** Satu berkas, satu tanggung jawab.
`protocol.ts` sekarang hanya deklarasi tipe dan tidak mengeksekusi apa pun;
`parse.ts` memegang validasi runtime.

## Alternatif yang Dipertimbangkan

**Pustaka skema seperti Zod atau Valibot.** Keduanya populer dan aktif
dirawat, tetapi keduanya menambah pohon dependensi ke `tui/` yang ADR-0006
justru sengaja bersihkan. Kontraknya hanya sekitar sepuluh tipe sederhana, dan
versi tanpa dependensi, sekitar 90 SLOC, masih jauh di bawah ambang 100 SLOC
yang membuat membangun sendiri lebih disukai. Pustaka skema baru diperlukan
ketika kontrak tumbuh jauh di luar yang bisa ditangani satu tabel.

**`Map` alih-alih `Record` untuk tabel allowlist.** `Map` juga menutup
prototype chain, dan sempat menjadi implementasi pertama. Ditolak karena
konvensi repo menyatakan tabel lookup statis berbentuk `Record`, dan karena
`Object.hasOwn` menyelesaikan masalah yang sama tanpa mengubah struktur data.
Keamanan di sini tidak bergantung pada pilihan struktur data, melainkan pada satu
fungsi lookup yang bisa dibaca dan diuji.

**Meninggalkan parser apa adanya dan mengandalkan fixture saja.** Fixture
memang menguji payload yang valid, dan justru itu kegunaannya. Fixture tidak
pernah memuat `{"type":"constructor"}` maupun field yang hilang, sehingga ketiga
parser bisa menyimpang tanpa test mana pun yang gagal. Drift yang baru
ditemukan justru karena fixture tidak cukup untuk menangkapnya.

**Menambal sisi Rust atau Python.** Parser Rust dan Python sudah benar.
Menambal sisi yang rusak adalah satu-satunya perbaikan yang menutup celah,
karena TUI adalah pihak yang memproses input dari luar.

## Konsekuensi

**Biaya yang diterima:**

- **Perilaku berubah.** Baris yang sebelumnya diterima sekarang ditolak. Bagi
  TUI ini justru memperbaiki kegagalan senyap: payload dengan tipe salah akan
  berhenti di batas dengan pesan yang menyebut field persisnya, bukan gagal
  secara membingungkan di lapisan render. Karena TUI belum terimplementasi
  (masih `phase 3`), tidak ada pengguna yang terdampak.
- **Kontrak field kini ada di tiga tempat** — Rust, Python, dan tabel
  TypeScript. Ini trade-off yang melekat pada ADR-0003 sendiri: fixture
  mengikat perilaku, tetapi tidak menggantikan implementasi.

**Manfaat yang didapat:**

- Bypass allowlist tertutup, dan sifatnya struktural: menghapus satu guard tidak
  akan membukanya kembali.
- Cakupan TypeScript naik dari 85,7% baris dan 50% cabang menjadi 99,0% dan
  97,4%, karena jalur penolakan kini diuji.
- Ketiga bahasa kembali menyepakati kontrak yang sama, dan `parse_test.ts`
  mengunci setiap perilaku itu — termasuk lima kunci prototype yang akan
  menggagalkan test bila suatu saat allowlist kembali bocor.
- Satu tipe error alih-alih beberapa, sehingga pemanggil tidak perlu
  `instanceof` berlapis.
