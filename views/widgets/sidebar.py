from PySide6.QtWidgets import (
    QFrame,
    QPushButton,
    QLabel,
    QVBoxLayout
)


class Sidebar(QFrame):

    def __init__(self):

        super().__init__()

        self.setFixedWidth(
            260
        )

        self.setObjectName(
            "Sidebar"
        )

        layout = QVBoxLayout(
            self
        )

        self.logo = QLabel(
            "🚢 FERRYBOOK"
        )

        self.logo.setObjectName(
            "SidebarLogo"
        )

        layout.addWidget(
            self.logo
        )

        # =========================
        # MENU
        # =========================

        self.btn_dashboard = QPushButton(
            "📊 Dashboard"
        )

        self.btn_jadwal = QPushButton(
            "🚢 Jadwal"
        )

        self.btn_reservasi = QPushButton(
            "🎟 Reservasi"
        )

        self.btn_ai = QPushButton(
            "🤖 AI Pelabuhan"
        )

        self.btn_export = QPushButton(
            "📑 Export"
        )

        self.btn_theme = QPushButton(
            "🌙 Dark / Light"
        )

        self.btn_logout = QPushButton(
            "🚪 Logout"
        )

        layout.addWidget(
            self.btn_dashboard
        )

        layout.addWidget(
            self.btn_jadwal
        )

        layout.addWidget(
            self.btn_reservasi
        )

        layout.addWidget(
            self.btn_ai
        )

        layout.addWidget(
            self.btn_export
        )

        layout.addWidget(
            self.btn_theme
        )

        layout.addStretch()

        layout.addWidget(
            self.btn_logout
        )

    def set_role(
        self,
        role
    ):

        if role == "Super Admin":

            self.btn_dashboard.show()

            self.btn_jadwal.show()

            self.btn_ai.show()

            self.btn_export.show()

            self.btn_reservasi.hide()

        else:

            self.btn_dashboard.show()

            self.btn_reservasi.show()

            self.btn_theme.show()

            self.btn_logout.show()

            self.btn_jadwal.hide()

            self.btn_ai.hide()

            self.btn_export.hide()