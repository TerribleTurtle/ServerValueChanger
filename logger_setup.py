"""
LoggerSetup Module

This module provides the LoggerSetup class, which configures logging for the application using settings
from a configuration manager. It sets up file and stream handlers, configures log levels, and ensures
that log directories exist.

Classes:
    LoggerSetup: Configures logging based on settings from a configuration manager.

Methods:
    __init__(self, config_manager): Initializes LoggerSetup and configures logging.
    configure_logging(self): Configures logging settings.
    close_handlers(): Closes all handlers of the root logger.
"""

import logging
import os

class LoggerSetup:
    """
    LoggerSetup configures logging for the application using settings from a config manager.
    """

    def __init__(self, config_manager):
        """
        Initialize LoggerSetup with a config manager and configure logging.

        :param config_manager: Instance of ConfigManager to get logging settings.
        """
        self.config_manager = config_manager
        self.configure_logging()

    def configure_logging(self):
        """
        Configure logging settings using the config manager.
        """
        log_level = self.config_manager.get_setting('logging.level')
        log_file = self.config_manager.get_setting('logging.file')

        log_level = getattr(logging, log_level.upper(), logging.INFO)

        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        file_handler = logging.FileHandler(log_file)
        stream_handler = logging.StreamHandler()

        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=log_level, format=log_format, handlers=[file_handler, stream_handler])

        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)

        # Debug statements to verify configuration
        root_logger.debug("Logger configured with level: %s", log_level)
        root_logger.debug("Logger handlers: %s", root_logger.handlers)

    @staticmethod
    def close_handlers():
        """
        Close all handlers of the root logger.
        """
        root_logger = logging.getLogger()
        handlers = root_logger.handlers[:]
        for handler in handlers:
            handler.flush()
            handler.close()
            root_logger.removeHandler(handler)
