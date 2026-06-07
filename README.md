# ⛴ FerryBook
**Sistem Manajemen Jadwal dan Reservasi Tiket Kapal Feri Antar-Pulau Berbasis GUI PySide6**

---

## 📋 Final Project Pemrograman Visual

| Anggota | NIM |
|---|---|
| Juan Jordan Anugrah | F1D02310061 |
| Fairuza Luthfiana | F1D02310111 |
| Muhammad Fathan Abdullah | F1D02410124 |

---

## 🚀 Cara Menjalankan

### Prasyarat
- Python 3.10+ (disarankan 3.11/3.12)
- pip

### Instalasi

**Windows:**
```bash
# Jalankan installer otomatis
install.bat

# Atau manual:
pip install PySide6 reportlab
python main.py
```

**Linux / macOS:**
```bash
# Beri izin eksekusi
chmod +x install.sh
./install.sh

# Atau manual:
pip install PySide6 reportlab
python3 main.py
```

### Login Default

| Role | Username | Password |
|---|---|---|
| Super Admin | `admin` | `admin123` |
| Petugas Loket | `petugas1` | `petugas123` |

---

## 🗂️ Struktur Proyek

```
ferrybook/
├── main.py              ← Entry point
├── main_window.py       ← Jendela utama + navigasi sidebar
├── seed_demo.py         ← Data demo (auto-run pertama kali)
│
├── database/
│   └── schema.py        ← Inisialisasi & koneksi SQLite
│
├── models/
│   └── models.py        ← Seluruh logika akses data (CRUD)
│
├── views/
│   ├── login_view.py        ← Halaman login
│   ├── dashboard_view.py    ← Dashboard statistik real-time
│   ├── kapal_view.py        ← Kelola data kapal
│   ├── rute_view.py         ← Kelola rute penyeberangan
│   ├── jadwal_view.py       ← Kelola jadwal keberangkatan
│   ├── reservasi_view.py    ← POS reservasi tiket
│   ├── cari_tiket_view.py   ← Cari & cetak ulang tiket
│   ├── laporan_view.py      ← Laporan manifes + ekspor
│   ├── user_view.py         ← Manajemen pengguna (admin)
│   └── about_view.py        ← Info aplikasi
│
└── utils/
    ├── styles.py        ← Tema & stylesheet Qt
    └── pdf_utils.py     ← Generator PDF tiket & laporan
```

---

## ✨ Fitur Lengkap

### 👑 Super Admin
- **Dashboard** — Statistik real-time (jadwal hari ini, penumpang, pendapatan, tiket) + grafik batang 7 hari
- **Data Kapal** — CRUD kapal (nama, kode, kapasitas penumpang & kendaraan, status aktif)
- **Data Rute** — Tambah/hapus rute penyeberangan (asal, tujuan, jarak, durasi)
- **Jadwal Kapal** — Buat jadwal (pilih kapal+rute, tanggal, jam, tarif per kelas), ubah status, hapus
- **Reservasi Tiket** — POS ticketing (penumpang / kendaraan), kalkulasi otomatis, cetak PDF
- **Cari Tiket** — Temukan tiket by nomor, cetak ulang PDF
- **Laporan Manifes** — Filter periode+rute, ringkasan statistik, ekspor CSV & PDF
- **Manajemen User** — CRUD akun admin/petugas
- **Tentang** — Info aplikasi & tim

### 🖥️ Petugas Loket
- **Dashboard** — Ringkasan aktivitas hari ini
- **Reservasi Tiket** — POS penerbitan tiket
- **Cari Tiket** — Cari & cetak ulang
- **Laporan Manifes** — Lihat & ekspor laporan

---

## 🏗️ Arsitektur

Aplikasi menggunakan pola **Separation of Concerns (SoC)**:

```
[Views / UI Layer]  ←→  [Models / Data Layer]  ←→  [Database / SQLite]
   (PySide6)              (models.py)               (ferrybook.db)
```

- **Views**: Hanya menangani tampilan dan interaksi pengguna
- **Models**: Seluruh query dan logika bisnis terpusat di satu file
- **Database**: SQLite dengan foreign key constraint dan auto-seeding

---

## 📄 Ekspor Dokumen

- **Tiket PDF** — Format struk thermal 80mm, berisi info lengkap penumpang/kendaraan
- **Laporan PDF** — Format A4, tabel manifes dengan summary total tiket & pendapatan
- **Laporan CSV** — Format spreadsheet, kompatibel dengan Excel / Google Sheets

---

## 🗄️ Skema Database

```
users       → Akun pengguna (admin / petugas)
kapal       → Data armada kapal
rute        → Rute penyeberangan antar pelabuhan
jadwal      → Jadwal keberangkatan (kapal + rute + waktu + tarif + kapasitas)
tiket       → Tiket yang diterbitkan (terhubung ke jadwal + user)
```

Setiap penerbitan tiket **otomatis mengurangi kapasitas** jadwal terkait secara transaksional.
