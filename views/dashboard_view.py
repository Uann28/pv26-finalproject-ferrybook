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

        self.chart.data = data

        self.chart.update()

class MiniChart(QWidget):

    def __init__(self):

        super().__init__()

        self.data = []

        self.setMinimumHeight(220)

    def paintEvent(self, event):

        if not self.data:
            return

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        w = self.width()
        h = self.height()

        max_val = max(
            item["total"]
            for item in self.data
        )

        if max_val == 0:
            return

        bar_width = w / len(self.data)

        for i, item in enumerate(self.data):

            nilai = item["total"]

            tanggal = item["tanggal"][5:]

            bar_h = (
                nilai / max_val
            ) * (h - 80)

            x = i * bar_width + 20

            y = h - bar_h - 40

            # batang grafik
            painter.setBrush(
                QColor("#00D4FF")
            )

            painter.setPen(
                Qt.NoPen
            )

            painter.drawRect(
                int(x),
                int(y),
                int(bar_width - 25),
                int(bar_h)
            )

            # nominal di atas batang
            painter.setPen(
                QColor("white")
            )

            painter.drawText(
                int(x),
                int(y - 10),
                f"Rp {int(nilai):,}".replace(",", ".")
            )

            # tanggal di bawah batang
            painter.drawText(
                int(x),
                h - 10,
                tanggal
            )