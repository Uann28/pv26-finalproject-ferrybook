from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QFrame,
    QComboBox,
    QDateEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView
)

from PySide6.QtCore import (
    QDate
)


class CariTiketView(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout(
            self
        )

        title = QLabel(
            "🔍 Cari Tiket"
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
        # FORM PENCARIAN
        # ==================================

        form_card = QFrame()

        form_card.setObjectName(
            "StatCard"
        )

        form_layout = QFormLayout(
            form_card
        )

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
            "🔍 Cari Tiket"
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
            self.btn_cari
        )

        # ==================================
        # LABEL HASIL
        # ==================================

        self.lbl_hasil = QLabel(
            "Menampilkan semua tiket"
        )

        form_layout.addRow(
            self.lbl_hasil
        )

        self.btn_reset = QPushButton(
            "🔄 Reset"
        )

        form_layout.addRow(
            self.btn_reset
        )

        content.addWidget(
            form_card,
            1
        )

        # ==================================
        # TABEL HASIL PENCARIAN
        # ==================================

        table_card = QFrame()

        table_card.setObjectName(
            "StatCard"
        )

        table_layout = QVBoxLayout(
            table_card
        )

        self.table_tiket = (
            QTableWidget()
        )

        self.table_tiket.setColumnCount(
            8
        )

        self.table_tiket.setHorizontalHeaderLabels([

            "ID Tiket",

            "Nama",

            "Golongan",

            "Kapal",

            "Asal",

            "Tujuan",

            "Tanggal",

            "Total Bayar"
        ])

        self.table_tiket.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.btn_cetak = QPushButton(
            "🖨 Cetak Tiket"
        )

        table_layout.addWidget(
            self.table_tiket
        )

        table_layout.addWidget(
            self.btn_cetak
        )

        content.addWidget(
            table_card,
            2
        )

    def load_data(
        self,
        data
    ):

        self.table_tiket.setRowCount(
            0
        )

        for row_idx, row in enumerate(
            data
        ):

            self.table_tiket.insertRow(
                row_idx
            )

            for col_idx, value in enumerate(
                row
            ):

                self.table_tiket.setItem(

                    row_idx,

                    col_idx,

                    QTableWidgetItem(
                        str(value)
                    )
                )

    def ambil_data_terpilih(self):

        row = (
            self.table_tiket.currentRow()
        )

        if row < 0:
            return None

        return {

            "id_tiket":
            int(
                self.table_tiket
                .item(row, 0)
                .text()
            ),

            "nama":
            self.table_tiket
            .item(row, 1)
            .text(),

            "golongan":
            self.table_tiket
            .item(row, 2)
            .text(),

            "kapal":
            self.table_tiket
            .item(row, 3)
            .text(),

            "asal":
            self.table_tiket
            .item(row, 4)
            .text(),

            "tujuan":
            self.table_tiket
            .item(row, 5)
            .text(),

            "tanggal":
            self.table_tiket
            .item(row, 6)
            .text(),

            "total":
            self.table_tiket
            .item(row, 7)
            .text()
        }
