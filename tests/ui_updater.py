import unittest
import tkinter as tk
from ui_updater import UIUpdater
from config_manager import ConfigManager
import os
import json

class TestUIUpdater(unittest.TestCase):
    """Test cases for the UIUpdater class."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        cls.test_config_path = 'test_config.json'
        with open(cls.test_config_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps({
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
            }))

        cls.test_schema_path = 'test_schema.json'
        with open(cls.test_schema_path, 'w', encoding='utf-8') as f:
            f.write('{}')

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment."""
        if os.path.exists(cls.test_config_path):
            os.remove(cls.test_config_path)
        if os.path.exists(cls.test_schema_path):
            os.remove(cls.test_schema_path)

    def setUp(self):
        """Set up for each test."""
        self.config_manager = ConfigManager(self.test_config_path, self.test_schema_path)
        self.ui_updater = UIUpdater(self.config_manager)
        self.settings = {
            'key1': tk.Entry(),
            'key2': tk.BooleanVar()
        }

    def test_initialize_with_defaults(self):
        """Test initializing the UI with default settings."""
        schema = {
            'tabs': {
                'Tab1': {
                    'groups': {
                        'Group1': {
                            'column': 1,
                            'settings': [
                                {
                                    'label': 'Label1',
                                    'file': 'test_file.json',
                                    'key_path': 'key1',
                                    'type': 'string',
                                    'default': 'default_value',
                                    'complex': False
                                },
                                {
                                    'label': 'Label2',
                                    'file': 'test_file.json',
                                    'key_path': 'key2',
                                    'type': 'boolean',
                                    'default': True,
                                    'complex': False
                                }
                            ]
                        }
                    }
                }
            }
        }
        self.config_manager.schema = schema

        self.ui_updater.initialize_with_defaults(self.settings)
        self.assertEqual(self.settings['key1'].get(), 'default_value')
        self.assertTrue(self.settings['key2'].get())

    def test_capture_ui_state(self):
        """Test capturing the current state of the UI."""
        self.settings['key1'].insert(0, 'current_value')
        self.settings['key2'].set(False)

        state = self.ui_updater.capture_ui_state(self.settings)
        self.assertEqual(state['key1'], 'current_value')
        self.assertFalse(state['key2'])

    def test_update_ui_with_preset(self):
        """Test updating the UI with a given preset."""
        changes = {
            'key1': 'preset_value',
            'key2': True
        }

        self.ui_updater.update_ui_with_preset(self.settings, changes)
        self.assertEqual(self.settings['key1'].get(), 'preset_value')
        self.assertTrue(self.settings['key2'].get())

if __name__ == '__main__':
    unittest.main()
