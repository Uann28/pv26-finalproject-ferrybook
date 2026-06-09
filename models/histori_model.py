from database.db_manager import (
    get_connection
)


class HistoriModel:

    @staticmethod
    def tambah(
        tanggal,
        id_jadwal
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO
            tb_histori_reservasi(

                tanggal,

                id_jadwal,

                jumlah_booking

            )
            VALUES(
                ?,?,?
            )
        """, (

            tanggal,

            id_jadwal,

            1
        ))

        conn.commit()

        conn.close()

    @staticmethod
    def get_all():

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM tb_histori_reservasi
        """)

        data = cursor.fetchall()

        conn.close()

        return data