from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QFrame,
    QHeaderView,
    QAbstractItemView,
    QComboBox,
    QLineEdit,
    QDialog,
    QMessageBox
)

from PySide6.QtCore import Qt

from controllers.user_controller import UserController


class UserDialog(QDialog):
    """Dialog tambah / edit user."""

    def __init__(self, parent=None, user=None):

        super().__init__(parent)

        self.user = user  # tuple (id_user, username, role) atau None

        self.setWindowTitle(
            "Tambah User" if not user else "Edit User"
        )

        self.setMinimumWidth(360)

        self._build_ui()

        if user:
            self._populate(user)

    def _build_ui(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title = QLabel(
            "Data Pengguna"
        )
        title.setObjectName("DashboardTitle")
        layout.addWidget(title)

        form = QFormLayout()
        form.setSpacing(10)

        self.txt_username = QLineEdit()
        self.txt_username.setFixedHeight(36)
        self.txt_username.setPlaceholderText("Username...")

        self.txt_password = QLineEdit()
        self.txt_password.setEchoMode(QLineEdit.Password)
        self.txt_password.setFixedHeight(36)
        self.txt_password.setPlaceholderText(
            "Password..." if not self.user
            else "Kosongkan jika tidak diubah"
        )

        self.cb_role = QComboBox()
        self.cb_role.setFixedHeight(36)
        self.cb_role.addItems(["Super Admin", "Petugas Loket"])

        form.addRow("Username *", self.txt_username)
        form.addRow("Password", self.txt_password)
        form.addRow("Role *", self.cb_role)

        layout.addLayout(form)

        # Tombol
        btns = QHBoxLayout()
        btns.addStretch()

        btn_batal = QPushButton("Batal")
        btn_batal.clicked.connect(self.reject)

        self.btn_simpan = QPushButton("💾 Simpan")
        self.btn_simpan.clicked.connect(self._simpan)

        btns.addWidget(btn_batal)
        btns.addWidget(self.btn_simpan)
        layout.addLayout(btns)

    def _populate(self, user):

        self.txt_username.setText(user[1])
        self.txt_username.setEnabled(False)  # username tidak bisa diubah

        idx = self.cb_role.findText(user[2])
        if idx >= 0:
            self.cb_role.setCurrentIndex(idx)

    def _simpan(self):

        role = self.cb_role.currentText()
        password = self.txt_password.text()

        if self.user:
            # Mode edit
            ok, msg = UserController.update(
                self.user[0],
                role,
                password
            )
        else:
            # Mode tambah
            username = self.txt_username.text().strip()
            if not password:
                QMessageBox.warning(
                    self, "Validasi",
                    "Password wajib diisi untuk user baru."
                )
                return
            ok, msg = UserController.tambah(username, password, role)

        if ok:
            self.accept()
        else:
            QMessageBox.critical(self, "Error", msg)


class UserView(QWidget):

    def __init__(self):

        super().__init__()

        self.current_user_id = None  # diset dari main setelah login

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout(self)

        # ==================================
        # HEADER
        # ==================================

        hdr = QHBoxLayout()

        title = QLabel("👥 Manajemen Pengguna")
        title.setObjectName("DashboardTitle")
        hdr.addWidget(title)

        hdr.addStretch()

        self.btn_tambah = QPushButton("+ Tambah User")
        self.btn_tambah.setFixedHeight(36)
        self.btn_tambah.clicked.connect(self._tambah)
        hdr.addWidget(self.btn_tambah)

        layout.addLayout(hdr)

        # ==================================
        # TABEL
        # ==================================

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "ID", "Username", "Role", "Aksi"
        ])
        self.table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.Stretch
        )
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.verticalHeader().setVisible(False)

        layout.addWidget(self.table)

        self._refresh()

    def _refresh(self):

        rows = UserController.get_all()
        self.table.setRowCount(len(rows))

        for i, u in enumerate(rows):

            id_user, username, role = u

            self.table.setItem(i, 0, QTableWidgetItem(str(id_user)))
            self.table.setItem(i, 1, QTableWidgetItem(username))

            role_lbl = QLabel(role)
            role_lbl.setAlignment(Qt.AlignCenter)
            color = "#00D4FF" if role == "Super Admin" else "#FFD700"
            role_lbl.setStyleSheet(
                f"color:{color}; font-weight:bold; padding:4px;"
            )
            self.table.setCellWidget(i, 2, role_lbl)

            # Tombol aksi
            btn_frame = QFrame()
            btn_layout = QHBoxLayout(btn_frame)
            btn_layout.setContentsMargins(4, 2, 4, 2)
            btn_layout.setSpacing(4)

            btn_edit = QPushButton("✏ Edit")
            btn_edit.setFixedHeight(28)
            btn_edit.clicked.connect(
                lambda _, row=u: self._edit(row)
            )

            btn_hapus = QPushButton("🗑 Hapus")
            btn_hapus.setFixedHeight(28)
            btn_hapus.clicked.connect(
                lambda _, uid=id_user: self._hapus(uid)
            )

            # Tidak bisa hapus diri sendiri
            if self.current_user_id and id_user == self.current_user_id:
                btn_hapus.setEnabled(False)
                btn_hapus.setToolTip("Tidak bisa menghapus akun sendiri")

            btn_layout.addWidget(btn_edit)
            btn_layout.addWidget(btn_hapus)
            self.table.setCellWidget(i, 3, btn_frame)
            self.table.setRowHeight(i, 44)

    def _tambah(self):

        dlg = UserDialog(self)
        if dlg.exec():
            self._refresh()

    def _edit(self, user):

        dlg = UserDialog(self, user)
        if dlg.exec():
            self._refresh()

    def _hapus(self, id_user):

        reply = QMessageBox.question(
            self, "Konfirmasi",
            "Hapus user ini?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:

            ok, msg = UserController.delete(id_user)

            if ok:
                self._refresh()
            else:
                QMessageBox.critical(self, "Error", msg)
