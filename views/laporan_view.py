from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QHeaderView,
    QAbstractItemView,
    QComboBox,
    QDateEdit,
    QFileDialog,
    QMessageBox
)

from PySide6.QtCore import Qt, QDate

from models.tiket_model import TiketModel
from models.jadwal_model import JadwalModel
from utils.laporan_pdf import cetak_laporan_pdf

import csv


class LaporanView(QWidget):

    def __init__(self):

        super().__init__()

        self._data = []

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout(self)

        title = QLabel("📋 Laporan Manifest Penumpang")
        title.setObjectName("DashboardTitle")
        layout.addWidget(title)

        # ==================================
        # FILTER
        # ==================================

        filter_card = QFrame()
        filter_card.setObjectName("StatCard")
        filter_layout = QHBoxLayout(filter_card)

        filter_layout.addWidget(QLabel("Dari:"))
        self.tgl_awal = QDateEdit()
        self.tgl_awal.setCalendarPopup(True)
        self.tgl_awal.setDate(QDate.currentDate().addDays(-7))
        self.tgl_awal.setFixedHeight(32)
        filter_layout.addWidget(self.tgl_awal)

        filter_layout.addWidget(QLabel("Sampai:"))
        self.tgl_akhir = QDateEdit()
        self.tgl_akhir.setCalendarPopup(True)
        self.tgl_akhir.setDate(QDate.currentDate())
        self.tgl_akhir.setFixedHeight(32)
        filter_layout.addWidget(self.tgl_akhir)

        self.btn_tampilkan = QPushButton("🔍 Tampilkan")
        self.btn_tampilkan.setFixedHeight(32)
        self.btn_tampilkan.clicked.connect(self._refresh)
        filter_layout.addWidget(self.btn_tampilkan)

        filter_layout.addStretch()
        layout.addWidget(filter_card)

        # ==================================
        # TABEL
        # ==================================

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID Tiket",
            "Nama",
            "Golongan",
            "No. Pol",
            "Kapal",
            "Asal",
            "Tujuan",
            "Total Bayar"
        ])
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )
        self.table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

        # ==================================
        # RINGKASAN + EXPORT
        # ==================================

        bottom = QHBoxLayout()

        self.lbl_total = QLabel("Total: 0 tiket  |  Pendapatan: Rp 0")
        self.lbl_total.setObjectName("CardValue")
        bottom.addWidget(self.lbl_total)

        bottom.addStretch()

        self.btn_csv = QPushButton("📄 Ekspor CSV")
        self.btn_csv.clicked.connect(self._export_csv)
        bottom.addWidget(self.btn_csv)

        self.btn_pdf = QPushButton("📑 Ekspor PDF")
        self.btn_pdf.clicked.connect(self._export_pdf)
        bottom.addWidget(self.btn_pdf)

        layout.addLayout(bottom)

    def _refresh(self):

        tgl_awal = self.tgl_awal.date().toString("yyyy-MM-dd")
        tgl_akhir = self.tgl_akhir.date().toString("yyyy-MM-dd")

        self._data = TiketModel.get_laporan(tgl_awal, tgl_akhir)

        self.table.setRowCount(len(self._data))

        total_bayar = 0

        for i, row in enumerate(self._data):

            vals = [
                str(row[0]),  # id_tiket
                row[1],       # nama_penumpang
                row[2],       # golongan
                row[3] or "-",# nopol
                row[4],       # nama_kapal
                row[5],       # asal
                row[6],       # tujuan
                f"Rp {int(row[7]):,}".replace(",", ".")  # total_bayar
            ]

            for c, v in enumerate(vals):
                item = QTableWidgetItem(v)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, c, item)

            self.table.setRowHeight(i, 34)
            total_bayar += row[7]

        self.lbl_total.setText(
            f"Total: {len(self._data)} tiket  |  "
            f"Pendapatan: Rp {int(total_bayar):,}".replace(",", ".")
        )

    def _export_csv(self):

        if not self._data:
            QMessageBox.warning(
                self, "Data Kosong",
                "Tidak ada data untuk diekspor."
            )
            return

        path, _ = QFileDialog.getSaveFileName(
            self, "Simpan CSV", "laporan_manifest.csv", "CSV (*.csv)"
        )

        if not path:
            return

        try:
            with open(path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "ID Tiket", "Nama", "Golongan", "No. Polisi",
                    "Kapal", "Asal", "Tujuan", "Total Bayar"
                ])
                for row in self._data:
                    writer.writerow(row[:8])
            QMessageBox.information(
                self, "Sukses", f"CSV disimpan ke:\n{path}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _export_pdf(self):

        if not self._data:
            QMessageBox.warning(
                self, "Data Kosong",
                "Tidak ada data untuk diekspor."
            )
            return

        path, _ = QFileDialog.getSaveFileName(
            self, "Simpan PDF", "laporan_manifest.pdf", "PDF (*.pdf)"
        )

        if not path:
            return

        tgl_a = self.tgl_awal.date().toString("dd/MM/yyyy")
        tgl_b = self.tgl_akhir.date().toString("dd/MM/yyyy")

        ok = cetak_laporan_pdf(
            self._data,
            f"Periode: {tgl_a} s/d {tgl_b}",
            path
        )

        if ok:
            QMessageBox.information(
                self, "Sukses", f"PDF disimpan ke:\n{path}"
            )
        else:
            QMessageBox.critical(
                self, "Error",
                "Gagal membuat PDF. Pastikan reportlab terinstal."
            )
