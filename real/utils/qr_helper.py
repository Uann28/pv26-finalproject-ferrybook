import os
import qrcode


class QRHelper:

    @staticmethod
    def generate(
        ticket_id
    ):

        folder = "exports"

        if not os.path.exists(
            folder
        ):

            os.makedirs(
                folder
            )

        file_path = os.path.join(

            folder,

            f"qr_{ticket_id}.png"
        )

        qr_data = f"""

FERRYBOOK

ID TIKET:
{ticket_id}

STATUS:
VALID

"""

        img = qrcode.make(
            qr_data
        )

        img.save(
            file_path
        )

        return file_path