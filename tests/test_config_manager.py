import unittest
import os
from config_manager import ConfigManager

class TestConfigManager(unittest.TestCase):
    """Test cases for the ConfigManager class."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        # Create a temporary config file for testing
        cls.test_config_path = 'test_config.json'
        with open(cls.test_config_path, 'w', encoding='utf-8') as f:
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

        # Create a temporary schema file for testing
        cls.test_schema_path = 'test_schema.json'
        with open(cls.test_schema_path, 'w', encoding='utf-8') as f:
            f.write('{}')

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment."""
        # Remove the temporary config and schema files after tests
        if os.path.exists(cls.test_config_path):
            os.remove(cls.test_config_path)
        if os.path.exists(cls.test_schema_path):
            os.remove(cls.test_schema_path)

    def setUp(self):
        """Set up for each test."""
        self.config_manager = ConfigManager(self.test_config_path, self.test_schema_path)

    def test_get_existing_setting(self):
        """Test retrieving an existing setting."""
        self.assertEqual(self.config_manager.get_setting('logging.level'), 'INFO')

    def test_get_non_existing_setting(self):
        """Test retrieving a non-existing setting."""
        with self.assertRaises(KeyError):
            self.config_manager.get_setting('non.existing.setting')

if __name__ == '__main__':
    unittest.main()
