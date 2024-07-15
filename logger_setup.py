# logger_setup.py
import logging
import os
from config_manager import ConfigManager

class LoggerSetup:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.configure_logging()

    def configure_logging(self):
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
        root_logger.debug(f"Logger configured with level: {log_level}")
        root_logger.debug(f"Logger handlers: {root_logger.handlers}")

    @staticmethod
    def close_handlers():
        root_logger = logging.getLogger()
        handlers = root_logger.handlers[:]
        for handler in handlers:
            handler.flush()
            handler.close()
            root_logger.removeHandler(handler)
