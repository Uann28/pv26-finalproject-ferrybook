from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QFrame,
    QComboBox,
    QDateEdit
)

from PySide6.QtCore import QDate


class JadwalView(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout(self)

        title = QLabel(
            "🚢 Manajemen Jadwal Kapal"
        )

        title.setObjectName(
            "DashboardTitle"
        )

        layout.addWidget(
            title
        )

        content = QHBoxLayout()

        layout.addLayout(
            content
        )

        # ==================================
        # FORM
        # ==================================

        form_card = QFrame()

        form_card.setObjectName(
            "StatCard"
        )

        form_layout = QFormLayout(
            form_card
        )

        self.txt_nama_kapal = QLineEdit()

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

        self.txt_kapasitas = (
            QLineEdit()
        )

        self.txt_harga = (
            QLineEdit()
        )

        form_layout.addRow(
            "Nama Kapal",
            self.txt_nama_kapal
        )

        form_layout.addRow(
            "Asal",
            self.cb_asal
        )

        form_layout.addRow(
            "Tujuan",
            self.cb_tujuan
        )

        form_layout.addRow(
            "Tanggal",
            self.date_berangkat
        )

        form_layout.addRow(
            "Jam",
            self.cb_jam
        )

        form_layout.addRow(
            "Kapasitas",
            self.txt_kapasitas
        )

        self.btn_simpan = QPushButton(
            "💾 Simpan"
        )

        self.btn_edit = QPushButton(
            "✏ Edit"
        )

        self.btn_hapus = QPushButton(
            "🗑 Hapus"
        )

        form_layout.addRow(
            self.btn_simpan
        )

        form_layout.addRow(
            self.btn_edit
        )

        form_layout.addRow(
            self.btn_hapus
        )

        content.addWidget(
            form_card,
            1
        )

        # ==================================
        # TABLE
        # ==================================

        table_card = QFrame()

        table_card.setObjectName(
            "StatCard"
        )

        table_layout = QVBoxLayout(
            table_card
        )

        self.table_jadwal = (
            QTableWidget()
        )

        self.table_jadwal.setColumnCount(
            9
        )

        self.table_jadwal.setHorizontalHeaderLabels([
            "ID",
            "Kapal",
            "Asal",
            "Tujuan",
            "Tanggal",
            "Jam",
            "Kapasitas",
            "Harga",
            "Status"
        ])

        self.table_jadwal.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        table_layout.addWidget(
            self.table_jadwal
        )

        content.addWidget(
            table_card,
            2
        )

    def load_data(
        self,
        data
    ):

        self.table_jadwal.setRowCount(
            0
        )

        for row_idx, row in enumerate(data):

            self.table_jadwal.insertRow(
                row_idx
            )

            for col_idx, value in enumerate(row):

                self.table_jadwal.setItem(
                    row_idx,
                    col_idx,
                    QTableWidgetItem(
                        str(value)
                    )
                )

    def ambil_data_terpilih(self):
        row = self.table_jadwal.currentRow()

        if row < 0:
            return None

        return {

            "id":
            int(
                self.table_jadwal
                .item(row, 0)
                .text()
            ),

            "kapal":
            self.table_jadwal
            .item(row, 1)
            .text(),

            "asal":
            self.table_jadwal
            .item(row, 2)
            .text(),

            "tujuan":
            self.table_jadwal
            .item(row, 3)
            .text(),

            "tanggal":
            self.table_jadwal
            .item(row, 4)
            .text(),

            "jam":
            self.table_jadwal
            .item(row, 5)
            .text(),

            "kapasitas":
            self.table_jadwal
            .item(row, 6)
            .text(),

            "harga":
            self.table_jadwal
            .item(row, 7)
            .text()
        }