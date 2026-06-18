from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame
)

from PySide6.QtCore import Qt


class AboutView(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            40, 40, 40, 40
        )

        layout.setSpacing(20)

        layout.setAlignment(Qt.AlignTop)

        title = QLabel("ℹ️ Tentang Aplikasi")
        title.setObjectName("DashboardTitle")
        layout.addWidget(title)

        # ==================================
        # INFO APLIKASI
        # ==================================

        card = QFrame()
        card.setObjectName("StatCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(14)

        logo = QLabel("🚢")
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet("font-size: 52px;")

        app_name = QLabel("FerryBook v2.0")
        app_name.setAlignment(Qt.AlignCenter)
        app_name.setObjectName("CardValue")

        app_desc = QLabel(
            "Sistem Manajemen Jadwal dan Reservasi Tiket Kapal Feri Antar-Pulau"
        )
        app_desc.setAlignment(Qt.AlignCenter)
        app_desc.setWordWrap(True)
        app_desc.setObjectName("CardTitle")

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)

        card_layout.addWidget(logo)
        card_layout.addWidget(app_name)
        card_layout.addWidget(app_desc)
        card_layout.addWidget(sep)

        info_rows = [
            ("Framework",   "PySide6 (Qt for Python)"),
            ("Database",    "SQLite (via Python sqlite3)"),
            ("Arsitektur",  "MVC (Model-View-Controller)"),
            ("PDF Export",  "ReportLab"),
            ("Excel Export","OpenPyXL"),
            ("QR Code",     "qrcode"),
            ("Mata Kuliah", "Pemrograman Visual"),
        ]

        for label, value in info_rows:
            row = QHBoxLayout()
            lbl = QLabel(label)
            lbl.setObjectName("CardTitle")
            lbl.setFixedWidth(130)
            val = QLabel(value)
            val.setObjectName("CardValue")
            row.addWidget(lbl)
            row.addWidget(val, 1)
            card_layout.addLayout(row)

        sep2 = QFrame()
        sep2.setFrameShape(QFrame.HLine)
        card_layout.addWidget(sep2)

        dev_title = QLabel("👥 Tim Pengembang")
        dev_title.setObjectName("CardTitle")
        card_layout.addWidget(dev_title)

        devs = [
            ("Juan Jordan Anugrah",       "F1D02310061"),
            ("Fairuza Luthfiana",         "F1D02310111"),
            ("Muhammad Fathan Abdullah",  "F1D02410124"),
        ]

        for name, nim in devs:
            dev_row = QHBoxLayout()
            icon = QLabel("👨‍💻")
            icon.setFixedWidth(28)
            name_lbl = QLabel(f"{name}  —  NIM: {nim}")
            name_lbl.setObjectName("CardTitle")
            dev_row.addWidget(icon)
            dev_row.addWidget(name_lbl, 1)
            card_layout.addLayout(dev_row)

        layout.addWidget(card)
        layout.addStretch()
