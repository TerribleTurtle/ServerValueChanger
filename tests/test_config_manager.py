import unittest
import os
from config_manager import ConfigManager

class TestConfigManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a temporary config file for testing
        cls.test_config_path = 'test_config.json'
        with open(cls.test_config_path, 'w') as f:
            f.write('''
            {
              "paths": {
                "server_database": "S:/server config test/SPT_Data/Server/database",
                "server_config": "S:/server config test/SPT_Data/Server/configs"
              },
              "logging": {
                "level": "INFO",
                "file": "app.log"
              },
              "backup": {
                "directory": "backup"
              }
            }
            ''')

    @classmethod
    def tearDownClass(cls):
        # Remove the temporary config file after tests
        os.remove(cls.test_config_path)

    def setUp(self):
        self.config_manager = ConfigManager(self.test_config_path)

    def test_get_existing_setting(self):
        self.assertEqual(self.config_manager.get_setting('logging.level'), 'INFO')

    def test_get_non_existing_setting(self):
        with self.assertRaises(KeyError):
            self.config_manager.get_setting('non.existing.setting')

if __name__ == '__main__':
    unittest.main()
