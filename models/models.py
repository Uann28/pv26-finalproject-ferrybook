from database import get_connection, hash_password
from datetime import datetime
import random, string

# ─── USER MODEL ──────────────────────────────────────────────────────────────

def login(username: str, password: str):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, hash_password(password))
    ).fetchone()
    conn.close()
    return dict(row) if row else None

def get_all_users():
    conn = get_connection()
    rows = conn.execute("SELECT id,username,full_name,role,created_at FROM users ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def create_user(username, password, full_name, role):
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO users (username,password,full_name,role) VALUES (?,?,?,?)",
            (username, hash_password(password), full_name, role)
        )
        conn.commit()
        return True, "User berhasil dibuat"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def update_user(uid, full_name, role, password=None):
    conn = get_connection()
    try:
        if password:
            conn.execute("UPDATE users SET full_name=?,role=?,password=? WHERE id=?",
                         (full_name, role, hash_password(password), uid))
        else:
            conn.execute("UPDATE users SET full_name=?,role=? WHERE id=?",
                         (full_name, role, uid))
        conn.commit()
        return True, "User berhasil diperbarui"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def delete_user(uid):
    conn = get_connection()
    try:
        conn.execute("DELETE FROM users WHERE id=?", (uid,))
        conn.commit()
        return True, "User dihapus"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

# ─── KAPAL MODEL ─────────────────────────────────────────────────────────────

def get_all_kapal():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM kapal ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_kapal_aktif():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM kapal WHERE is_active=1 ORDER BY nama_kapal").fetchall()
    conn.close()
    return [dict(r) for r in rows]

_DEFAULT_JAM_SLOTS = ["06:00", "08:00", "10:00", "12:00", "14:00", "16:00", "18:00", "20:00"]

def create_kapal(nama, kode, kap_penumpang, kap_kendaraan, ket=""):
    conn = get_connection()
    try:
        cur = conn.execute(
            "INSERT INTO kapal (nama_kapal,kode_kapal,kapasitas_penumpang,kapasitas_kendaraan,keterangan) VALUES (?,?,?,?,?)",
            (nama, kode, kap_penumpang, kap_kendaraan, ket)
        )
        kapal_id = cur.lastrowid

        rute_rows = conn.execute("SELECT * FROM rute").fetchall()
        n_kapal   = conn.execute("SELECT COUNT(*) FROM kapal WHERE is_active=1").fetchone()[0]
        k_idx     = (kapal_id - 1) % len(_DEFAULT_JAM_SLOTS)
        slots     = _DEFAULT_JAM_SLOTS[k_idx::n_kapal] or [_DEFAULT_JAM_SLOTS[k_idx % len(_DEFAULT_JAM_SLOTS)]]
        for rute in rute_rows:
            jarak = rute['jarak_km'] or 0
            if jarak > 20:
                harga = (50000, 150000, 400000, 1000000, 1500000)
            else:
                harga = (25000, 80000, 250000, 600000, 900000)
            for jam in slots:
                conn.execute("""
                    INSERT OR IGNORE INTO jadwal_template
                        (kapal_id, rute_id, jam_berangkat,
                         harga_dewasa, harga_kendaraan_motor, harga_kendaraan_mobil,
                         harga_kendaraan_bus, harga_kendaraan_truk)
                    VALUES (?,?,?,?,?,?,?,?)
                """, (kapal_id, rute['id'], jam) + harga)

        conn.commit()
        return True, "Kapal berhasil ditambahkan"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def update_kapal(kid, nama, kode, kap_penumpang, kap_kendaraan, ket, is_active):
    conn = get_connection()
    try:
        conn.execute(
            "UPDATE kapal SET nama_kapal=?,kode_kapal=?,kapasitas_penumpang=?,kapasitas_kendaraan=?,keterangan=?,is_active=? WHERE id=?",
            (nama, kode, kap_penumpang, kap_kendaraan, ket, is_active, kid)
        )
        conn.commit()
        return True, "Kapal berhasil diperbarui"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def delete_kapal(kid):
    conn = get_connection()
    try:
        used = conn.execute("SELECT COUNT(*) FROM jadwal WHERE kapal_id=?", (kid,)).fetchone()[0]
        if used > 0:
            return False, f"Kapal tidak bisa dihapus, masih dipakai {used} jadwal"
        conn.execute("DELETE FROM kapal WHERE id=?", (kid,))
        conn.commit()
        return True, "Kapal dihapus"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

# ─── RUTE MODEL ──────────────────────────────────────────────────────────────

def get_all_rute():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM rute ORDER BY asal").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def create_rute(asal, tujuan, jarak, durasi):
    conn = get_connection()
    try:
        conn.execute("INSERT INTO rute (asal,tujuan,jarak_km,durasi_menit) VALUES (?,?,?,?)",
                     (asal, tujuan, jarak, durasi))
        conn.commit()
        return True, "Rute berhasil ditambahkan"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def update_rute(rid, asal, tujuan, jarak, durasi):
    conn = get_connection()
    try:
        conn.execute("UPDATE rute SET asal=?,tujuan=?,jarak_km=?,durasi_menit=? WHERE id=?",
                     (asal, tujuan, jarak, durasi, rid))
        conn.commit()
        return True, "Rute berhasil diperbarui"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def delete_rute(rid):
    conn = get_connection()
    try:
        used = conn.execute("SELECT COUNT(*) FROM jadwal WHERE rute_id=?", (rid,)).fetchone()[0]
        if used > 0:
            return False, f"Rute tidak bisa dihapus, masih dipakai {used} jadwal"
        conn.execute("DELETE FROM rute WHERE id=?", (rid,))
        conn.commit()
        return True, "Rute dihapus"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

# ─── JADWAL MODEL ────────────────────────────────────────────────────────────

def get_jadwal(tanggal=None, kapal_id=None, rute_id=None, status=None):
    conn = get_connection()
    query = """
        SELECT j.*, k.nama_kapal, k.kode_kapal, r.asal, r.tujuan,
               (j.kapasitas_penumpang - j.terisi_penumpang) AS sisa_penumpang,
               (j.kapasitas_kendaraan - j.terisi_kendaraan) AS sisa_kendaraan
        FROM jadwal j
        JOIN kapal k ON j.kapal_id = k.id
        JOIN rute r ON j.rute_id = r.id
        WHERE 1=1
    """
    params = []
    if tanggal:
        query += " AND j.tanggal=?"; params.append(tanggal)
    if kapal_id:
        query += " AND j.kapal_id=?"; params.append(kapal_id)
    if rute_id:
        query += " AND j.rute_id=?"; params.append(rute_id)
    if status:
        query += " AND j.status=?"; params.append(status)
    query += " ORDER BY j.tanggal, j.jam_berangkat"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_jadwal_by_id(jid):
    conn = get_connection()
    row = conn.execute("""
        SELECT j.*, k.nama_kapal, k.kode_kapal, r.asal, r.tujuan,
               (j.kapasitas_penumpang - j.terisi_penumpang) AS sisa_penumpang,
               (j.kapasitas_kendaraan - j.terisi_kendaraan) AS sisa_kendaraan
        FROM jadwal j
        JOIN kapal k ON j.kapal_id=k.id
        JOIN rute r ON j.rute_id=r.id
        WHERE j.id=?
    """, (jid,)).fetchone()
    conn.close()
    return dict(row) if row else None

def create_jadwal(kapal_id, rute_id, tanggal, jam_berangkat, jam_tiba,
                  harga_dewasa, harga_motor, harga_mobil, harga_bus, harga_truk,
                  kap_penumpang, kap_kendaraan):
    conn = get_connection()
    try:
        conn.execute("""
            INSERT INTO jadwal (kapal_id,rute_id,tanggal,jam_berangkat,jam_tiba,
                harga_dewasa,harga_kendaraan_motor,harga_kendaraan_mobil,
                harga_kendaraan_bus,harga_kendaraan_truk,
                kapasitas_penumpang,kapasitas_kendaraan)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """, (kapal_id, rute_id, tanggal, jam_berangkat, jam_tiba,
              harga_dewasa, harga_motor, harga_mobil, harga_bus, harga_truk,
              kap_penumpang, kap_kendaraan))
        conn.commit()
        return True, "Jadwal berhasil dibuat"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def update_jadwal_status(jid, status):
    conn = get_connection()
    try:
        conn.execute("UPDATE jadwal SET status=? WHERE id=?", (status, jid))
        conn.commit()
        return True, "Status jadwal diperbarui"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def update_jadwal(jid, kapal_id, rute_id, tanggal, jam_berangkat, jam_tiba,
                  harga_dewasa, harga_motor, harga_mobil, harga_bus, harga_truk,
                  kap_penumpang, kap_kendaraan):
    conn = get_connection()
    try:
        conn.execute("""
            UPDATE jadwal SET kapal_id=?,rute_id=?,tanggal=?,jam_berangkat=?,jam_tiba=?,
                harga_dewasa=?,harga_kendaraan_motor=?,harga_kendaraan_mobil=?,
                harga_kendaraan_bus=?,harga_kendaraan_truk=?,
                kapasitas_penumpang=?,kapasitas_kendaraan=?
            WHERE id=?
        """, (kapal_id, rute_id, tanggal, jam_berangkat, jam_tiba,
              harga_dewasa, harga_motor, harga_mobil, harga_bus, harga_truk,
              kap_penumpang, kap_kendaraan, jid))
        conn.commit()
        return True, "Jadwal berhasil diperbarui"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def delete_jadwal(jid):
    conn = get_connection()
    try:
        conn.execute("DELETE FROM jadwal WHERE id=?", (jid,))
        conn.commit()
        return True, "Jadwal dihapus"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

# ─── JADWAL TEMPLATE MODEL ───────────────────────────────────────────────────

def get_all_templates():
    conn = get_connection()
    rows = conn.execute("""
        SELECT jt.*, k.nama_kapal, k.kode_kapal, r.asal, r.tujuan
        FROM jadwal_template jt
        JOIN kapal k ON jt.kapal_id = k.id
        JOIN rute  r ON jt.rute_id  = r.id
        ORDER BY k.nama_kapal, r.asal, jt.jam_berangkat
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_templates_by_kapal(kapal_id):
    conn = get_connection()
    rows = conn.execute("""
        SELECT jt.*, r.asal, r.tujuan, r.jarak_km
        FROM jadwal_template jt
        JOIN rute r ON jt.rute_id = r.id
        WHERE jt.kapal_id = ?
        ORDER BY r.asal, jt.jam_berangkat
    """, (kapal_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def create_template(kapal_id, rute_id, jam_berangkat,
                    harga_dewasa=25000, harga_motor=80000, harga_mobil=250000,
                    harga_bus=600000, harga_truk=900000):
    conn = get_connection()
    try:
        conn.execute("""
            INSERT OR IGNORE INTO jadwal_template
                (kapal_id, rute_id, jam_berangkat,
                 harga_dewasa, harga_kendaraan_motor, harga_kendaraan_mobil,
                 harga_kendaraan_bus, harga_kendaraan_truk)
            VALUES (?,?,?,?,?,?,?,?)
        """, (kapal_id, rute_id, jam_berangkat,
              harga_dewasa, harga_motor, harga_mobil, harga_bus, harga_truk))
        conn.commit()
        return True, "Template jadwal berhasil dibuat"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def delete_template(tid):
    conn = get_connection()
    try:
        conn.execute("DELETE FROM jadwal_template WHERE id=?", (tid,))
        conn.commit()
        return True, "Template dihapus"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def set_template_active(tid, is_active: bool):
    conn = get_connection()
    try:
        conn.execute("UPDATE jadwal_template SET is_active=? WHERE id=?", (1 if is_active else 0, tid))
        conn.commit()
        return True, "Status template diperbarui"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

# ─── TIKET MODEL ─────────────────────────────────────────────────────────────

def generate_nomor_tiket():
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"FRY-{ts}-{rand}"

def create_tiket(jadwal_id, petugas_id, nama_penumpang, no_identitas, no_hp,
                 tipe_tiket, jenis_kendaraan, no_polisi, jumlah_penumpang,
                 harga_satuan, total_harga):
    conn = get_connection()
    try:
        nomor = generate_nomor_tiket()
        j = conn.execute("SELECT * FROM jadwal WHERE id=?", (jadwal_id,)).fetchone()
        if not j:
            return False, "Jadwal tidak ditemukan", None
        if j['status'] != 'aktif':
            return False, f"Jadwal berstatus '{j['status']}'", None
        if tipe_tiket == 'penumpang':
            sisa = j['kapasitas_penumpang'] - j['terisi_penumpang']
            if jumlah_penumpang > sisa:
                return False, f"Kapasitas penumpang tidak cukup. Sisa: {sisa}", None
            conn.execute("UPDATE jadwal SET terisi_penumpang=terisi_penumpang+? WHERE id=?",
                         (jumlah_penumpang, jadwal_id))
        else:
            sisa = j['kapasitas_kendaraan'] - j['terisi_kendaraan']
            if sisa < 1:
                return False, "Kapasitas kendaraan penuh", None
            conn.execute("UPDATE jadwal SET terisi_kendaraan=terisi_kendaraan+1 WHERE id=?",
                         (jadwal_id,))
        j_upd = conn.execute("SELECT * FROM jadwal WHERE id=?", (jadwal_id,)).fetchone()
        if j_upd['terisi_penumpang'] >= j_upd['kapasitas_penumpang'] and \
           j_upd['terisi_kendaraan'] >= j_upd['kapasitas_kendaraan']:
            conn.execute("UPDATE jadwal SET status='penuh' WHERE id=?", (jadwal_id,))

        conn.execute("""
            INSERT INTO tiket (nomor_tiket,jadwal_id,petugas_id,nama_penumpang,no_identitas,
                no_hp,tipe_tiket,jenis_kendaraan,no_polisi,jumlah_penumpang,
                harga_satuan,total_harga)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """, (nomor, jadwal_id, petugas_id, nama_penumpang, no_identitas,
              no_hp, tipe_tiket, jenis_kendaraan, no_polisi, jumlah_penumpang,
              harga_satuan, total_harga))
        conn.commit()
        return True, "Tiket berhasil diterbitkan", nomor
    except Exception as e:
        conn.rollback()
        return False, str(e), None
    finally:
        conn.close()

def get_tiket_by_nomor(nomor):
    conn = get_connection()
    row = conn.execute("""
        SELECT t.*, j.tanggal, j.jam_berangkat, j.jam_tiba,
               k.nama_kapal, k.kode_kapal, r.asal, r.tujuan,
               u.full_name AS nama_petugas
        FROM tiket t
        JOIN jadwal j ON t.jadwal_id=j.id
        JOIN kapal k ON j.kapal_id=k.id
        JOIN rute r ON j.rute_id=r.id
        JOIN users u ON t.petugas_id=u.id
        WHERE t.nomor_tiket=?
    """, (nomor,)).fetchone()
    conn.close()
    return dict(row) if row else None

def get_tiket_by_jadwal(jadwal_id):
    conn = get_connection()
    rows = conn.execute("""
        SELECT t.*, u.full_name AS nama_petugas
        FROM tiket t
        JOIN users u ON t.petugas_id=u.id
        WHERE t.jadwal_id=?
        ORDER BY t.tanggal_transaksi
    """, (jadwal_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_laporan_manifes(tanggal_awal, tanggal_akhir, rute_id=None):
    conn = get_connection()
    query = """
        SELECT t.*, j.tanggal, j.jam_berangkat, k.nama_kapal, r.asal, r.tujuan,
               u.full_name AS nama_petugas
        FROM tiket t
        JOIN jadwal j ON t.jadwal_id=j.id
        JOIN kapal k ON j.kapal_id=k.id
        JOIN rute r ON j.rute_id=r.id
        JOIN users u ON t.petugas_id=u.id
        WHERE j.tanggal BETWEEN ? AND ?
    """
    params = [tanggal_awal, tanggal_akhir]
    if rute_id:
        query += " AND j.rute_id=?"; params.append(rute_id)
    query += " ORDER BY j.tanggal, j.jam_berangkat, t.tanggal_transaksi"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_statistik_dashboard():
    conn = get_connection()
    today = datetime.now().strftime("%Y-%m-%d")
    stats = {}
    stats['total_jadwal_hari_ini'] = conn.execute(
        "SELECT COUNT(*) FROM jadwal WHERE tanggal=?", (today,)).fetchone()[0]
    stats['total_penumpang_hari_ini'] = conn.execute(
        "SELECT COALESCE(SUM(t.jumlah_penumpang),0) FROM tiket t JOIN jadwal j ON t.jadwal_id=j.id WHERE j.tanggal=? AND t.tipe_tiket='penumpang'",
        (today,)).fetchone()[0]
    stats['total_pendapatan_hari_ini'] = conn.execute(
        "SELECT COALESCE(SUM(t.total_harga),0) FROM tiket t JOIN jadwal j ON t.jadwal_id=j.id WHERE j.tanggal=?",
        (today,)).fetchone()[0]
    stats['total_tiket_hari_ini'] = conn.execute(
        "SELECT COUNT(*) FROM tiket t JOIN jadwal j ON t.jadwal_id=j.id WHERE j.tanggal=?",
        (today,)).fetchone()[0]
    stats['pendapatan_mingguan'] = []
    for i in range(6, -1, -1):
        row = conn.execute("""
            SELECT j.tanggal, COALESCE(SUM(t.total_harga),0) as total
            FROM jadwal j
            LEFT JOIN tiket t ON t.jadwal_id=j.id
            WHERE date(j.tanggal) = date('now', ? || ' days')
            GROUP BY j.tanggal
        """, (f"-{i}",)).fetchone()
        if row and row['tanggal']:
            stats['pendapatan_mingguan'].append({'tanggal': row['tanggal'], 'total': row['total']})
        else:
            from datetime import timedelta
            d = datetime.now().date()
            from datetime import timedelta
            td = d - timedelta(days=i)
            stats['pendapatan_mingguan'].append({'tanggal': str(td), 'total': 0})
    conn.close()
    return stats
