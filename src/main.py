"""
file : main.py

author : Khaing Hsu Thwe
cdate : Thursday March 28th 2024
mdate : Thursday March 28th 2024
copyright: 2024 GlobalWalkers.inc. All rights reserved.
"""

import argparse
import sys
from pipeline import Pipeline
from utils.logger import Logger


if __name__ == "__main__":
    pipeline = Pipeline()
    logger = Logger().get_instance()

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
        print(error)

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
        print("Invalid mode type.  -h mode for more information")
