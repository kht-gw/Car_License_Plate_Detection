"""
file : licenseplate_detector.py

author : Khaing Hsu Thwe
cdate : Thursday March 21st 2024
mdate : Thursday March 21st 2024
copyright: 2024 GlobalWalkers.inc. All rights reserved.
"""

from ultralytics import YOLO
from license_plate.utils.logger import Logger


class LicensePlateDetector:
    def __init__(self):
        self.logger = Logger().get_instance()
        self.weight_path = "weights/license_plate_detector.pt"
        self.model = YOLO(self.weight_path)

    def predict_image(self, img_path: str) -> list:
        results = self.model.predict(source=img_path)
        return results

    def predict_video(self, video_path: str) -> list:
        results = self.model.predict(source=video_path)
        return results
