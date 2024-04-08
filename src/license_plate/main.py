"""
file : main.py

author : Khaing Hsu Thwe
cdate : Thursday March 28th 2024
mdate : Thursday March 28th 2024
copyright: 2024 GlobalWalkers.inc. All rights reserved.
"""

import argparse
import os
import sys

from utils.weight_downloader import FILE_ID, download_file_from_google_drive

from license_plate.pipeline import Pipeline
from license_plate.utils.logger import Logger

if __name__ == "__main__":
    logger = Logger().get_instance()
    logger = Logger().get_instance()
    # get car license plate detection model from google drive
    if not os.path.exists("weights"):
        os.mkdir("weights")

    # if weights directory exists but empty
    # weights dir is removed and created again,
    # weights dir is removed and created again,
    # otherwise, can face permession denied to download inside esisting empty dir

    elif not os.path.exists("weights/license_plate_detector.pt"):
        os.rmdir("weights")
        os.mkdir("weights")

    if not os.path.exists("weights/license_plate_detector.pt"):

        weight_file_path = os.path.join("weights", "license_plate_detector.pt")
        download_file_from_google_drive(FILE_ID, weight_file_path)
    else:
        logger.info("Weight file alreary downloaded. Continue Object Detection...")
    pipeline = Pipeline()

    parser = argparse.ArgumentParser(description="Car License Plate Detection and OCR")
    parser.add_argument(
        "mode",
        help="Inference mode : Type 1 for IMAGE inference and 2 for Video Inference",
        type=int,
    )
    parser.add_argument(
        "input_dir",
        help="Path to the input image/images or video",
        type=str,
    )
    parser.add_argument(
        "output_dir", help="Path to the output file to store results", type=str
    )
    args = parser.parse_args()

    try:
        options = parser.parse_args()
    except Exception as error:
        logger.error(error)

        sys.exit(0)

    input_type = args.mode
    input_dir = args.input_dir
    output_dir = args.output_dir
    mode = ""
    if input_type == 1:
        mode = "IMAGE"
        pipeline.detect_and_ocr(mode, input_dir, output_dir)
    elif input_type == 2:
        mode = "VIDEO"
        pipeline.detect_and_ocr(mode, input_dir, output_dir)
    else:
        logger.error("Invalid mode type.  -h mode for more information")
