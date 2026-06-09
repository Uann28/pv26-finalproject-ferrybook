from datetime import datetime

from models.tiket_model import (
    TiketModel
)

from models.tarif_model import (
    TarifModel
)

from models.histori_model import (
    HistoriModel
)

from models.jadwal_model import (
    JadwalModel
)


class ReservasiController:

    @staticmethod
    def get_tarif(
        golongan
    ):

        return (
            TarifModel.get_harga(
                golongan
            )
        )

    @staticmethod
    def cari_kapal(

        asal,

        tujuan,

        tanggal,

        jam
    ):

        return (
            JadwalModel.cari_jadwal(

                asal,

                tujuan,

                tanggal,

                jam
            )
        )

    @staticmethod
    def simpan_tiket(

        id_jadwal,

        nama,

        golongan,

        nopol
    ):
        
        sisa = (
            JadwalModel
            .kapasitas_tersisa(
                id_jadwal
            )
        )

        if sisa <= 0:

            raise Exception(
                "Kapal sudah penuh"
            )

        total = (
            TarifModel.get_harga(
                golongan
            )
        )

        id_tiket = (

            TiketModel.tambah(

                id_jadwal,

                nama,

                golongan,

                nopol,

                total
            )
        )

        HistoriModel.tambah(

            datetime.now().strftime(
                "%Y-%m-%d"
            ),

            id_jadwal
        )

        return (
            id_tiket,
            total
        )