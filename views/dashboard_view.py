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

from PySide6.QtCore import QTimer, QDateTime, Qt
from PySide6.QtGui import QPainter, QColor
from models.tiket_model import TiketModel

from views.widgets.stat_card import StatCard



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

        self.time_label = QLabel()
        self.time_label.setObjectName("DashboardTime")
        layout.addWidget(self.time_label)

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

        self.chart = MiniChart()
        layout.addWidget(self.chart)

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

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        self.update_time()

        self.chart_timer = QTimer(self)
        self.chart_timer.timeout.connect(self.update_chart)
        self.chart_timer.start(10000)

        self.update_chart()

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

    def update_time(self):
        now = QDateTime.currentDateTime()
        self.time_label.setText(
            now.toString("dddd, dd MMMM yyyy - HH:mm:ss")
        )

    def update_chart(self):

        data = TiketModel.pendapatan_7_hari()

        self.chart.data = [
            row["total"]
            for row in data
        ]

        self.chart.update()
        print(TiketModel.pendapatan_7_hari())

class MiniChart(QWidget):

    def __init__(self, data=None):
        super().__init__()
        self.data = data or [20, 40, 60, 30, 80, 50, 90]
        self.setMinimumHeight(120)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()

        if not self.data:
            return

        max_val = max(self.data)
        bar_width = w / len(self.data)

        for i, val in enumerate(self.data):
            bar_h = (val / max_val) * (h - 20)

            x = i * bar_width + 10
            y = h - bar_h

            painter.setBrush(QColor("#00D4FF"))
            painter.setPen(Qt.NoPen)

            painter.drawRect(x, y, bar_width - 15, bar_h)