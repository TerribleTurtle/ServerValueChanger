import unittest
import logging
import os
from config_manager import ConfigManager
from logger_setup import LoggerSetup

class TestLoggerSetup(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a temporary config file for testing
        cls.test_config_path = 'test_config.json'
        with open(cls.test_config_path, 'w') as f:
            f.write('''
            {
              "paths": {},
              "logging": {
                "level": "INFO",
                "file": "test_app.log"
              },
              "backup": {}
            }
            ''')

    @classmethod
    def tearDownClass(cls):
        # Close handlers to release the log file
        LoggerSetup.close_handlers()

        # Remove the temporary config file and log file after tests
        if os.path.exists(cls.test_config_path):
            os.remove(cls.test_config_path)
        if os.path.exists('test_app.log'):
            os.remove('test_app.log')

    def setUp(self):
        self.config_manager = ConfigManager(self.test_config_path)
        LoggerSetup(self.config_manager)

    def test_logging_setup(self):
        logger = logging.getLogger()  # Get the root logger
        logger.setLevel(logging.INFO)

        log_file_handler = None
        for handler in logger.handlers:
            if isinstance(handler, logging.FileHandler):
                log_file_handler = handler
                break

        self.assertIsNotNone(log_file_handler, "FileHandler not found in logger.handlers")

        logger.info('This is a test log message')

        # Ensure all handlers flush their buffers
        for handler in logger.handlers:
            handler.flush()

        with open('test_app.log', 'r') as f:
            log_content = f.read()
        self.assertIn('This is a test log message', log_content)

if __name__ == '__main__':
    unittest.main()
