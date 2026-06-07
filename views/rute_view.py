from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QDialog, QFormLayout, QLineEdit,
                               QDoubleSpinBox, QSpinBox, QMessageBox,
                               QHeaderView, QAbstractItemView)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
import models


def _action_cell(edit_cb, del_cb) -> QWidget:
    w = QWidget()
    w.setObjectName("action_cell")
    lay = QHBoxLayout(w)
    lay.setContentsMargins(2, 2, 2, 2)
    lay.setSpacing(6)

    edit_btn = QPushButton("Edit")
    edit_btn.setObjectName("btn_warning")
    edit_btn.setFixedHeight(32)
    edit_btn.setCursor(Qt.PointingHandCursor)
    edit_btn.clicked.connect(edit_cb)

    del_btn = QPushButton("Hapus")
    del_btn.setObjectName("btn_danger")
    del_btn.setFixedHeight(32)
    del_btn.setCursor(Qt.PointingHandCursor)
    del_btn.clicked.connect(del_cb)

    lay.addWidget(edit_btn)
    lay.addWidget(del_btn)
    return w


class RuteDialog(QDialog):
    def __init__(self, parent=None, rute=None):
        super().__init__(parent)
        self.rute = rute
        self.setWindowTitle("Edit Rute" if rute else "Tambah Rute")
        self.setMinimumWidth(380)
        self._build_ui()
        if rute:
            self._populate(rute)

    def _build_ui(self):
        layout = QVBoxLayout(self); layout.setContentsMargins(20, 20, 20, 20); layout.setSpacing(12)
        title = QLabel("Data Rute Penyeberangan"); title.setObjectName("section_header")
        layout.addWidget(title)
        form = QFormLayout(); form.setSpacing(10)
        self.asal_input = QLineEdit(); self.asal_input.setFixedHeight(36)
        self.tujuan_input = QLineEdit(); self.tujuan_input.setFixedHeight(36)
        self.jarak_input = QDoubleSpinBox(); self.jarak_input.setRange(0, 9999); self.jarak_input.setSuffix(" km"); self.jarak_input.setFixedHeight(36)
        self.durasi_input = QSpinBox(); self.durasi_input.setRange(0, 9999); self.durasi_input.setSuffix(" mnt"); self.durasi_input.setFixedHeight(36)
        form.addRow("Asal *", self.asal_input)
        form.addRow("Tujuan *", self.tujuan_input)
        form.addRow("Jarak", self.jarak_input)
        form.addRow("Durasi", self.durasi_input)
        layout.addLayout(form)
        btns = QHBoxLayout(); btns.addStretch()
        cancel_btn = QPushButton("Batal"); cancel_btn.clicked.connect(self.reject)
        save_btn = QPushButton("Simpan"); save_btn.setObjectName("btn_primary"); save_btn.clicked.connect(self._save)
        btns.addWidget(cancel_btn); btns.addWidget(save_btn)
        layout.addLayout(btns)

    def _populate(self, r):
        self.asal_input.setText(r['asal'])
        self.tujuan_input.setText(r['tujuan'])
        self.jarak_input.setValue(r.get('jarak_km') or 0)
        self.durasi_input.setValue(r.get('durasi_menit') or 0)

    def _save(self):
        asal = self.asal_input.text().strip()
        tujuan = self.tujuan_input.text().strip()
        if not asal or not tujuan:
            QMessageBox.warning(self, "Validasi", "Asal dan tujuan wajib diisi.")
            return
        if asal.lower() == tujuan.lower():
            QMessageBox.warning(self, "Validasi", "Asal dan tujuan tidak boleh sama.")
            return
        if self.rute:
            ok, msg = models.update_rute(self.rute['id'], asal, tujuan,
                                         self.jarak_input.value(), self.durasi_input.value())
        else:
            ok, msg = models.create_rute(asal, tujuan, self.jarak_input.value(), self.durasi_input.value())
        if ok:
            self.accept()
        else:
            QMessageBox.critical(self, "Error", msg)


class KelolaRuteView(QWidget):
    COLS = ["Asal", "Tujuan", "Jarak", "Durasi", "Aksi"]

    def __init__(self, user: dict):
        super().__init__()
        self.user = user
        self._build_ui()
        self._refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self); layout.setContentsMargins(24, 24, 24, 24); layout.setSpacing(16)
        hdr = QHBoxLayout()
        titles = QVBoxLayout(); titles.setSpacing(2)
        t = QLabel("Data Rute"); t.setObjectName("page_title")
        s = QLabel("Manajemen rute penyeberangan antar pelabuhan"); s.setObjectName("page_subtitle")
        titles.addWidget(t); titles.addWidget(s); hdr.addLayout(titles); hdr.addStretch()
        add_btn = QPushButton("Tambah Rute"); add_btn.setObjectName("btn_primary")
        add_btn.setFixedHeight(36); add_btn.clicked.connect(self._add); hdr.addWidget(add_btn)
        layout.addLayout(hdr)

        self.table = QTableWidget()
        self.table.setColumnCount(len(self.COLS))
        self.table.setHorizontalHeaderLabels(self.COLS)
        hh = self.table.horizontalHeader()
        hh.setSectionResizeMode(0, QHeaderView.Stretch)
        hh.setSectionResizeMode(1, QHeaderView.Stretch)
        hh.setSectionResizeMode(2, QHeaderView.Fixed);   self.table.setColumnWidth(2, 110)
        hh.setSectionResizeMode(3, QHeaderView.Fixed);   self.table.setColumnWidth(3, 110)
        hh.setSectionResizeMode(4, QHeaderView.Fixed);   self.table.setColumnWidth(4, 180)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)

    def _refresh(self):
        rows = models.get_all_rute()
        self.table.clearSpans()

        if not rows:
            self.table.setRowCount(1)
            empty = QTableWidgetItem("Belum ada rute. Klik \"Tambah Rute\" untuk menambahkan.")
            empty.setTextAlignment(Qt.AlignCenter)
            empty.setForeground(QColor("#888888"))
            self.table.setSpan(0, 0, 1, len(self.COLS))
            self.table.setItem(0, 0, empty)
            self.table.setRowHeight(0, 60)
            return

        self.table.setRowCount(len(rows))
        for i, r in enumerate(rows):
            jarak = r.get('jarak_km') or 0
            durasi = r.get('durasi_menit') or 0
            vals = [r['asal'], r['tujuan'], f"{jarak:g} km", f"{durasi} mnt"]
            for c, v in enumerate(vals):
                item = QTableWidgetItem(v)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, c, item)

            self.table.setCellWidget(i, 4, _action_cell(
                lambda _, row=r: self._edit(row),
                lambda _, rid=r['id']: self._delete(rid),
            ))
            self.table.setRowHeight(i, 54)

    def _add(self):
        dlg = RuteDialog(self)
        if dlg.exec(): self._refresh()

    def _edit(self, rute):
        dlg = RuteDialog(self, rute)
        if dlg.exec(): self._refresh()

    def _delete(self, rid):
        reply = QMessageBox.question(self, "Konfirmasi", "Hapus rute ini?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            ok, msg = models.delete_rute(rid)
            if ok:
                self._refresh()
            else:
                QMessageBox.critical(self, "Error", msg)
