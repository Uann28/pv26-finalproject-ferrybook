"""
Seed data demo untuk FerryBook.

- _seed_templates(): jalan SEKALI — isi jadwal_template (pola tetap kapal per rute & jam)
- _seed_historical_data(): jalan SEKALI — isi data historis 60 hari + tiket realistis
- ensure_jadwal_coverage(): jalan SETIAP app start — generate jadwal dari template
  untuk hari ini hingga N hari ke depan. Idempotent (aman dipanggil berkali-kali).
- seed_demo(): memanggil ketiganya
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import init_db, get_connection
from datetime import datetime, timedelta
import random
import string as _string

# Slot jam keberangkatan — 8 pilihan
JAM_SLOTS = ["06:00", "08:00", "10:00", "12:00", "14:00", "16:00", "18:00", "20:00"]

TARIF = {
    "default": dict(dewasa=25000, motor=80000,  mobil=250000, bus=600000,  truk=900000),
    "panjang": dict(dewasa=50000, motor=150000, mobil=400000, bus=1000000, truk=1500000),
}

NAMA_LIST = [
    "Budi Santoso", "Dewi Rahayu", "Ahmad Fauzi", "Siti Aminah",
    "Reza Pratama", "Nur Hidayah", "Agus Setiawan", "Rina Wulandari",
    "Hendra Gunawan", "Lestari Indah", "Wahyu Kusuma", "Sri Mulyani",
    "Eko Prasetyo", "Yuni Astuti", "Doni Kurniawan", "Maya Sari",
    "Fajar Nugroho", "Indah Permata", "Rizal Hakim", "Putri Andini",
]

_INSERT_JADWAL = """
    INSERT INTO jadwal
        (kapal_id, rute_id, tanggal, jam_berangkat, jam_tiba,
         harga_dewasa, harga_kendaraan_motor, harga_kendaraan_mobil,
         harga_kendaraan_bus, harga_kendaraan_truk,
         kapasitas_penumpang, kapasitas_kendaraan, status)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
"""


# ── Helpers ───────────────────────────────────────────────────────────────────

def _get_slots_for_kapal(k_idx: int, n_kapal: int) -> list:
    """
    Distribusi slot jam ke kapal secara round-robin.
    Jika kapal > 8: setiap kapal tetap dapat minimal 2 slot (bukan 1).
    """
    if n_kapal <= len(JAM_SLOTS):
        return JAM_SLOTS[k_idx % len(JAM_SLOTS)::n_kapal] or [JAM_SLOTS[k_idx % len(JAM_SLOTS)]]
    # Lebih dari 8 kapal → bagi JAM_SLOTS dua putaran
    extended = JAM_SLOTS + JAM_SLOTS          # 16 slot
    return extended[k_idx % len(JAM_SLOTS)::n_kapal] or [JAM_SLOTS[k_idx % len(JAM_SLOTS)]]


def _jam_tiba(jam_berangkat: str, durasi_menit: int) -> str:
    h, m = map(int, jam_berangkat.split(":"))
    total = h * 60 + m + max(durasi_menit, 60)
    return f"{(total // 60) % 24:02d}:{total % 60:02d}"


def _occupancy_factor(tgl_date, jam: str) -> float:
    dow  = tgl_date.weekday()
    hour = int(jam[:2])
    base = 0.35
    if dow >= 5:          base += 0.30
    elif dow == 4:        base += 0.15
    if 7 <= hour <= 9:    base += 0.20
    elif 15 <= hour <= 17: base += 0.15
    elif hour >= 20:      base -= 0.10
    base += random.uniform(-0.15, 0.15)
    return max(0.05, min(0.95, base))


def _gen_nomor(tgl_str: str) -> str:
    rand4 = ''.join(random.choices(_string.ascii_uppercase + _string.digits, k=4))
    rand6 = ''.join(random.choices(_string.digits, k=6))
    return f"FRY-{tgl_str.replace('-','')}{rand6}-{rand4}"


def _get_tarif(rute) -> dict:
    return TARIF["panjang"] if (rute['jarak_km'] or 0) > 20 else TARIF["default"]


# ── Fungsi 1: seed template (hanya sekali) ───────────────────────────────────

def _seed_templates():
    """
    Isi jadwal_template untuk semua kombinasi (kapal aktif, rute) dengan
    distribusi slot jam round-robin. Hanya jalan jika tabel masih kosong.
    """
    conn = get_connection()
    if conn.execute("SELECT COUNT(*) FROM jadwal_template").fetchone()[0] > 0:
        conn.close()
        return

    kapal_rows = conn.execute("SELECT * FROM kapal WHERE is_active=1").fetchall()
    rute_rows  = conn.execute("SELECT * FROM rute").fetchall()

    if not kapal_rows or not rute_rows:
        conn.close()
        return

    inserted = 0
    for k_idx, kapal in enumerate(kapal_rows):
        slots = _get_slots_for_kapal(k_idx, len(kapal_rows))
        for rute in rute_rows:
            tarif = _get_tarif(rute)
            for jam in slots:
                conn.execute("""
                    INSERT OR IGNORE INTO jadwal_template
                        (kapal_id, rute_id, jam_berangkat,
                         harga_dewasa, harga_kendaraan_motor, harga_kendaraan_mobil,
                         harga_kendaraan_bus, harga_kendaraan_truk)
                    VALUES (?,?,?,?,?,?,?,?)
                """, (kapal['id'], rute['id'], jam,
                      tarif['dewasa'], tarif['motor'], tarif['mobil'],
                      tarif['bus'], tarif['truk']))
                inserted += 1

    conn.commit()
    conn.close()
    print(f"[seed] Dibuat {inserted} template jadwal tetap.")


# ── Fungsi 2: seed historis (hanya sekali) ────────────────────────────────────

def _seed_historical_data():
    """
    Isi data jadwal 60 hari ke belakang + tiket historis realistis.
    Hanya jalan jika belum ada jadwal sama sekali.
    """
    conn = get_connection()
    existing = conn.execute("SELECT COUNT(*) FROM jadwal").fetchone()[0]
    if existing > 0:
        conn.close()
        return

    today     = datetime.now().date()
    kapal_rows = conn.execute("SELECT * FROM kapal WHERE is_active=1").fetchall()
    rute_rows  = conn.execute("SELECT * FROM rute").fetchall()

    if not kapal_rows or not rute_rows:
        conn.close()
        return

    petugas = conn.execute("SELECT id FROM users WHERE role='petugas'").fetchone() \
           or conn.execute("SELECT id FROM users LIMIT 1").fetchone()
    pid = petugas[0]

    jadwal_historis = []   # [(jid, kapal, rute, tgl_date, jam, tarif)]

    # Buat jadwal 60 hari lalu — status 'selesai'
    for delta in range(-60, 0):
        tgl     = today + timedelta(days=delta)
        tgl_str = tgl.strftime("%Y-%m-%d")
        for rute in rute_rows:
            tarif = _get_tarif(rute)
            durasi = rute['durasi_menit'] or 90
            for k_idx, kapal in enumerate(kapal_rows):
                for jam in _get_slots_for_kapal(k_idx, len(kapal_rows)):
                    cur = conn.execute(_INSERT_JADWAL, (
                        kapal['id'], rute['id'], tgl_str, jam, _jam_tiba(jam, durasi),
                        tarif['dewasa'], tarif['motor'], tarif['mobil'],
                        tarif['bus'], tarif['truk'],
                        kapal['kapasitas_penumpang'], kapal['kapasitas_kendaraan'],
                        'selesai'
                    ))
                    jadwal_historis.append((cur.lastrowid, kapal, rute, tgl, jam, tarif))

    conn.commit()
    print(f"[seed] Dibuat {len(jadwal_historis)} jadwal historis.")

    # Buat tiket historis realistis
    tiket_dibuat = 0
    for jid, kapal, rute, tgl, jam, tarif in jadwal_historis:
        factor  = _occupancy_factor(tgl, jam)
        target_p = int(kapal['kapasitas_penumpang'] * factor)
        target_k = int(kapal['kapasitas_kendaraan'] * factor)
        terisi_p = terisi_k = 0

        while terisi_p < target_p:
            jml   = min(random.randint(1, 4), target_p - terisi_p)
            nomor = _gen_nomor(tgl.strftime("%Y-%m-%d"))
            conn.execute("""
                INSERT OR IGNORE INTO tiket
                (nomor_tiket,jadwal_id,petugas_id,nama_penumpang,no_identitas,
                 tipe_tiket,jumlah_penumpang,harga_satuan,total_harga)
                VALUES (?,?,?,?,?,?,?,?,?)
            """, (nomor, jid, pid,
                  random.choice(NAMA_LIST),
                  f"35{random.randint(10,99)}{random.randint(100000,999999)}{random.randint(1000,9999)}",
                  'penumpang', jml, tarif['dewasa'], tarif['dewasa'] * jml))
            terisi_p  += jml
            tiket_dibuat += 1

        while terisi_k < target_k:
            jenis = random.choice(["Motor", "Motor", "Mobil", "Bus"])
            harga = tarif.get(jenis.lower(), tarif['motor'])
            prov  = random.choice(["B","D","L","EA","DR","N","DK","S"])
            nopol = f"{prov} {random.randint(1000,9999)} {random.choice(['AB','CD','EF','GH'])}"
            nomor = _gen_nomor(tgl.strftime("%Y-%m-%d"))
            conn.execute("""
                INSERT OR IGNORE INTO tiket
                (nomor_tiket,jadwal_id,petugas_id,nama_penumpang,no_identitas,
                 tipe_tiket,jenis_kendaraan,no_polisi,jumlah_penumpang,harga_satuan,total_harga)
                VALUES (?,?,?,?,?,?,?,?,?,?,?)
            """, (nomor, jid, pid,
                  random.choice(NAMA_LIST),
                  f"35{random.randint(10,99)}{random.randint(100000,999999)}{random.randint(1000,9999)}",
                  'kendaraan', jenis, nopol, 1, harga, harga))
            terisi_k += 1
            tiket_dibuat += 1

        conn.execute(
            "UPDATE jadwal SET terisi_penumpang=?, terisi_kendaraan=? WHERE id=?",
            (terisi_p, terisi_k, jid)
        )

    conn.commit()
    conn.close()
    print(f"[seed] Dibuat {tiket_dibuat} tiket historis.")


# ── Fungsi 3: ensure coverage (idempotent, setiap app start) ─────────────────

def ensure_jadwal_coverage(days_ahead: int = 30):
    """
    Generate jadwal aktif dari jadwal_template untuk hari ini s.d. days_ahead hari ke depan.
    Idempotent — skip kombinasi (kapal, rute, tanggal, jam) yang sudah ada.
    """
    conn = get_connection()
    today = datetime.now().date()

    templates = conn.execute("""
        SELECT jt.kapal_id, jt.rute_id, jt.jam_berangkat,
               jt.harga_dewasa, jt.harga_kendaraan_motor, jt.harga_kendaraan_mobil,
               jt.harga_kendaraan_bus, jt.harga_kendaraan_truk,
               k.kapasitas_penumpang, k.kapasitas_kendaraan,
               r.durasi_menit
        FROM jadwal_template jt
        JOIN kapal k ON jt.kapal_id = k.id
        JOIN rute  r ON jt.rute_id  = r.id
        WHERE jt.is_active = 1 AND k.is_active = 1
    """).fetchall()

    if not templates:
        conn.close()
        return

    added = 0
    for delta in range(0, days_ahead + 1):
        tgl_str = (today + timedelta(days=delta)).strftime("%Y-%m-%d")
        for t in templates:
            exists = conn.execute(
                "SELECT 1 FROM jadwal "
                "WHERE kapal_id=? AND rute_id=? AND tanggal=? AND jam_berangkat=?",
                (t['kapal_id'], t['rute_id'], tgl_str, t['jam_berangkat'])
            ).fetchone()
            if exists:
                continue
            durasi = t['durasi_menit'] or 90
            conn.execute(_INSERT_JADWAL, (
                t['kapal_id'], t['rute_id'], tgl_str,
                t['jam_berangkat'], _jam_tiba(t['jam_berangkat'], durasi),
                t['harga_dewasa'], t['harga_kendaraan_motor'], t['harga_kendaraan_mobil'],
                t['harga_kendaraan_bus'], t['harga_kendaraan_truk'],
                t['kapasitas_penumpang'], t['kapasitas_kendaraan'],
                'aktif'
            ))
            added += 1

    conn.commit()
    conn.close()
    if added:
        print(f"[ensure] +{added} jadwal baru dari template ({days_ahead} hari ke depan).")


# ── Entry point ───────────────────────────────────────────────────────────────

def seed_demo():
    init_db()
    _seed_templates()          # sekali saja — bangun template tetap per kapal
    _seed_historical_data()    # sekali saja — 60 hari historis + tiket
    ensure_jadwal_coverage()   # selalu — generate jadwal dari template untuk hari baru


if __name__ == "__main__":
    seed_demo()
