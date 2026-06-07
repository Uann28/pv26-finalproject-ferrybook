from openpyxl import (
    Workbook
)

from openpyxl.styles import (
    Font
)

import os


class ExcelHelper:

    @staticmethod
    def export_manifest(
        data
    ):

        folder = "exports"

        if not os.path.exists(
            folder
        ):

            os.makedirs(
                folder
            )

        file_path = os.path.join(

            folder,

            "manifest_penumpang.xlsx"
        )

        wb = Workbook()

        ws = wb.active

        ws.title = "Manifest"

        headers = [

            "ID Tiket",

            "Nama",

            "Golongan",

            "Kapal",

            "Asal",

            "Tujuan"
        ]

        ws.append(
            headers
        )

        for cell in ws[1]:

            cell.font = Font(
                bold=True
            )

        for row in data:

            ws.append(
                row
            )

        wb.save(
            file_path
        )

        return file_path