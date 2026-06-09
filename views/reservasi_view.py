from PySide6.QtWidgets import (

    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QFormLayout,
    QFrame,
    QComboBox,
    QLineEdit,
    QDateEdit
)

from PySide6.QtCore import (
    QDate
)


class ReservasiView(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout(
            self
        )

        title = QLabel(
            "🎟 Reservasi Ferry"
        )

        title.setObjectName(
            "DashboardTitle"
        )

        layout.addWidget(
            title
        )

        card = QFrame()

        card.setObjectName(
            "StatCard"
        )

        form = QFormLayout(
            card
        )

        # ==================
        # CARI JADWAL
        # ==================

        self.cb_asal = QComboBox()

        self.cb_asal.addItems([

            "Kayangan",

            "Lembar",

            "Padang Bai",

            "Pototano"
        ])

        self.cb_tujuan = QComboBox()

        self.cb_tujuan.addItems([

            "Kayangan",

            "Lembar",

            "Padang Bai",

            "Pototano"
        ])

        self.date_berangkat = (
            QDateEdit()
        )

        self.date_berangkat.setDate(
            QDate.currentDate()
        )

        self.date_berangkat.setCalendarPopup(
            True
        )

        self.cb_jam = QComboBox()

        for jam in range(24):

            self.cb_jam.addItem(
                f"{jam:02d}:00"
            )

        self.btn_cari = QPushButton(
            "🔍 Cari Kapal"
        )

        # ==================
        # KAPAL TERSEDIA
        # ==================

        self.cb_kapal = (
            QComboBox()
        )

        self.lbl_sisa = QLabel(
            "-"
        )

        # ==================
        # PENUMPANG
        # ==================

        self.txt_nama = (
            QLineEdit()
        )

        self.cb_golongan = (
            QComboBox()
        )

        self.cb_golongan.addItems([

            "Pejalan Kaki",

            "Golongan II - Motor",

            "Golongan IV - Mobil",

            "Golongan V - Bus",

            "Golongan VI - Truk"
        ])

        self.txt_nopol = (
            QLineEdit()
        )

        self.lbl_harga = QLabel(
            "Rp 0"
        )

        self.lbl_harga.setObjectName(
            "CardValue"
        )

        self.btn_proses = QPushButton(
            "🖨 Reservasi"
        )

        form.addRow(
            "Asal",
            self.cb_asal
        )

        form.addRow(
            "Tujuan",
            self.cb_tujuan
        )

        form.addRow(
            "Tanggal",
            self.date_berangkat
        )

        form.addRow(
            "Jam",
            self.cb_jam
        )

        form.addRow(
            self.btn_cari
        )

        form.addRow(
            "Kapal Tersedia",
            self.cb_kapal
        )

        form.addRow(
            "Sisa Kursi",
            self.lbl_sisa
        )

        form.addRow(
            "Nama",
            self.txt_nama
        )

        form.addRow(
            "Golongan",
            self.cb_golongan
        )

        form.addRow(
            "Nomor Polisi",
            self.txt_nopol
        )

        form.addRow(
            "Tarif",
            self.lbl_harga
        )

        form.addRow(
            self.btn_proses
        )

        layout.addWidget(
            card
        )