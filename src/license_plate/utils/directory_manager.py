"""
file : DirectoryManager.py

author : Khaing Hsu Thwe
cdate : Friday March 22nd 2024
mdate : Friday March 22nd 2024
copyright: 2024 GlobalWalkers.inc. All rights reserved.
"""

import os


class DirectoryManager:
    def __init__(self) -> None:
        pass

    def create_dir(self, directory: str) -> None:
        if not os.path.exists(directory):
            os.makedirs(directory)

    def is_file_image(self, path: str) -> None:
        if path.endswith(".jpg") or path.endswith(".png"):
            return True
        else:
            return False

    def count_images(self, path: str) -> int:
        images = [
            f
            for f in os.listdir(path)
            if (f.endswith(".jpg") or f.endswith(".png"))
            and os.path.isfile(os.path.join(path, f))
        ]
        count = len(images)
        return count

    def extract_filename(self, path: str) -> str:
        filename = path.split("/")[-1]
        return filename
