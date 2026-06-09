from models.tiket_model import (
    TiketModel
)

from utils.excel_helper import (
    ExcelHelper
)


class ExportController:

    @staticmethod
    def export_manifest():

        data = (
            TiketModel
            .manifest()
        )

        return (
            ExcelHelper
            .export_manifest(
                data
            )
        )