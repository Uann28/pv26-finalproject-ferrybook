from database.db_manager import (
    get_connection
)


class TarifModel:

    @staticmethod
    def get_all():

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM tb_tarif
        """)

        data = cursor.fetchall()

        conn.close()

        return data

    @staticmethod
    def get_harga(
        golongan
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT harga
            FROM tb_tarif
            WHERE golongan=?
        """, (
            golongan,
        ))

        result = cursor.fetchone()

        conn.close()

        if result:
            return result[0]

        return 0