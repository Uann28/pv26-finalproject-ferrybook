from models.jadwal_model import JadwalModel


class JadwalController:

    @staticmethod
    def get_all():

        return JadwalModel.get_all()

    @staticmethod
    def tambah(
        nama_kapal,
        asal,
        tujuan,
        tanggal,
        jam,
        kapasitas,
    ):

        JadwalModel.tambah(
            nama_kapal,
            asal,
            tujuan,
            tanggal,
            jam,
            kapasitas,

        )

    @staticmethod
    def update(
        id_jadwal,
        nama_kapal,
        asal,
        tujuan,
        tanggal,
        jam,
        kapasitas,
    ):

        JadwalModel.update(

            id_jadwal,

            nama_kapal,

            asal,

            tujuan,

            tanggal,

            jam,

            kapasitas,


        )

    @staticmethod
    def hapus(
        id_jadwal
    ):

        JadwalModel.delete(
            id_jadwal
        )

    @staticmethod
    def get_sisa_kursi(
        id_jadwal
    ):

        return JadwalModel.kapasitas_tersisa(
            id_jadwal
        )
    
    @staticmethod
    def cari_jadwal(
        asal,
        tujuan,
        tanggal,
        jam
    ):

        return JadwalModel.cari_jadwal(

            asal,

            tujuan,

            tanggal,

            jam
        )