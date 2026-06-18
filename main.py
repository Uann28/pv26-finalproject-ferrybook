import sys
import os

from PySide6.QtWidgets import (

    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QStackedWidget,
    QMessageBox
)

from views.login_view import LoginView
from views.dashboard_view import DashboardView
from views.jadwal_view import JadwalView
from views.reservasi_view import ReservasiView
from views.ai_view import AIView

from views.laporan_view import LaporanView

from views.about_view import AboutView

from views.user_view import UserView

from views.widgets.sidebar import Sidebar

from controllers.login_controller import (
    LoginController
)

from controllers.dashboard_controller import (
    DashboardController
)

from controllers.jadwal_controller import (
    JadwalController
)

from controllers.reservasi_controller import (
    ReservasiController
)

from controllers.ai_controller import (
    AIController
)

from controllers.export_controller import (
    ExportController
)

from models.jadwal_model import (
    JadwalModel
)

from utils.export_helper import (
    ExportHelper
)


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "FerryBook v2.0"
        )

        self.resize(
            1400,
            850
        )

        self.dark_mode = False

        self.current_user = None

        self.setup_ui()

        self.load_theme(
            "themes/light.qss"
        )

    # ==================================
    # UI
    # ==================================

    def setup_ui(self):

        self.main_stack = (
            QStackedWidget()
        )

        self.setCentralWidget(
            self.main_stack
        )

        # LOGIN

        self.login_view = (
            LoginView()
        )

        self.main_stack.addWidget(
            self.login_view
        )

        # APP PAGE

        self.app_page = QWidget()

        app_layout = QHBoxLayout(
            self.app_page
        )

        self.sidebar = Sidebar()

        app_layout.addWidget(
            self.sidebar
        )

        self.pages = (
            QStackedWidget()
        )

        app_layout.addWidget(
            self.pages
        )

        self.dashboard_view = (
            DashboardView()
        )

        self.jadwal_view = (
            JadwalView()
        )

        self.reservasi_view = (
            ReservasiView()
        )

        self.ai_view = (
            AIView()
        )

        self.laporan_view = (
            LaporanView()
        )

        self.about_view = (
            AboutView()
        )

        self.user_view = (
            UserView()
        )

        self.pages.addWidget(
            self.dashboard_view
        )

        self.pages.addWidget(
            self.jadwal_view
        )

        self.pages.addWidget(
            self.reservasi_view
        )

        self.pages.addWidget(
            self.ai_view
        )

        self.pages.addWidget(
            self.laporan_view
        )

        self.pages.addWidget(
            self.about_view
        )

        self.pages.addWidget(
            self.user_view
        )

        self.main_stack.addWidget(
            self.app_page
        )

        self.connect_signals()

    # ==================================
    # SIGNAL
    # ==================================

    def connect_signals(self):

        self.login_view.btn_login.clicked.connect(
            self.login
        )

        self.sidebar.btn_dashboard.clicked.connect(
            self.buka_dashboard
        )

        self.sidebar.btn_jadwal.clicked.connect(
            self.buka_jadwal
        )

        self.sidebar.btn_reservasi.clicked.connect(
            self.buka_reservasi
        )

        self.sidebar.btn_ai.clicked.connect(
            self.buka_ai
        )

        self.sidebar.btn_laporan.clicked.connect(
            self.buka_laporan
        )

        self.sidebar.btn_about.clicked.connect(
            self.buka_about
        )

        self.sidebar.btn_user.clicked.connect(
            self.buka_user
        )

        self.sidebar.btn_export.clicked.connect(
            self.export_manifest
        )

        self.sidebar.btn_theme.clicked.connect(
            self.toggle_theme
        )

        self.sidebar.btn_logout.clicked.connect(
            self.logout
        )

        self.jadwal_view.btn_simpan.clicked.connect(
            self.simpan_jadwal
        )

        self.jadwal_view.btn_edit.clicked.connect(
            self.edit_jadwal
        )

        self.jadwal_view.btn_hapus.clicked.connect(
            self.hapus_jadwal
        )

        self.reservasi_view.btn_proses.clicked.connect(
            self.proses_reservasi
        )

        self.reservasi_view.btn_cari.clicked.connect(
            self.cari_kapal
        )

        self.reservasi_view.cb_golongan.currentIndexChanged.connect(
            self.update_tarif
        )

        self.reservasi_view.cb_kapal.currentIndexChanged.connect(
            self.update_sisa_kursi
        )

    # ==================================
    # THEME
    # ==================================

    def load_theme(
        self,
        path
    ):

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            self.setStyleSheet(
                f.read()
            )

    def toggle_theme(self):

        if self.dark_mode:

            self.load_theme(
                "themes/light.qss"
            )

        else:

            self.load_theme(
                "themes/dark.qss"
            )

        self.dark_mode = (
            not self.dark_mode
        )

    # ==================================
    # LOGIN
    # ==================================

    def login(self):
        username = (
            self.login_view
            .txt_username
            .text()
        )

        password = (
            self.login_view
            .txt_password
            .text()
        )

        user = (
            LoginController.authenticate(
                username,
                password
            )
        )

        if not user:

            QMessageBox.warning(

                self,

                "Login",

                "Username atau Password salah"
            )

            return

        self.current_user = user

        role = user[2]

        # Kirim id user yang sedang login ke user_view
        # supaya tombol hapus diri sendiri dinonaktifkan
        self.user_view.current_user_id = user[0]

        self.sidebar.set_role(
            role
        )

        self.main_stack.setCurrentWidget(
            self.app_page
        )

        if role == "Super Admin":

            self.buka_dashboard()

        else:

            self.buka_reservasi()

    # ==================================
    # DASHBOARD
    # ==================================

    def buka_dashboard(self):
        data = (
            DashboardController
            .get_dashboard_data()
        )

        self.dashboard_view.set_dashboard_data(

            data["tiket"],

            data["pendapatan"],

            data["jadwal"],

            data["histori"]
        )

        manifest = (
            DashboardController
            .get_manifest()
        )

        self.dashboard_view.load_manifest(
            manifest
        )

        self.pages.setCurrentWidget(
            self.dashboard_view
        )

    # ==================================
    # AI
    # ==================================

    def buka_ai(self):
        data = (
            AIController
            .get_analisis()
        )

        self.ai_view.load_data(
            data
        )

        self.pages.setCurrentWidget(
            self.ai_view
        )

    # ==================================
    # JADWAL
    # ==================================

    def buka_jadwal(self):

        data = (
            JadwalController
            .get_all()
        )


        self.jadwal_view.load_data(
            data
        )

        self.pages.setCurrentWidget(
            self.jadwal_view
        )

    def simpan_jadwal(self):

        try:

            JadwalController.tambah(

                self.jadwal_view
                .txt_nama_kapal.text(),

                self.jadwal_view
                .cb_asal.currentText(),

                self.jadwal_view
                .cb_tujuan.currentText(),

                self.jadwal_view
                .date_berangkat
                .date()
                .toString(
                    "yyyy-MM-dd"
                ),

                self.jadwal_view
                .cb_jam.currentText(),

                int(
                    self.jadwal_view
                    .txt_kapasitas.text()
                )
            )

            QMessageBox.information(
                self,
                "Sukses",
                "Jadwal berhasil ditambahkan"
            )

            self.buka_jadwal()

        except Exception as e:

            QMessageBox.warning(
                self,
                "Error",
                str(e)
            )

    def edit_jadwal(self):
        row = (
            self.jadwal_view
            .table_jadwal
            .currentRow()
        )

        if row < 0:

            QMessageBox.warning(
                self,
                "Edit",
                "Pilih data terlebih dahulu"
            )

            return

        id_jadwal = int(

            self.jadwal_view
            .table_jadwal
            .item(row, 0)
            .text()
        )

        JadwalController.update(

            id_jadwal,

            self.jadwal_view
            .txt_nama_kapal.text(),

            self.jadwal_view
            .cb_asal.currentText(),

            self.jadwal_view
            .cb_tujuan.currentText(),

            self.jadwal_view
            .date_berangkat
            .date()
            .toString(
                "yyyy-MM-dd"
            ),

            self.jadwal_view
            .cb_jam.currentText(),

            int(
                self.jadwal_view
                .txt_kapasitas.text()
            )
        )

        QMessageBox.information(
            self,
            "Sukses",
            "Jadwal berhasil diubah"
        )

        self.buka_jadwal()

    def hapus_jadwal(self):

        row = (
            self.jadwal_view
            .table_jadwal
            .currentRow()
        )

        if row < 0:
            return

        id_jadwal = int(

            self.jadwal_view
            .table_jadwal
            .item(row, 0)
            .text()
        )

        JadwalController.hapus(
            id_jadwal
        )

        self.buka_jadwal()

    def update_tarif(self):

        harga = (

            ReservasiController
            .get_tarif(

                self.reservasi_view
                .cb_golongan.currentText()
            )
        )

        self.reservasi_view.lbl_harga.setText(
            f"Rp {harga:,.0f}"
        )

    # ==================================
    # RESERVASI
    # ==================================

    def buka_reservasi(self):
        self.reservasi_view.cb_kapal.clear()

        self.reservasi_view.lbl_sisa.setText(
            "-"
        )

        self.pages.setCurrentWidget(
            self.reservasi_view
        )

        self.update_tarif()

    def proses_reservasi(self):
        try:

            id_jadwal = (
                self.reservasi_view
                .cb_kapal
                .currentData()
            )

            if not id_jadwal:

                QMessageBox.warning(
                    self,
                    "Reservasi",
                    "Pilih kapal terlebih dahulu"
                )

                return

            nama = (
                self.reservasi_view
                .txt_nama.text()
                .strip()
            )

            if not nama:

                QMessageBox.warning(
                    self,
                    "Reservasi",
                    "Nama wajib diisi"
                )

                return

            golongan = (
                self.reservasi_view
                .cb_golongan.currentText()
            )

            nopol = (
                self.reservasi_view
                .txt_nopol.text()
                .strip()
            )

            if golongan != "Pejalan Kaki" and not nopol:

                QMessageBox.warning(
                    self,
                    "Reservasi",
                    "Nomor polisi wajib diisi"
                )

                return

            id_tiket, total = (

                ReservasiController
                .simpan_tiket(

                    id_jadwal,

                    nama,

                    golongan,

                    nopol
                )
            )

            jadwal = (
                JadwalModel
                .get_by_id(
                    id_jadwal
                )
            )

            pdf = (
                ExportHelper
                .cetak_tiket(

                    id_tiket,

                    nama,

                    golongan,

                    jadwal[1],

                    jadwal[2],

                    jadwal[3],

                    jadwal[4],

                    jadwal[5],

                    total
                )
            )

            QMessageBox.information(

                self,

                "Reservasi Berhasil",

                f"""
    ID Tiket : {id_tiket}

    PDF :
    {pdf}
    """
            )

            self.buka_dashboard()

        except Exception as e:

            QMessageBox.warning(
                self,
                "Error",
                str(e)
            )

    def update_sisa_kursi(self):

        id_jadwal = (
            self.reservasi_view
            .cb_kapal
            .currentData()
        )

        if not id_jadwal:

            self.reservasi_view.lbl_sisa.setText(
                "-"
            )

            return

        sisa = (
            JadwalModel
            .kapasitas_tersisa(
                id_jadwal
            )
        )

        self.reservasi_view.lbl_sisa.setText(
            f"{sisa} Kursi"
        )

    def cari_kapal(self):

        hasil = (

            ReservasiController
            .cari_kapal(

                self.reservasi_view
                .cb_asal.currentText(),

                self.reservasi_view
                .cb_tujuan.currentText(),

                self.reservasi_view
                .date_berangkat
                .date()
                .toString(
                    "yyyy-MM-dd"
                ),

                self.reservasi_view
                .cb_jam.currentText()
            )
        )

        self.reservasi_view.cb_kapal.clear()

        if not hasil:

            QMessageBox.information(

                self,

                "Jadwal",

                "Tidak ada kapal tersedia"
            )

            self.reservasi_view.lbl_sisa.setText(
                "-"
            )

            return

        for kapal in hasil:

            sisa = (
                JadwalModel
                .kapasitas_tersisa(
                    kapal[0]
                )
            )

            self.reservasi_view.cb_kapal.addItem(

                f"{kapal[1]} (Sisa {sisa})",

                kapal[0]
            )

    # ==================================
    # USER MANAGEMENT
    # ==================================

    def buka_user(self):

        self.user_view._refresh()

        self.pages.setCurrentWidget(
            self.user_view
        )

    # ==================================
    # LAPORAN
    # ==================================

    def buka_laporan(self):

        self.pages.setCurrentWidget(
            self.laporan_view
        )

    # ==================================
    # ABOUT
    # ==================================

    def buka_about(self):

        self.pages.setCurrentWidget(
            self.about_view
        )

    # ==================================
    # EXPORT
    # ==================================

    def export_manifest(self):

        file = (
            ExportController
            .export_manifest()
        )

        QMessageBox.information(

            self,

            "Export Berhasil",

            f"""
Manifest berhasil diexport

{file}
"""
        )

    # ==================================
    # LOGOUT
    # ==================================

    def logout(self):

        self.login_view.txt_username.clear()

        self.login_view.txt_password.clear()

        self.main_stack.setCurrentWidget(
            self.login_view
        )


app = QApplication(
    sys.argv
)

window = MainWindow()

window.show()

sys.exit(
    app.exec()
)