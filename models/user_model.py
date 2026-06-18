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
    @staticmethod
    def get_all():

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id_user,
                username,
                role
            FROM tb_users
            ORDER BY id_user
        """)

        data = cursor.fetchall()

        conn.close()

        return data

    @staticmethod
    def tambah(
        username,
        password,
        role
    ):

        conn = get_connection()

        cursor = conn.cursor()

        try:

            cursor.execute("""
                INSERT INTO tb_users(
                    username,
                    password,
                    role
                )
                VALUES(?,?,?)
            """, (
                username,
                UserModel.hash_password(password),
                role
            ))

            conn.commit()

            return True, "User berhasil ditambahkan"

        except Exception as e:

            return False, str(e)

        finally:

            conn.close()

    @staticmethod
    def update(
        id_user,
        role,
        password=None
    ):

        conn = get_connection()

        cursor = conn.cursor()

        try:

            if password:

                cursor.execute("""
                    UPDATE tb_users
                    SET role=?, password=?
                    WHERE id_user=?
                """, (
                    role,
                    UserModel.hash_password(password),
                    id_user
                ))

            else:

                cursor.execute("""
                    UPDATE tb_users
                    SET role=?
                    WHERE id_user=?
                """, (role, id_user))

            conn.commit()

            return True, "User berhasil diperbarui"

        except Exception as e:

            return False, str(e)

        finally:

            conn.close()

    @staticmethod
    def delete(id_user):

        conn = get_connection()

        cursor = conn.cursor()

        try:

            cursor.execute("""
                DELETE FROM tb_users
                WHERE id_user=?
            """, (id_user,))

            conn.commit()

            return True, "User berhasil dihapus"

        except Exception as e:

            return False, str(e)

        finally:

            conn.close()
