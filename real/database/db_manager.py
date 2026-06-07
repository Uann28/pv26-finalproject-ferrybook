import sqlite3
import os
import hashlib

DB_NAME = "ferrybook.db"


def get_connection():

    root_dir = os.path.dirname(
        os.path.dirname(__file__)
    )

    db_path = os.path.join(
        root_dir,
        DB_NAME
    )

    conn = sqlite3.connect(
        db_path
    )

    conn.execute(
        "PRAGMA foreign_keys = ON"
    )

    return conn


def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()


def init_database():

    conn = get_connection()

    cursor = conn.cursor()

    # =====================================
    # USERS
    # =====================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tb_users(

            id_user INTEGER
            PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL,

            role TEXT NOT NULL
        )
    """)

    # =====================================
    # JADWAL
    # =====================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tb_jadwal(

            id_jadwal INTEGER
            PRIMARY KEY AUTOINCREMENT,

            nama_kapal TEXT NOT NULL,

            pelabuhan_asal TEXT NOT NULL,

            pelabuhan_tujuan TEXT NOT NULL,

            tanggal_berangkat TEXT NOT NULL,

            jam_berangkat TEXT NOT NULL,

            kapasitas_maks INTEGER NOT NULL,

            status TEXT DEFAULT 'Aktif'
        )
    """)

    # =====================================
    # TARIF
    # =====================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tb_tarif(

            id_tarif INTEGER
            PRIMARY KEY AUTOINCREMENT,

            golongan TEXT NOT NULL,

            harga REAL NOT NULL
        )
    """)

    # =====================================
    # TIKET
    # =====================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tb_tiket(

            id_tiket INTEGER
            PRIMARY KEY AUTOINCREMENT,

            id_jadwal INTEGER NOT NULL,

            nama_penumpang TEXT NOT NULL,

            golongan TEXT NOT NULL,

            nopol TEXT,

            tanggal_booking TEXT NOT NULL,

            total_bayar REAL NOT NULL,

            FOREIGN KEY(id_jadwal)
            REFERENCES tb_jadwal(id_jadwal)
            ON DELETE CASCADE
        )
    """)

    # =====================================
    # HISTORI RESERVASI
    # =====================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS
        tb_histori_reservasi(

            id_histori INTEGER
            PRIMARY KEY AUTOINCREMENT,

            tanggal TEXT NOT NULL,

            id_jadwal INTEGER NOT NULL,

            jumlah_booking INTEGER NOT NULL,

            FOREIGN KEY(id_jadwal)
            REFERENCES tb_jadwal(id_jadwal)
            ON DELETE CASCADE
        )
    """)

    # =====================================
    # USER DEFAULT
    # =====================================

    cursor.execute(
        "SELECT COUNT(*) FROM tb_users"
    )

    if cursor.fetchone()[0] == 0:

        users = [

            (
                "admin",
                hash_password(
                    "admin123"
                ),
                "Super Admin"
            ),

            (
                "loket1",
                hash_password(
                    "loket123"
                ),
                "Petugas Loket"
            )
        ]

        cursor.executemany("""
            INSERT INTO tb_users(
                username,
                password,
                role
            )
            VALUES(?,?,?)
        """, users)

    # =====================================
    # TARIF DEFAULT
    # =====================================

    cursor.execute(
        "SELECT COUNT(*) FROM tb_tarif"
    )

    if cursor.fetchone()[0] == 0:

        tarif_default = [

            (
                "Pejalan Kaki",
                20000
            ),

            (
                "Golongan II - Motor",
                50000
            ),

            (
                "Golongan IV - Mobil",
                150000
            ),

            (
                "Golongan V - Bus",
                250000
            ),

            (
                "Golongan VI - Truk",
                350000
            )
        ]

        cursor.executemany("""
            INSERT INTO tb_tarif(
                golongan,
                harga
            )
            VALUES(?,?)
        """, tarif_default)

    conn.commit()

    conn.close()


init_database()