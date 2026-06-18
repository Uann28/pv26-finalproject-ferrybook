from models.user_model import (
    UserModel
)


class UserController:

    @staticmethod
    def get_all():

        return UserModel.get_all()

    @staticmethod
    def tambah(
        username,
        password,
        role
    ):

        if not username.strip():
            return False, "Username tidak boleh kosong"

        if not password.strip():
            return False, "Password tidak boleh kosong"

        return UserModel.tambah(
            username,
            password,
            role
        )

    @staticmethod
    def update(
        id_user,
        role,
        password=None
    ):

        return UserModel.update(
            id_user,
            role,
            password if password and password.strip() else None
        )

    @staticmethod
    def delete(id_user):

        return UserModel.delete(id_user)
