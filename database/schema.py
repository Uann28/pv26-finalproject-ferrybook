import sqlite3
import os
import hashlib
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ferrybook.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'petugas')),
            created_at TEXT DEFAULT (datetime('now','localtime'))
        );

        CREATE TABLE IF NOT EXISTS kapal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_kapal TEXT NOT NULL,
            kode_kapal TEXT UNIQUE NOT NULL,
            kapasitas_penumpang INTEGER NOT NULL,
            kapasitas_kendaraan INTEGER NOT NULL,
            keterangan TEXT,
            is_active INTEGER DEFAULT 1,
            created_at TEXT DEFAULT (datetime('now','localtime'))
        );

        CREATE TABLE IF NOT EXISTS rute (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asal TEXT NOT NULL,
            tujuan TEXT NOT NULL,
            jarak_km REAL,
            durasi_menit INTEGER
        );

        CREATE TABLE IF NOT EXISTS jadwal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kapal_id INTEGER NOT NULL,
            rute_id INTEGER NOT NULL,
            tanggal TEXT NOT NULL,
            jam_berangkat TEXT NOT NULL,
            jam_tiba TEXT,
            harga_dewasa REAL NOT NULL,
            harga_kendaraan_motor REAL NOT NULL,
            harga_kendaraan_mobil REAL NOT NULL,
            harga_kendaraan_bus REAL NOT NULL,
            harga_kendaraan_truk REAL NOT NULL,
            kapasitas_penumpang INTEGER NOT NULL,
            kapasitas_kendaraan INTEGER NOT NULL,
            terisi_penumpang INTEGER DEFAULT 0,
            terisi_kendaraan INTEGER DEFAULT 0,
            status TEXT DEFAULT 'aktif' CHECK(status IN ('aktif','penuh','dibatalkan','selesai')),
            created_at TEXT DEFAULT (datetime('now','localtime')),
            FOREIGN KEY (kapal_id) REFERENCES kapal(id),
            FOREIGN KEY (rute_id) REFERENCES rute(id)
        );

        CREATE TABLE IF NOT EXISTS tiket (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nomor_tiket TEXT UNIQUE NOT NULL,
            jadwal_id INTEGER NOT NULL,
            petugas_id INTEGER NOT NULL,
            nama_penumpang TEXT NOT NULL,
            no_identitas TEXT NOT NULL,
            no_hp TEXT,
            tipe_tiket TEXT NOT NULL CHECK(tipe_tiket IN ('penumpang','kendaraan')),
            jenis_kendaraan TEXT,
            no_polisi TEXT,
            jumlah_penumpang INTEGER DEFAULT 1,
            harga_satuan REAL NOT NULL,
            total_harga REAL NOT NULL,
            status_pembayaran TEXT DEFAULT 'lunas',
            tanggal_transaksi TEXT DEFAULT (datetime('now','localtime')),
            FOREIGN KEY (jadwal_id) REFERENCES jadwal(id),
            FOREIGN KEY (petugas_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS jadwal_template (
            id                    INTEGER PRIMARY KEY AUTOINCREMENT,
            kapal_id              INTEGER NOT NULL,
            rute_id               INTEGER NOT NULL,
            jam_berangkat         TEXT NOT NULL,
            harga_dewasa          REAL NOT NULL DEFAULT 25000,
            harga_kendaraan_motor REAL NOT NULL DEFAULT 80000,
            harga_kendaraan_mobil REAL NOT NULL DEFAULT 250000,
            harga_kendaraan_bus   REAL NOT NULL DEFAULT 600000,
            harga_kendaraan_truk  REAL NOT NULL DEFAULT 900000,
            is_active             INTEGER DEFAULT 1,
            FOREIGN KEY (kapal_id) REFERENCES kapal(id),
            FOREIGN KEY (rute_id)  REFERENCES rute(id),
            UNIQUE (kapal_id, rute_id, jam_berangkat)
        );
    """)

    # Seed default admin
    cur.execute("SELECT id FROM users WHERE username='admin'")
    if not cur.fetchone():
        cur.execute(
            "INSERT INTO users (username, password, full_name, role) VALUES (?,?,?,?)",
            ("admin", hash_password("admin123"), "Super Administrator", "admin")
        )
        cur.execute(
            "INSERT INTO users (username, password, full_name, role) VALUES (?,?,?,?)",
            ("petugas1", hash_password("petugas123"), "Budi Santoso", "petugas")
        )

    # Seed rute
    cur.execute("SELECT id FROM rute WHERE asal='Kayangan'")
    if not cur.fetchone():
        rutes = [
            ("Kayangan", "Pototano", 15.0, 90),
            ("Pototano", "Kayangan", 15.0, 90),
            ("Lembar", "Padangbai", 40.0, 270),
            ("Padangbai", "Lembar", 40.0, 270),
            ("Ketapang", "Gilimanuk", 5.0, 45),
            ("Gilimanuk", "Ketapang", 5.0, 45),
        ]
        cur.executemany("INSERT INTO rute (asal, tujuan, jarak_km, durasi_menit) VALUES (?,?,?,?)", rutes)

    # Seed kapal
    cur.execute("SELECT id FROM kapal WHERE kode_kapal='KM-001'")
    if not cur.fetchone():
        kapals = [
            ("KM Nusa Tenggara I", "KM-001", 300, 50, "Kapal Feri Utama"),
            ("KM Nusa Tenggara II", "KM-002", 250, 40, "Kapal Feri Cadangan"),
            ("KM Bahari Express", "KM-003", 200, 30, "Kapal Cepat"),
        ]
        cur.executemany(
            "INSERT INTO kapal (nama_kapal, kode_kapal, kapasitas_penumpang, kapasitas_kendaraan, keterangan) VALUES (?,?,?,?,?)",
            kapals
        )

    conn.commit()
    conn.close()
