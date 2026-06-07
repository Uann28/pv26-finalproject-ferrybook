from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QFrame
)

from PySide6.QtCore import Qt


class LoginView(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout(self)

        layout.setAlignment(
            Qt.AlignCenter
        )

        self.card = QFrame()

        self.card.setObjectName(
            "LoginCard"
        )

        self.card.setFixedWidth(
            450
        )

        card_layout = QVBoxLayout(
            self.card
        )

        self.lbl_logo = QLabel(
            "🚢 FERRYBOOK"
        )

        self.lbl_logo.setObjectName(
            "LoginTitle"
        )

        self.lbl_logo.setAlignment(
            Qt.AlignCenter
        )

        self.txt_username = QLineEdit()

        self.txt_username.setPlaceholderText(
            "Username"
        )

        self.txt_password = QLineEdit()

        self.txt_password.setPlaceholderText(
            "Password"
        )

        self.txt_password.setEchoMode(
            QLineEdit.Password
        )

        self.btn_login = QPushButton(
            "Masuk"
        )

        card_layout.addWidget(
            self.lbl_logo
        )

        card_layout.addWidget(
            self.txt_username
        )

        card_layout.addWidget(
            self.txt_password
        )

        card_layout.addWidget(
            self.btn_login
        )

        layout.addWidget(
            self.card
        )