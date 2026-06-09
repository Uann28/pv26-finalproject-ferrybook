from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QFrame, QScrollArea, QSizePolicy, QGridLayout)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QColor, QPen, QFont
import models
from utils import format_rupiah
from datetime import datetime

class MiniBarChart(QWidget):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data  # list of {'tanggal': ..., 'total': ...}
        self.setMinimumHeight(120)

    def paintEvent(self, event):
        if not self.data:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        max_val = max(d['total'] for d in self.data) or 1
        n = len(self.data)
        bar_w = (w - 20) // n - 4
        pad = 10

        for i, item in enumerate(self.data):
            x = pad + i * ((w - 20) // n)
            bar_h = int((item['total'] / max_val) * (h - 30)) if item['total'] > 0 else 2
            y = h - 20 - bar_h
            # Bar
            grad_color = QColor("#00416A") if i < n - 1 else QColor("#00D4FF")
            painter.setBrush(grad_color)
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(x, y, bar_w, bar_h, 3, 3)
            # Date label
            date_short = item['tanggal'][5:] if item.get('tanggal') else ''
            painter.setPen(QColor("#4A7FA0"))
            f = QFont("Arial", 7)
            painter.setFont(f)
            painter.drawText(x, h - 4, date_short)


class StatCard(QFrame):
    def __init__(self, icon, label, value, accent="#00D4FF"):
        super().__init__()
        self.setObjectName("stat_card")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        icon_lbl = QLabel(icon)
        icon_lbl.setStyleSheet(f"font-size: 32px; background: transparent; color: {accent};")
        icon_lbl.setFixedWidth(44)
        text_layout = QVBoxLayout()
        self.value_lbl = QLabel(str(value))
        self.value_lbl.setObjectName("stat_card_value")
        self.value_lbl.setStyleSheet(f"color: {accent}; font-size: 26px; font-weight: bold; background: transparent;")
        self.label_lbl = QLabel(label)
        self.label_lbl.setObjectName("stat_card_label")
        self.label_lbl.setStyleSheet("background: transparent;")
        text_layout.addWidget(self.value_lbl)
        text_layout.addWidget(self.label_lbl)
        layout.addWidget(icon_lbl)
        layout.addLayout(text_layout)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def set_value(self, v):
        self.value_lbl.setText(str(v))


class DashboardView(QWidget):
    def __init__(self, user: dict):
        super().__init__()
        self.user = user
        self._build_ui()
        self._refresh()
        # Auto-refresh every 30s
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._refresh)
        self.timer.start(30000)

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        # Header
        hdr = QHBoxLayout()
        titles = QVBoxLayout()
        t = QLabel("Dashboard")
        t.setObjectName("page_title")
        s = QLabel(f"Selamat datang, {self.user['full_name']}")
        s.setObjectName("page_subtitle")
        titles.addWidget(t)
        titles.addWidget(s)
        hdr.addLayout(titles)
        hdr.addStretch()
        self.time_lbl = QLabel()
        self.time_lbl.setStyleSheet("color: #4A7FA0; font-size: 12px;")
        hdr.addWidget(self.time_lbl)
        layout.addLayout(hdr)

        # Stat cards
        grid = QGridLayout()
        grid.setSpacing(12)
        self.card_jadwal = StatCard("🚢", "Jadwal Hari Ini", "0", "#00D4FF")
        self.card_penumpang = StatCard("👥", "Penumpang Hari Ini", "0", "#00FF99")
        self.card_tiket = StatCard("🎫", "Tiket Diterbitkan", "0", "#FFD700")
        self.card_pendapatan = StatCard("💰", "Pendapatan Hari Ini", "Rp 0", "#FF6B6B")
        grid.addWidget(self.card_jadwal, 0, 0)
        grid.addWidget(self.card_penumpang, 0, 1)
        grid.addWidget(self.card_tiket, 0, 2)
        grid.addWidget(self.card_pendapatan, 0, 3)
        layout.addLayout(grid)

        # Chart section
        chart_frame = QFrame()
        chart_frame.setObjectName("stat_card")
        chart_layout = QVBoxLayout(chart_frame)
        chart_hdr = QLabel("Pendapatan 7 Hari Terakhir")
        chart_hdr.setObjectName("section_header")
        chart_layout.addWidget(chart_hdr)
        self.bar_chart = MiniBarChart([])
        self.bar_chart.setMinimumHeight(130)
        chart_layout.addWidget(self.bar_chart)
        layout.addWidget(chart_frame)

        # Recent schedules
        sched_frame = QFrame()
        sched_frame.setObjectName("stat_card")
        sched_layout = QVBoxLayout(sched_frame)
        sched_hdr = QLabel(f"Jadwal Hari Ini — {datetime.now().strftime('%d %B %Y')}")
        sched_hdr.setObjectName("section_header")
        sched_layout.addWidget(sched_hdr)
        self.jadwal_list = QWidget()
        self.jadwal_list_layout = QVBoxLayout(self.jadwal_list)
        self.jadwal_list_layout.setSpacing(6)
        sched_layout.addWidget(self.jadwal_list)
        layout.addWidget(sched_frame)
        layout.addStretch()

        # Update time every second
        self.tick_timer = QTimer(self)
        self.tick_timer.timeout.connect(self._update_time)
        self.tick_timer.start(1000)
        self._update_time()

    def _update_time(self):
        self.time_lbl.setText(datetime.now().strftime("%A, %d %B %Y  %H:%M:%S"))

    def _refresh(self):
        stats = models.get_statistik_dashboard()
        self.card_jadwal.set_value(stats['total_jadwal_hari_ini'])
        self.card_penumpang.set_value(stats['total_penumpang_hari_ini'])
        self.card_tiket.set_value(stats['total_tiket_hari_ini'])
        self.card_pendapatan.set_value(format_rupiah(stats['total_pendapatan_hari_ini']))
        self.bar_chart.data = stats['pendapatan_mingguan']
        self.bar_chart.update()

        # Jadwal list
        for i in reversed(range(self.jadwal_list_layout.count())):
            w = self.jadwal_list_layout.itemAt(i).widget()
            if w: w.deleteLater()
        today = datetime.now().strftime("%Y-%m-%d")
        jadwals = models.get_jadwal(tanggal=today)
        if not jadwals:
            lbl = QLabel("Tidak ada jadwal hari ini")
            lbl.setStyleSheet("color: #4A7FA0; padding: 8px; background: transparent;")
            self.jadwal_list_layout.addWidget(lbl)
        for j in jadwals[:6]:
            row = QFrame()
            row.setStyleSheet("background-color: #162535; border-radius: 6px; padding: 0;")
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(12, 8, 12, 8)
            time_lbl = QLabel(f"🕐 {j['jam_berangkat']}")
            time_lbl.setStyleSheet("color: #00D4FF; font-weight: bold; font-size: 13px; background: transparent;")
            route_lbl = QLabel(f"{j['asal']} → {j['tujuan']}")
            route_lbl.setStyleSheet("color: #E8EDF2; background: transparent;")
            kapal_lbl = QLabel(j['nama_kapal'])
            kapal_lbl.setStyleSheet("color: #7A9BB5; font-size: 11px; background: transparent;")
            sisa_lbl = QLabel(f"Sisa: {j['sisa_penumpang']} penumpang")
            sisa_lbl.setStyleSheet("color: #7A9BB5; font-size: 11px; background: transparent;")
            st_color = {"aktif":"#00FF99","penuh":"#FF6B6B","dibatalkan":"#4A7FA0","selesai":"#7A9BB5"}.get(j['status'],"#7A9BB5")
            st_lbl = QLabel(j['status'].upper())
            st_lbl.setStyleSheet(f"color: {st_color}; font-size: 11px; font-weight: bold; background: transparent;")
            row_layout.addWidget(time_lbl)
            row_layout.addWidget(route_lbl)
            row_layout.addWidget(kapal_lbl)
            row_layout.addStretch()
            row_layout.addWidget(sisa_lbl)
            row_layout.addWidget(st_lbl)
            self.jadwal_list_layout.addWidget(row)
