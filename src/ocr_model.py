"""
file : ocr_model.py

author : Khaing Hsu Thwe
cdate : Thursday March 21st 2024
mdate : Thursday March 21st 2024
copyright: 2024 GlobalWalkers.inc. All rights reserved.
"""

from paddleocr import PaddleOCR
from config.configurations import OCR_PARAMS


class OCR_Model:
    def __init__(self) -> None:
        self.ocr = PaddleOCR(
            use_angle_cls=OCR_PARAMS["use_angle_cls"],
            lang=OCR_PARAMS["lang"],
            use_gpu=OCR_PARAMS["use_gpu"],
            enable_mkldnn=OCR_PARAMS["enable_mkldnn"],
            show_log=OCR_PARAMS["show_log"],
        )

    def image_to_text(self, img_path: str) -> tuple:

        result = self.ocr.ocr(img_path)
        text = ""
        conf = 0.0

        if result[0] is None:
            return text, conf
        text = result[0][0][1][0]
        conf = result[0][0][1][1]

        return text, conf
