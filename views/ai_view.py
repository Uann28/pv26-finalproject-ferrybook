from PySide6.QtWidgets import (

    QWidget,

    QLabel,

    QVBoxLayout,

    QTableWidget,

    QTableWidgetItem,

    QHeaderView
)


class AIView(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout(
            self
        )

        title = QLabel(
            "🤖 AI Pelabuhan Pintar"
        )

        title.setObjectName(
            "DashboardTitle"
        )

        layout.addWidget(
            title
        )

        self.table_ai = (
            QTableWidget()
        )

        self.table_ai.setColumnCount(
            6
        )

        self.table_ai.setHorizontalHeaderLabels([

            "Kapal",

            "Terjual",

            "Kapasitas",

            "Occupancy",

            "Status",

            "Rekomendasi"
        ])

        self.table_ai.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        layout.addWidget(
            self.table_ai
        )

    def load_data(
        self,
        data
    ):

        self.table_ai.setRowCount(
            0
        )

        for row_idx, item in enumerate(
            data
        ):

            self.table_ai.insertRow(
                row_idx
            )

            values = [

                item["kapal"],

                item["terjual"],

                item["kapasitas"],

                f"{item['occupancy']}%",

                item["status"],

                item["rekomendasi"]
            ]

            for col_idx, value in enumerate(
                values
            ):

                self.table_ai.setItem(

                    row_idx,

                    col_idx,

                    QTableWidgetItem(
                        str(value)
                    )
                )