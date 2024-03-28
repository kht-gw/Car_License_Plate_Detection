"""
file : configurations.py

author : Khaing Hsu Thwe
cdate : Friday March 22nd 2024
mdate : Friday March 22nd 2024
copyright: 2024 GlobalWalkers.inc. All rights reserved.
"""

OCR_PARAMS = {
    "use_angle_cls": True,
    "lang": "en",
    "use_gpu": False,
    "det": False,
    "enable_mkldnn": False,
    "show_log": False,
}

DETECTOR_PARAMS = {
    'conf': 0.25,
     
}

IMAGE_COUNT = 1000

MIN_BBOX_WIDTH = 23
MIN_BBOX_HEIGHT = 13

BBOX_COLOR = (0, 255, 0)
OCR_TEXT_COLOR = (255, 255, 255)
TEXT_BG_COLOR = (0, 0, 0)
