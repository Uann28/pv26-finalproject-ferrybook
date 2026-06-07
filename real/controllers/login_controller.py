from models.user_model import (
    UserModel
)


class LoginController:

    @staticmethod
    def authenticate(
        username,
        password
    ):

        if not username.strip():

            return None

        if not password.strip():

            return None

        return UserModel.login(
            username,
            password
        )