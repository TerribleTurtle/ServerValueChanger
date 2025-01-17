import unittest
import os
import json
import shutil
import tkinter as tk
from batch_apply import BatchApply
from config_manager import ConfigManager

class TestBatchApply(unittest.TestCase):
    """Test cases for the BatchApply class."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        cls.test_config_path = 'test_config.json'
        with open(cls.test_config_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps({
                "paths": {
                    "server_database": "database",
                    "server_config": "configs"
                },
                "logging": {
                    "level": "INFO",
                    "file": "test_app.log"
                },
                "backup": {
                    "directory": "backup"
                }
            }))

        cls.test_schema_path = 'test_schema.json'
        with open(cls.test_schema_path, 'w', encoding='utf-8') as f:
            f.write('{}')

        os.makedirs('database', exist_ok=True)
        os.makedirs('configs', exist_ok=True)

        cls.test_file_path = 'database/test_file.json'
        with open(cls.test_file_path, 'w', encoding='utf-8') as f:
            json.dump({'key1': {'subkey1': 'value1'}, 'key2': {'subkey2': 'value2'}}, f)

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment."""
        if os.path.exists(cls.test_config_path):
            os.remove(cls.test_config_path)
        if os.path.exists(cls.test_schema_path):
            os.remove(cls.test_schema_path)
        if os.path.exists(cls.test_file_path):
            os.remove(cls.test_file_path)
        if os.path.exists('database'):
            shutil.rmtree('database')
        if os.path.exists('configs'):
            shutil.rmtree('configs')

    def setUp(self):
        """Set up for each test."""
        self.config_manager = ConfigManager(self.test_config_path, self.test_schema_path)
        self.batch_apply = BatchApply(self.config_manager)
        self.test_backup_dir = 'backup'

    def tearDown(self):
        """Clean up after each test."""
        if os.path.exists(self.test_backup_dir):
            shutil.rmtree(self.test_backup_dir)

    def test_apply_changes(self):
        """Test applying changes."""
        settings = {'key1.subkey1': tk.Entry()}
        settings['key1.subkey1'].insert(0, 'new_value1')
        schema = {
            'tabs': {
                'Tab1': {
                    'groups': {
                        'Group1': {
                            'column': 1,
                            'settings': [
                                {
                                    'label': 'Label1',
                                    'file': 'database/test_file.json',
                                    'key_path': 'key1.subkey1',
                                    'type': 'string',
                                    'default': 'value1',
                                    'complex': False
                                }
                            ]
                        }
                    }
                }
            }
        }

        self.batch_apply.apply_changes(settings, schema)

        with open(self.test_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.assertEqual(data['key1']['subkey1'], 'new_value1')

if __name__ == '__main__':
    unittest.main()
