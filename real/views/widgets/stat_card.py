from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout
)

from PySide6.QtCore import Qt


class StatCard(QFrame):

    def __init__(
        self,
        icon,
        title
    ):

        super().__init__()

        self.setObjectName(
            "StatCard"
        )

        layout = QVBoxLayout(self)

        self.lbl_icon = QLabel(
            icon
        )

        self.lbl_icon.setAlignment(
            Qt.AlignCenter
        )

        self.lbl_icon.setObjectName(
            "CardIcon"
        )

        self.lbl_title = QLabel(
            title
        )

        self.lbl_title.setAlignment(
            Qt.AlignCenter
        )

        self.lbl_title.setObjectName(
            "CardTitle"
        )

        self.lbl_value = QLabel(
            "0"
        )

        self.lbl_value.setAlignment(
            Qt.AlignCenter
        )

        self.lbl_value.setObjectName(
            "CardValue"
        )

        layout.addWidget(
            self.lbl_icon
        )

        layout.addWidget(
            self.lbl_title
        )

        layout.addWidget(
            self.lbl_value
        )

    def set_value(
        self,
        value
    ):

        self.lbl_value.setText(
            str(value)
        )