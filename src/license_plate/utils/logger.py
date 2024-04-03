"""
file : logger.py

author : Khaing Hsu Thwe
cdate : Thursday March 21st 2024
mdate : Thursday March 21st 2024
copyright: 2024 GlobalWalkers.inc. All rights reserved.
"""

import logging


class Logger(object):

    def __init__(self) -> None:
        self.log_file = "src/license_plate/utils/log.log"
        self.logger = logging.getLogger("mainlogger")
        self.logger.setLevel(logging.INFO)
        logging.basicConfig(
            filename=self.log_file,
            filemode="w",
            level=logging.INFO,
        )

        if not self.logger.handlers:
            # create a file handler
            handler = logging.FileHandler(self.log_file)
            handler.setLevel(logging.INFO)

            # create a logging format
            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(module)s - %(message)s"
            )
            handler.setFormatter(formatter)

            # add the file handler to the logger
            self.logger.addHandler(handler)

    def get_instance(self):
        return self.logger
