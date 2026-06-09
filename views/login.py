from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QLineEdit, QPushButton, QFrame, QMessageBox)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
import models

class LoginWindow(QWidget):
    login_success = Signal(dict)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("FerryBook — Login")
        self.setMinimumSize(420, 520)
        self._build_ui()

    def _build_ui(self):
        main = QVBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)

        # Background
        bg = QFrame()
        bg.setObjectName("login_bg")
        bg.setStyleSheet("background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 #0A1118, stop:1 #0F2030);")
        bg_layout = QVBoxLayout(bg)
        bg_layout.setAlignment(Qt.AlignCenter)
        main.addWidget(bg)

        # Card
        card = QFrame()
        card.setObjectName("login_card")
        card.setFixedWidth(340)
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(16)
        card_layout.setContentsMargins(32, 32, 32, 32)

        # Logo
        logo = QLabel("⛴")
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet("font-size: 48px; background: transparent;")

        title = QLabel("FerryBook")
        title.setObjectName("login_title")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Sistem Manajemen Kapal Feri")
        subtitle.setObjectName("login_subtitle")
        subtitle.setAlignment(Qt.AlignCenter)

        divider = QFrame()
        divider.setObjectName("divider")
        divider.setFrameShape(QFrame.HLine)

        # Form
        lbl_user = QLabel("Username")
        lbl_user.setObjectName("form_label")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Masukkan username...")
        self.username_input.setFixedHeight(40)

        lbl_pass = QLabel("Password")
        lbl_pass.setObjectName("form_label")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Masukkan password...")
        self.password_input.setFixedHeight(40)
        self.password_input.returnPressed.connect(self._do_login)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #FF6B6B; font-size: 12px; background: transparent;")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setWordWrap(True)

        login_btn = QPushButton("MASUK")
        login_btn.setObjectName("btn_primary")
        login_btn.setFixedHeight(44)
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.clicked.connect(self._do_login)

        hint = QLabel("Demo: admin/admin123 | petugas1/petugas123")
        hint.setStyleSheet("color: #3A5A70; font-size: 10px; background: transparent;")
        hint.setAlignment(Qt.AlignCenter)
        hint.setWordWrap(True)

        card_layout.addWidget(logo)
        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addWidget(divider)
        card_layout.addSpacing(8)
        card_layout.addWidget(lbl_user)
        card_layout.addWidget(self.username_input)
        card_layout.addWidget(lbl_pass)
        card_layout.addWidget(self.password_input)
        card_layout.addWidget(self.error_label)
        card_layout.addWidget(login_btn)
        card_layout.addWidget(hint)

        bg_layout.addWidget(card, alignment=Qt.AlignCenter)
        self.username_input.setFocus()

    def _do_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        if not username or not password:
            self.error_label.setText("Username dan password wajib diisi.")
            return
        user = models.login(username, password)
        if user:
            self.error_label.setText("")
            self.login_success.emit(user)
        else:
            self.error_label.setText("Username atau password salah.")
            self.password_input.clear()
            self.password_input.setFocus()
