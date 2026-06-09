from models.tiket_model import TiketModel
from models.histori_model import HistoriModel
from models.jadwal_model import JadwalModel


class DashboardController:

    @staticmethod
    def get_dashboard_data():

        total_tiket = (
            TiketModel.total_tiket()
        )

        total_pendapatan = (
            TiketModel.total_pendapatan()
        )

        total_histori = len(
            HistoriModel.get_all()
        )

        total_jadwal = len(
            JadwalModel.get_all()
        )

        return {

            "tiket":
                total_tiket,

            "pendapatan":
                total_pendapatan,

            "histori":
                total_histori,

            "jadwal":
                total_jadwal
        }

    @staticmethod
    def get_manifest():

        return (
            TiketModel.manifest()
        )