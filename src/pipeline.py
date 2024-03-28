"""
file : pipeline.py

author : Khaing Hsu Thwe
cdate : Thursday March 21st 2024
mdate : Thursday March 21st 2024
copyright: 2024 GlobalWalkers.inc. All rights reserved.
"""

import cv2
import os
import time
import json
import mimetypes
from licenseplate_detector import LicensePlateDetector
from ocr_model import OCR_Model
from utils.logger import Logger
from utils.directory_manager import DirectoryManager
from config.configurations import (
    IMAGE_COUNT,
    MIN_BBOX_HEIGHT,
    MIN_BBOX_WIDTH,
    BBOX_COLOR,
    OCR_TEXT_COLOR,
    TEXT_BG_COLOR,
)


class Pipeline:
    def __init__(self):
        self.final_results = []
        self.detector = LicensePlateDetector()
        self.ocr_model = OCR_Model()
        self.dir_manager = DirectoryManager()
        self.logger = Logger().get_instance()

    def detect_and_ocr(self, mode: str, input_path: str, save_dir: str) -> None:
        """Detect Car License Plates  and Extract Text with OCR
        Args:
            mode (str) : IMAGE mode or VIDEO mode
            input_path(str) : path of images or a single image or a single video
            save_dir (str) : path of output results

        Returns:
            results: list of information containing detectin results
        """

        if mode == "IMAGE":  # image mode
            if os.path.isdir(input_path):
                if len(os.listdir(input_path)) == 0:
                    self.logger.error("Empty Directory!")
                    exit()

                count = self.dir_manager.count_images(input_path)
                if count > IMAGE_COUNT:
                    self.logger.warn(
                        "Inside  detect_and_ocr : Cannot accept more than 1000 images."
                    )
                    exit()

            elif os.path.isfile(input_path):
                if not self.dir_manager.is_file_image:
                    self.logger.ERROR(
                        "Inside - detect_and_ocr : Can accept imageonly in jpg or png format."
                    )
                    exit()
            self.create_image_mode_dirs(save_dir)  # create dirs to store results
            results = self.detector.predict_image(input_path)
            final_results = self.process_img_results(results, save_dir)

            self.save_as_json(final_results, save_dir)  # save results in json file
            self.logger.info(
                "\n Detection finished! You can check the detected images inside : "
                + save_dir
            )

        elif mode == "VIDEO":
            if os.path.isfile(input_path) and mimetypes.guess_type(input_path)[
                0
            ].startswith("video"):

                self.process_video(input_path, save_dir)
                self.logger.info(
                    "Finish processing video ! You can check the detected video inside : "
                    + save_dir
                )
            else:
                self.logger.error(
                    "Input path is not a video file! Video Mode only accepts a video file"
                )

    def process_img_results(self, results: list, save_dir: str) -> list:
        """Process Detection Results
        Args:
            results (str) : detection results
            save_dir (str) : path of output results

        Returns:
            results: list of detectin results
        """

        output_results = []
        for result in results:  # loop detection result of  images
            json_dict = {}  # to store results values for json file output
            filename = self.dir_manager.extract_filename(result.path)
            json_dict["file_name"] = filename
            image = cv2.imread(result.path)

            if image is None:
                self.logger.error("Cannot read the image : ", result.path)
                break

            boxes_xyxy = result.boxes.xyxy.tolist()
            conf_scores = result.boxes.conf.tolist()
            box_conf_pair = list(zip(boxes_xyxy, conf_scores))

            crop_id = 1
            detection_details = []

            for bbox, detection_conf in box_conf_pair:
                detection_detail = {}
                bbox = [round(x, 3) for x in bbox]

                x1, y1, x2, y2 = bbox
                x1 = int(x1)
                y1 = int(y1)
                x2 = int(x2)
                y2 = int(y2)
                coords = [x1, y1, x2, y2]
                width = x2 - x1
                height = y2 - y1

                cropped_img = image[y1:y2, x1:x2]

                # ocr process
                text, text_conf = self.ocr_model.image_to_text(cropped_img)

                if text == "":
                    text = "license_plate"

                # save results and images if the image is not small
                if width > MIN_BBOX_WIDTH and height > MIN_BBOX_HEIGHT:
                    detection_detail["bbox_coordinate"] = bbox
                    detection_detail["detection_score"] = round(detection_conf, 3)
                    detection_detail["ocr_text"] = text
                    detection_detail["ocr_score"] = round(text_conf, 3)
                    detection_details.append(detection_detail)

                    img_filename = filename.split(".")[0]
                    crop_img_name = img_filename + "_" + str(crop_id) + ".jpg"
                    crop_out_dir = os.path.join(save_dir, "crops")

                    self.save_img(cropped_img, crop_out_dir, crop_img_name)
                    crop_id += 1

                bbox_img = self.get_bbox_image(image, coords)
                bbox_img = self.get_visualized_img(bbox_img, coords, text)

            json_dict["results"] = detection_details
            output_results.append(json_dict)

            bbox_image_dir = os.path.join(save_dir, "bbox_images")
            self.save_img(bbox_img, bbox_image_dir, filename)  # save bbox image

        return output_results

    def process_video(self, video_path: str, save_dir: str) -> None:
        """Detect car license plates and extract text
        Args:
            video_path (str) : path of video file
            save_dir (str) : path of output results

        """
        cap = cv2.VideoCapture(video_path)
        output_dir = os.path.join(save_dir, "output_video.mp4")
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Specify the codec
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        out = cv2.VideoWriter(output_dir, fourcc, fps, (width, height))

        index = 0
        while True:
            ret, frame = cap.read()

            if not ret:
                break

            # detect license plates in a frame
            results = self.detector.predict_video(frame)

            # extract text using ocr
            frame, speed = self.process_video_results(results, frame)

            # font using to display FPS
            font = cv2.FONT_HERSHEY_SIMPLEX

            # Calculating the fps
            if speed > 0:
                fps = 1.0 / speed
            else:
                fps = 0

            fps = int(fps)
            fps = str(fps)

            fps_text = "FPS: " + fps
            # putting the FPS count on the frame
            cv2.putText(
                frame, fps_text, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA
            )
            out.write(frame)
            index += 1
        out.release()
        cap.release()

    def process_video_results(self, results: list, frame: object) -> tuple:
        """Process Detection Results of a frame
        Args:
            results (list) : detection results
            frame (object) : frame/ image object

        Returns:
            frame: modified frame with bbox
            total_time: time taken for detection process and ocr process
        """
        total_time = 0
        for result in results:  # detection results in one frame
            boxes_xyxy = result.boxes.xyxy.tolist()

            speed = result.speed["inference"]
            speed = speed / 1000
            for bbox in boxes_xyxy:
                x1, y1, x2, y2 = bbox
                x1 = int(x1)
                y1 = int(y1)
                x2 = int(x2)
                y2 = int(y2)
                coords = [x1, y1, x2, y2]

                cropped_img = frame[y1:y2, x1:x2]

                total_time = speed
                start_time = time.time()
                # ocr
                text, text_conf = self.ocr_model.image_to_text(cropped_img)
                end_time = time.time()
                total_time += end_time - start_time
                if text == "":
                    text = "license_plate"

                frame = self.get_bbox_image(frame, coords)
                frame = self.get_visualized_img(frame, coords, text)
        return frame, total_time

    def get_bbox_image(self, image: object, coords: list) -> object:
        """Visualize image with bounding box
        Args:
            image (object) : image
            coords (list) : list of bounding box coordinates

        Returns:
            img: image drawn bounding box on it
        """
        try:
            x1, y1, x2, y2 = coords
            # license plate bounding box
            img = cv2.rectangle(image, (x1, y1), (x2, y2), BBOX_COLOR, 2)

        except Exception as error:
            self.logger.error("error occured!", error)
        else:
            return img

    def get_visualized_img(self, image: object, coords: list, text: str) -> object:
        """Visualize image with OCR Text
        Args:
            image (object) : image
            coords (list) : list of bounding box coordinates
            text: OCR text

        Returns:
            img: image with ocr text on it
        """
        try:
            x1, y1, x2, y2 = coords
            w = x2 - x1

            if w < 30:
                font_scale = 1
            else:
                font_scale = 1.1

            (text_width, text_height), _ = cv2.getTextSize(
                text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 5
            )
            # put ocr text
            img = cv2.rectangle(
                image,
                (x1, y1 - text_height - 20),
                (x2 + text_width, y1),
                TEXT_BG_COLOR,
                -1,
            )

            img = cv2.putText(
                img,
                text,
                (x1 + int(w / 2), y1 - int(text_height / 2)),
                cv2.FONT_HERSHEY_SIMPLEX,
                font_scale,
                OCR_TEXT_COLOR,
                2,
            )
        except Exception as error:
            self.logger.error("error occured! ", error)
        else:
            return img

    def create_image_mode_dirs(self, root_output_dir: str) -> None:
        self.dir_manager.create_dir(os.path.join(root_output_dir, "crops"))
        self.dir_manager.create_dir(os.path.join(root_output_dir, "bbox_images"))

    def save_img(self, image, output_dir: str, file_name: str) -> None:
        save_img_file = os.path.join(output_dir, file_name)
        cv2.imwrite(save_img_file, image)

    def save_as_json(self, results: list, output_dir: str) -> None:

        json_filename = os.path.join(output_dir, "results.json")
        with open(json_filename, "w") as outfile:
            json.dump(results, outfile, indent=2)
