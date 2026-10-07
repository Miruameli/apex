<!--
ADR 0004 — Why Rust reaches Python through a PyO3 cdylib named apex_py.

File purpose: record the accepted decision to expose apex-core to Python via a
PyO3 extension module wrapped by apex/bridge.py, together with the pinned
versions, the loud-failure rule, and the interpreter-resolution pitfall that
breaks the build when the wrong Python is found on PATH.

An accepted ADR is immutable. Do not edit it to change its decision. Supersede
it with a new ADR that references this file number instead.
-->

# ADR 0004 — Bridge PyO3 Bound

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-10-07 |
| Author | Apex Contributors |
| Review Date | 2027-01-07 |

## Konteks

Otak Apex ada di Python, speed core ada di Rust. Keduanya harus bisa saling
memanggil: Python butuh pemindaian konteks dan tipe protokol dari Rust, dan CLI
Rust butuh logika inti yang sama tanpa menduplikasi.

Cara paling sederhana untuk dua bahasa memanggil satu sama lain adalah FFI
melalui ekstensi Python. Yang perlu diputuskan adalah bentuk ekstensi itu, apa
yang terjadi ketika build-nya gagal, dan bagaimana proses build memastikan
interpreter yang dipakai benar.

## Keputusan

**Rust diekspos ke Python sebagai extension module PyO3 bernama `apex_py`,
berupa cdylib.** Manifest `crates/apex-py/Cargo.toml` menetapkan
`crate-type = ["cdylib"]` dan `pyo3` versi `0.25` dengan fitur
`extension-module`; workspace mengunci resolver `3` dan edition `2024`.
Modul ini adalah facade tipis di atas `apex-core`: ia memanggil fungsi core,
bukan memegang logika sendiri.

**`apex/bridge.py` adalah facade Python yang gagal keras.** Modul itu melakukan
`importlib.import_module("apex_py")` dan, jika gagal, melempar `ApexBridgeError`
yang memuat perintah perbaikannya. Tidak ada jalur fallback Python murni.
Alasannya langsung: fallback senyap membuat build yang rusak terlihat sehat,
dan itu persis jenis drift yang dilarang aturan proyek.

**Sinkronisasi bridge memakai `scripts/sync_apex_py.py`, bukan maturin.**
Skrip itu membangun lokasi site-packages untuk interpreter yang sedang aktif
dengan membaca `EXT_SUFFIX` lewat `sysconfig`, lalu menyalin artefak dengan
`shutil.copy2`. Tag suffix dibaca dari interpreter yang berjalan, bukan ditebak,
karena tag yang dikarang tangan tidak akan import. Kegagalan dilaporkan keras:
skrip berhenti dengan perintah build yang tepat bila artefak belum ada.

**Versi di-pin.** Python `3.12` ditulis di `.python-version` dan
`requires-python` di `pyproject.toml`; PyO3 `0.25` di-pin di
`crates/apex-py/Cargo.toml` dan terkunci di `Cargo.lock`.

** Jebakan resolusi interpreter, dan cara menutupnya.** Build script PyO3
mencari Python dari `PATH`. Kalau `PATH` memuat interpreter lain, hasilnya
adalah cdylib yang tertaut ke interpreter yang salah, dan gejalanya muncul
saat import sebagai simbol `Py_TYPE` yang undefined. Karena itu build WAJIB
memakai `uv run cargo build`, yang mengunci interpreter lewat `VIRTUAL_ENV`:

```sh
uv run cargo build --workspace
uv run python scripts/sync_apex_py.py
uv run python -c 'import apex; print(apex.core_hello())'
```

`scripts/build.sh` dan `scripts/verify.sh` sudah menjalankan urutan itu.

## Alternatif yang Dipertimbangkan

**Subprocess ke binary Rust.** Python memanggil binary Rust sebagai proses
terpisah. Ditolak karena setiap pemanggilan scan konteks menjadi biaya spawn
proses dan serialisasi, sehingga bridge tidak bisa mengembalikan struktur data
dengan biaya rendah.

**ctypes atau cffi.** Butuh header dan FFI parser manual, tidak punya integrasi
dengan tipe Python. Ditolak karena PyO3 sudah memberi pemetaan tipe, konversi
`PyResult` yang benar, dan integrasi dengan argparse tanpa lapisan tambahan.

**Arah sebaliknya: Rust memanggil Python lewat pyo3.** Menempelkan interpreter
ke dalam binary Rust membuat Rust memanggil interpreter Python dari sisi dalam.
Ditolak karena membuat Rust bergantung pada lifecycle interpreter, sementara
yang dibutuhkan justru kebalikannya: Rust dibiarkan bebas dari orkestrasi LLM
seperti pada ADR-0001.

**Tidak melakukan apa-apa, duplikasi logika inti di kedua bahasa.** Ditolak
karena dua implementasi pasti berbeda pada kasus pojok, dan perbedaannya akan
tampil sebagai bug yang sulit direproduksi.

## Konsekuensi

**Biaya yang diterima:**

- **Build step tambahan.** Bridge bukan kode yang langsung jalan. Setiap
  perubahan Rust pada crate yang mengekspor perlu build lalu sinkronisasi
  sebelum Python melihatnya.
- **Dua versi yang harus dijaga.** PyO3 harus kompatibel dengan Python yang
  di-pin, jadi menaikkan Python berarti menaikkan PyO3.
- **Satu titik kegagalan saat load.** Bila artefak tidak ada atau salah tag,
  seluruh package Python gagal import. Ini disengaja, tetapi onboarding lokal
  tetap butuh langkah build.
- **Perbedaan platform.** Artefak harus dibangun per platform; sync memakai
  suffix yang dibaca dari interpreter aktif untuk menghadapi hal ini.

**Manfaat yang didapat:**

- Panggilan Rust dari Python punya biaya rendah dibanding spawn proses.
- Satu implementasi logika inti, di `apex-core`.
- Build yang rusak terdeteksi lebih awal, pada import, dengan pesan yang
  menyebutkan perbaikannya.