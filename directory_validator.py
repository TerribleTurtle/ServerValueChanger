"""
This module contains the DirectoryValidator class, which validates the existence
of required directory paths.

Classes:
    DirectoryValidator: A class to validate the existence of required directory paths.

Methods:
    __init__(self, paths): Initializes the DirectoryValidator with a list of paths.
    validate(self): Validates the existence of the paths provided during initialization.
"""

import os
import logging

class DirectoryValidator:
    """
    A class to validate the existence of required directory paths.
    """

    def __init__(self, paths):
        """
        Initializes the DirectoryValidator with a list of paths.

        :param paths: List of paths to validate.
        """
        self.paths = paths

    def validate(self):
        """
        Validates the existence of the paths provided during initialization.

        :raises FileNotFoundError: If any of the paths do not exist.
        """
        missing_paths = []
        for path in self.paths:
            if not os.path.exists(path):
                missing_paths.append(path)

        if missing_paths:
            logging.error("Missing required paths: %s", missing_paths)
            raise FileNotFoundError(f"Missing required paths: {missing_paths}")
        else:
            logging.info("All required paths are present.")
