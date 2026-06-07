from datetime import datetime

from database.db_manager import (
    get_connection
)

from models.tiket_model import (
    TiketModel
)


class JadwalModel:

    @staticmethod
    def get_all():

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM tb_jadwal
            ORDER BY
            tanggal_berangkat,
            jam_berangkat
        """)

        data = cursor.fetchall()

        conn.close()

        return data

    @staticmethod
    def tambah(
        nama_kapal,
        asal,
        tujuan,
        tanggal,
        jam,
        kapasitas
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO tb_jadwal(

                nama_kapal,

                pelabuhan_asal,

                pelabuhan_tujuan,

                tanggal_berangkat,

                jam_berangkat,

                kapasitas_maks,

                status

            )
            VALUES(
                ?,?,?,?,?,?,?
            )
        """, (

            nama_kapal,

            asal,

            tujuan,

            tanggal,

            jam,

            kapasitas,

            "Aktif"
        ))

        conn.commit()

        conn.close()

    @staticmethod
    def update(
        id_jadwal,
        nama_kapal,
        asal,
        tujuan,
        tanggal,
        jam,
        kapasitas
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            UPDATE tb_jadwal
            SET

            nama_kapal=?,

            pelabuhan_asal=?,

            pelabuhan_tujuan=?,

            tanggal_berangkat=?,

            jam_berangkat=?,

            kapasitas_maks=?

            WHERE id_jadwal=?
        """, (

            nama_kapal,

            asal,

            tujuan,

            tanggal,

            jam,

            kapasitas,

            id_jadwal
        ))

        conn.commit()

        conn.close()

    @staticmethod
    def delete(
        id_jadwal
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM tb_jadwal
            WHERE id_jadwal=?
        """, (
            id_jadwal,
        ))

        conn.commit()

        conn.close()

    @staticmethod
    def get_by_id(
        id_jadwal
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM tb_jadwal
            WHERE id_jadwal=?
        """, (
            id_jadwal,
        ))

        data = cursor.fetchone()

        conn.close()

        return data

    @staticmethod
    def kapasitas_tersisa(
        id_jadwal
    ):

        jadwal = (
            JadwalModel
            .get_by_id(
                id_jadwal
            )
        )

        if not jadwal:
            return 0

        kapasitas = jadwal[6]

        booking = (
            TiketModel
            .total_booking_jadwal(
                id_jadwal
            )
        )

        return kapasitas - booking
    
    @staticmethod
    def cari_jadwal(
        asal,
        tujuan,
        tanggal,
        jam
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM tb_jadwal
            WHERE

            pelabuhan_asal=?

            AND pelabuhan_tujuan=?

            AND tanggal_berangkat=?

            AND jam_berangkat=?

            AND status='Aktif'
        """, (

            asal,

            tujuan,

            tanggal,

            jam
        ))

        data = cursor.fetchall()

        conn.close()

        return data