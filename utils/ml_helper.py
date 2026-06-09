from models.jadwal_model import (
    JadwalModel
)

from models.tiket_model import (
    TiketModel
)


class MLHelper:

    @staticmethod
    def analisis_kepadatan():

        hasil = []

        semua_jadwal = (
            JadwalModel.get_all()
        )

        for jadwal in semua_jadwal:

            id_jadwal = jadwal[0]

            nama_kapal = jadwal[1]

            kapasitas = jadwal[6]

            terjual = (
                TiketModel
                .total_booking_jadwal(
                    id_jadwal
                )
            )

            if kapasitas == 0:

                occupancy = 0

            else:

                occupancy = round(

                    (
                        terjual
                        /
                        kapasitas
                    ) * 100,

                    2
                )

            if occupancy >= 80:

                status = "🔴 PADAT"

                rekomendasi = (
                    "Tambahkan armada cadangan."
                )

            elif occupancy >= 50:

                status = "🟡 SEDANG"

                rekomendasi = (
                    "Pantau reservasi secara berkala."
                )

            else:

                status = "🟢 SEPI"

                rekomendasi = (
                    "Kapasitas masih mencukupi."
                )

            hasil.append({

                "kapal":
                nama_kapal,

                "terjual":
                terjual,

                "kapasitas":
                kapasitas,

                "occupancy":
                occupancy,

                "status":
                status,

                "rekomendasi":
                rekomendasi
            })

        return hasil