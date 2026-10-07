<!--
ADR 0002 — Why the interface layers talk to the agent over JSONL on stdio.

File purpose: record the accepted decision to use JSON Lines over stdin/stdout
as the only wire protocol between the TUI and CLI on one side and the Python
agent on the other, plus the hard stdout/stderr rule that keeps the stream
parseable.

An accepted ADR is immutable. Do not edit it to change its decision. Supersede
it with a new ADR that references this file number instead.
-->

# ADR 0002 — JSONL over stdio untuk IPC

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-10-07 |
| Author | Apex Contributors |
| Review Date | 2027-01-07 |

## Konteks

Agent Apex berjalan sebagai proses terpisah dari antarmuka. Baik TUI
(TypeScript) maupun CLI (Rust) perlu mengirim request dan menerima aliran event
dari agent Python. Bentuk pertukarannya harus sederhana, dapat di-debug dengan
alat standar, dan tidak menambah dependensi jaringan.

Kebutuhan nyata dari lapisan ini:

- Streaming event satu per satu, bukan satu respons besar di akhir.
- Kemampuan menjalankan `apex chat` dalam pipeline, sehingga keluarannya harus
  bisa dibaca mesin.
- Tiga bahasa yang harus bicara lewat format yang sama.

## Keputusan

TUI dan CLI berkomunikasi dengan agent melalui JSON Lines di atas stdin/stdout.
Satu request atau satu event per baris, UTF-8, dengan line separator `\n`.
Topologi ini tercermin di `docs/engineering/subsystems/interface/40-system-ipc-contract.md`:

```
TUI (TS)   ──JSONL stdio──▶  Agent (Python)
CLI (Rust) ──JSONL stdio──▶  Agent (Python)
```

**Aturan keras:**

1. **`stdout` hanya berisi JSONL event, satu per baris.** Tidak ada banner,
   spanduk versi, atau teks untuk manusia. Aturan ini penting karena stdout
   adalah data yang dikonsumsi pipeline, bukan tampilan.
2. **Banner dan log ditulis ke `stderr`.** Aturan inilah yang membuat pemisahan
   itu mungkin: diagnostik tetap terlihat tanpa pernah merusak stream.
3. **Penerima mengurai per-baris di dalam `try/catch`.** Baris yang bukan JSON,
   atau JSON dengan `type` yang tidak dikenal, menghasilkan event `Error`,
   bukan crash pada stream. Satu baris rusak tidak boleh menjatuhkan sesi
   yang sedang berjalan.
4. **Encoding UTF-8, newline `\n`.** Tanpa ini, diff dan output multibyte bisa
   rusak saat dipindah antar platform.

Aturan ini sudah menjadi konvensi yang berjalan: parser Python
(`apex/protocol.py`) dan parser TypeScript (`tui/src/protocol.ts`) keduanya
validasi `type` dan menolak tipe yang tidak dikenal.

## Alternatif yang Dipertimbangkan

**gRPC dengan protobuf.** Lebih cepat untuk payload besar dan punya skema yang
didefinisikan oleh mesin. Ditolak karena membawa toolchain terpisah untuk
membuat kode, menolak seluruh string JSON yang sudah bisa dibaca manusia,
dan tidak memberi apa pun untuk terminal yang sudah berupa pipe. Overhead IPC
lokal bukan masalah; kegunaannya yang tidak sebanding dengan biayanya.

**Unix domain socket.** Pola umum untuk daemon lokal dan mendukung
multiplexing. Ditolak karena membawa socket discovery, manajemen file socket,
dan kasus port yang bentrok. Untuk topologi satu-agent-satu-klien yang
dijalankan sebagai subprocess, pipe stdio lebih sederhana tanpa kehilangan
apa pun yang dibutuhkan.

**WebSocket.** Butuh server berjalan dan atravessasi jaringan. Ditolak karena
menambah permukaan serangan tanpa manfaat nyata: tidak ada akses remote yang
dibutuhkan untuk produk terminal yang berjalan di mesin sendiri.

**Tidak melakukan apa-apa, memakai pipe teks biasa.** Ditolak karena teks
biasa tidak punya batas baris yang tegas untuk event streaming dan tidak punya
jenis payload, sehingga penerima tidak bisa membedakan `Thinking` dari `Done`.

## Konsekuensi

**Biaya yang diterima:**

- **Tidak ada skema yang ditegakkan compiler.** Bentuk payload ditentukan oleh
  fixture dan test, bukan oleh `.proto`. Kontrak harus dijaga ADR-0003.
- **Setiap baris harus valid.** Siapa pun yang menulis ke stdout, termasuk
  pustaka pihak ketiga yang tidak dikontrol Apex, harus disiplin. Aturan ini
  dijaga lewat code review dan test.
- **Tidak ada multiplexing.** Satu request pada satu waktu per pipe. Cukup untuk
  satu TUI dan satu CLI, dan menyederhanakan siklus hidup sesi.

**Manfaat yang didapat:**

- Nol dependensi jaringan dan nol port yang perlu dialokasikan.
- Dapat di-debug langsung: `apex chat` bisa disimulasikan dengan echo dan pipe,
  dan keluarannya bisa dibaca dengan `head` atau `jq`.
- Format yang sama berlaku untuk skill subprocess dan MCP server, sehingga
  hanya ada satu cara bicara dalam repo ini.