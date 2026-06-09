from utils.ml_helper import (
    MLHelper
)


class AIController:

    @staticmethod
    def get_analisis():

        return (
            MLHelper
            .analisis_kepadatan()
        )