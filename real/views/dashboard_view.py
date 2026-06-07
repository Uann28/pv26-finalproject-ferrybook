from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QPushButton
)

from views.widgets.stat_card import (
    StatCard
)


class DashboardView(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout(self)

        title = QLabel(
            "🚢 Dashboard FerryBook"
        )

        title.setObjectName(
            "DashboardTitle"
        )

        layout.addWidget(title)

        # ====================
        # KPI
        # ====================

        cards = QHBoxLayout()

        self.card_tiket = StatCard(
            "🎟",
            "Reservasi"
        )

        self.card_pendapatan = StatCard(
            "💰",
            "Pendapatan"
        )

        self.card_jadwal = StatCard(
            "🚢",
            "Kapal Aktif"
        )

        self.card_histori = StatCard(
            "📈",
            "Histori"
        )

        cards.addWidget(
            self.card_tiket
        )

        cards.addWidget(
            self.card_pendapatan
        )

        cards.addWidget(
            self.card_jadwal
        )

        cards.addWidget(
            self.card_histori
        )

        layout.addLayout(cards)

        # ====================
        # EXPORT
        # ====================

        self.btn_export = QPushButton(
            "📑 Export Manifest"
        )

        layout.addWidget(
            self.btn_export
        )

        # ====================
        # MANIFEST
        # ====================

        lbl_manifest = QLabel(
            "Manifest Penumpang"
        )

        layout.addWidget(
            lbl_manifest
        )

        self.table_manifest = (
            QTableWidget()
        )

        self.table_manifest.setColumnCount(
            6
        )

        self.table_manifest.setHorizontalHeaderLabels([

            "ID Tiket",

            "Nama",

            "Golongan",

            "Kapal",

            "Asal",

            "Tujuan"
        ])

        self.table_manifest.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        layout.addWidget(
            self.table_manifest
        )

    def set_dashboard_data(
        self,
        tiket,
        pendapatan,
        jadwal,
        histori
    ):

        self.card_tiket.set_value(
            tiket
        )

        self.card_pendapatan.set_value(
            f"Rp {pendapatan:,.0f}"
        )

        self.card_jadwal.set_value(
            jadwal
        )

        self.card_histori.set_value(
            histori
        )

    def load_manifest(
        self,
        data
    ):

        self.table_manifest.setRowCount(
            0
        )

        for row_idx, row in enumerate(
            data
        ):

            self.table_manifest.insertRow(
                row_idx
            )

            for col_idx, value in enumerate(
                row
            ):

                self.table_manifest.setItem(

                    row_idx,

                    col_idx,

                    QTableWidgetItem(
                        str(value)
                    )
                )