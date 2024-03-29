"""
file : test_pipeline.py

author : Khaing Hsu Thwe
cdate : Friday March 29th 2024
mdate : Friday March 29th 2024
copyright: 2024 GlobalWalkers.inc. All rights reserved.
"""

import unittest
from src.pipeline import Pipeline
import os
from utils.logger import Logger


class test_image(unittest.TestCase):
    def setUp(self) -> None:
        self.pipeline = Pipeline()

    def test_image(self):
        text = ""
        current_dir = os.getcwd()
        img_path = os.path.join(current_dir, "assets/Cars297.png")

        out_results = self.pipeline.detect_and_ocr(
            "IMAGE", img_path, current_dir, False
        )
        results = out_results[0]["results"]
        text = results[0]["ocr_text"]
        text = text.replace(" ", "")

        self.assertEqual(text, "IM4U555")


if __name__ == "__main__":
    unittest.main()
