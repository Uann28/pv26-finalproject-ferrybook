from datetime import datetime

from database.db_manager import (
    get_connection
)


class TiketModel:

    @staticmethod
    def tambah(
        id_jadwal,
        nama,
        golongan,
        nopol,
        total_bayar
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO tb_tiket(

                id_jadwal,

                nama_penumpang,

                golongan,

                nopol,

                tanggal_booking,

                total_bayar

            )
            VALUES(
                ?,?,?,?,?,?
            )
        """, (

            id_jadwal,

            nama,

            golongan,

            nopol,

            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            total_bayar
        ))

        conn.commit()

        id_tiket = (
            cursor.lastrowid
        )

        conn.close()

        return id_tiket

    @staticmethod
    def total_tiket():

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM tb_tiket
        """)

        total = cursor.fetchone()[0]

        conn.close()

        return total

    @staticmethod
    def total_pendapatan():

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
            COALESCE(
                SUM(total_bayar),
                0
            )
            FROM tb_tiket
        """)

        total = cursor.fetchone()[0]

        conn.close()

        return total

    @staticmethod
    def manifest():

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT

                t.id_tiket,

                t.nama_penumpang,

                t.golongan,

                j.nama_kapal,

                j.pelabuhan_asal,

                j.pelabuhan_tujuan

            FROM tb_tiket t

            JOIN tb_jadwal j

            ON t.id_jadwal=j.id_jadwal

            ORDER BY t.id_tiket DESC
        """)

        data = cursor.fetchall()

        conn.close()

        return data

    @staticmethod
    def total_booking_jadwal(
        id_jadwal
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM tb_tiket
            WHERE id_jadwal=?
        """, (
            id_jadwal,
        ))

        total = cursor.fetchone()[0]

        conn.close()

        return total
    
    @staticmethod
    def pendapatan_7_hari():
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                DATE(tanggal_booking) as tanggal,
                COALESCE(SUM(total_bayar), 0) as total
            FROM tb_tiket
            WHERE DATE(tanggal_booking) >= DATE('now', '-6 day')
            GROUP BY DATE(tanggal_booking)
            ORDER BY tanggal ASC
        """)

        rows = cursor.fetchall()
        conn.close()

        return [
            {
                "tanggal": r[0],
                "total": r[1]
            }
            for r in rows
        ]
    
    @staticmethod
    def lihat_semua():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM tb_tiket
        """)

        data = cursor.fetchall()

        conn.close()

        return data
    
    @staticmethod
    def get_laporan(tgl_awal, tgl_akhir):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT

                t.id_tiket,

                t.nama_penumpang,

                t.golongan,

                t.nopol,

                j.nama_kapal,

                j.pelabuhan_asal,

                j.pelabuhan_tujuan,

                t.total_bayar

            FROM tb_tiket t

            JOIN tb_jadwal j
            ON t.id_jadwal = j.id_jadwal

            WHERE DATE(t.tanggal_booking)
            BETWEEN ? AND ?

            ORDER BY t.id_tiket DESC
        """, (
            tgl_awal,
            tgl_akhir
        ))

        data = cursor.fetchall()

        conn.close()

        return data