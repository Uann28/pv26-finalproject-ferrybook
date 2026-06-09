from reportlab.pdfgen import (
    canvas
)

from reportlab.lib.pagesizes import (
    A6
)

import os

from utils.qr_helper import (
    QRHelper
)


class ExportHelper:

    @staticmethod
    def cetak_tiket(

        id_tiket,

        nama,

        golongan,

        kapal,

        asal,

        tujuan,

        tanggal,

        jam,

        total
    ):

        folder = "exports"

        if not os.path.exists(
            folder
        ):

            os.makedirs(
                folder
            )

        pdf_path = os.path.join(

            folder,

            f"Tiket_{id_tiket}.pdf"
        )

        qr_path = (
            QRHelper.generate(
                id_tiket
            )
        )

        c = canvas.Canvas(
            pdf_path,
            pagesize=A6
        )

        width, height = A6

        c.setFont(
            "Helvetica-Bold",
            16
        )

        c.drawCentredString(
            width / 2,
            height - 25,
            "FERRYBOOK"
        )

        c.setFont(
            "Helvetica",
            10
        )

        y = height - 60

        data = [

            f"ID Tiket : {id_tiket}",

            f"Nama : {nama}",

            f"Golongan : {golongan}",

            f"Kapal : {kapal}",

            f"Asal : {asal}",

            f"Tujuan : {tujuan}",

            f"Tanggal : {tanggal}",

            f"Jam : {jam}",

            f"Total : Rp {total:,.0f}"
        ]

        for item in data:

            c.drawString(
                20,
                y,
                item
            )

            y -= 18

        c.drawImage(

            qr_path,

            width - 90,

            20,

            width=70,

            height=70
        )

        c.save()

        return pdf_path