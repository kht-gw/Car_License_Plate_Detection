"""
file : test_pipeline.py

author : Khaing Hsu Thwe
cdate : Friday March 29th 2024
mdate : Friday March 29th 2024
copyright: 2024 GlobalWalkers.inc. All rights reserved.
"""

import os
import unittest

from src.license_plate.pipeline import Pipeline
from src.license_plate.utils.weight_downloader import (
    FILE_ID,
    download_file_from_google_drive,
)


class test_image(unittest.TestCase):
    def setUp(self) -> None:
        self.pipeline = Pipeline()

    def test_image(self):
        if not os.path.exists("weights"):
            os.mkdir("weights")

        if not os.path.exists("weights/license_plate_detector.pt"):
            weight_file_path = os.path.join("weights", "license_plate_detector.pt")
            download_file_from_google_drive(FILE_ID, weight_file_path)
        text = ""
        current_dir = os.getcwd()
        img_path = os.path.join(current_dir, "assets/images/Cars297.png")

        out_results = self.pipeline.detect_and_ocr(
            "IMAGE", img_path, current_dir, False
        )
        results = out_results[0]["results"]
        text = results[0]["ocr_text"]
        text = text.replace(" ", "")

        self.assertEqual(text, "IM4U555")


if __name__ == "__main__":
    unittest.main()
