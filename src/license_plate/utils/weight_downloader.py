"""
file : weight_downloader.py

author : Khaing Hsu Thwe
cdate : Thursday April 4th 2024
mdate : Thursday April 4th 2024
copyright: 2024 GlobalWalkers.inc. All rights reserved.
"""

import urllib.request

FILE_ID = "1muzAWdrMfQW67-iT-JclDJaT6Fea_ynQ"


def download_file_from_google_drive(id, destination):
    try:
        URL = "https://drive.google.com/uc?export=download&id=" + id
        print("Downloading weight file...")
        session = urllib.request.urlopen(URL)
        token = session.headers.get("Content-Disposition")
        if token is None:
            print("Unable to download file. Check the file ID.")
            return

        file_bytes = session.read()
        session.close()

        with open(destination, "wb") as f:
            f.write(file_bytes)

        print("Weight file download completed successfully.")
    except Exception as error:
        print(error)


if __name__ == "__main__":
    file_id = "1muzAWdrMfQW67-iT-JclDJaT6Fea_ynQ"  # the ID of the file
    destination_path = (
        "weights/license_plate_detector.pt"  # Replace with the destination file path
    )

    download_file_from_google_drive(file_id, destination_path)
