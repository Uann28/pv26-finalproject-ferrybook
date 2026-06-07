import hashlib

from database.db_manager import (
    get_connection
)


class UserModel:

    @staticmethod
    def hash_password(password):

        return hashlib.sha256(
            password.encode()
        ).hexdigest()

    @staticmethod
    def login(
        username,
        password
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id_user,
                username,
                role
            FROM tb_users
            WHERE username=?
            AND password=?
        """, (
            username,
            UserModel.hash_password(
                password
            )
        ))

        user = cursor.fetchone()

        conn.close()

        return user