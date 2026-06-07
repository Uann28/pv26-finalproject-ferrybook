import os

from reportlab.pdfgen import (
    canvas
)

from reportlab.lib.pagesizes import (
    A6
)

from utils.qr_helper import (
    QRHelper
)


class PDFUtils:

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

        # ==================================
        # HEADER
        # ==================================

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
            9
        )

        c.drawCentredString(
            width / 2,
            height - 40,
            "Tiket Penyeberangan Ferry"
        )

        c.line(
            15,
            height - 48,
            width - 15,
            height - 48
        )

        # ==================================
        # ISI TIKET
        # ==================================

        c.setFont(
            "Helvetica",
            10
        )

        y = height - 68

        data = [

            f"ID Tiket  : {id_tiket}",

            f"Nama      : {nama}",

            f"Golongan  : {golongan}",

            f"Kapal     : {kapal}",

            f"Asal      : {asal}",

            f"Tujuan    : {tujuan}",

            f"Tanggal   : {tanggal}",

            f"Jam       : {jam}"
        ]

        for item in data:

            c.drawString(
                20,
                y,
                item
            )

            y -= 18

        c.line(
            15,
            y + 8,
            width - 15,
            y + 8
        )

        y -= 8

        # ==================================
        # TOTAL BAYAR
        # ==================================

        c.setFont(
            "Helvetica-Bold",
            11
        )

        c.drawString(
            20,
            y,
            f"Total     : Rp {int(total):,}"
        )

        # ==================================
        # QR CODE
        # ==================================

        c.drawImage(

            qr_path,

            width - 90,

            20,

            width=70,

            height=70
        )

        c.setFont(
            "Helvetica",
            7
        )

        c.drawCentredString(
            width - 55,
            15,
            "Scan untuk verifikasi"
        )

        c.save()

        return pdf_path

    @staticmethod
    def buka_tiket(
        pdf_path
    ):

        if not os.path.exists(
            pdf_path
        ):

            raise FileNotFoundError(
                f"File tidak ditemukan: {pdf_path}"
            )

        os.startfile(
            pdf_path
        )
