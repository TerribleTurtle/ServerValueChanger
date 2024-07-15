import unittest
import os
import json
import shutil  # Import shutil for file and directory operations
import tkinter as tk
from complex_config_handler import ComplexConfigHandler
from config_manager import ConfigManager

class TestComplexConfigHandler(unittest.TestCase):
    """Test cases for the ComplexConfigHandler class."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        cls.test_config_path = 'test_config.json'
        with open(cls.test_config_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps({
                "paths": {
                    "server_database": "database",
                    "server_config": "configs"
                }
            }))

        cls.test_schema_path = 'test_schema.json'
        with open(cls.test_schema_path, 'w', encoding='utf-8') as f:
            f.write('{}')

        os.makedirs('database', exist_ok=True)
        os.makedirs('configs', exist_ok=True)

        cls.test_file_path = 'database/test_items.json'
        with open(cls.test_file_path, 'w', encoding='utf-8') as f:
            json.dump({
                'item1': {'_parent': '5485a8684bdc2da71d8b4567', '_props': {'StackMaxSize': 10}},
                'item2': {'_parent': '5485a8684bdc2da71d8b4567', '_props': {'StackMaxSize': 20}},
                'item3': {'_parent': 'some_other_parent', '_props': {'StackMaxSize': 30}}
            }, f)

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
        self.handler = ComplexConfigHandler(self.config_manager)

    def test_update_ammo_stack_size(self):
        """Test updating the ammo stack size."""
        settings = {'_props.StackMaxSize': tk.Entry()}
        settings['_props.StackMaxSize'].insert(0, '50')
        schema = {
            'tabs': {
                'Tab1': {
                    'groups': {
                        'Group1': {
                            'column': 1,
                            'settings': [
                                {
                                    'label': 'Ammo Stack Size',
                                    'file': 'database/test_items.json',
                                    'key_path': '_props.StackMaxSize',
                                    'type': 'integer',
                                    'default': 10,
                                    'complex': True
                                }
                            ]
                        }
                    }
                }
            }
        }

        self.handler.update_ammo_stack_size(settings, schema)

        with open(self.test_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.assertEqual(data['item1']['_props']['StackMaxSize'], 50)
        self.assertEqual(data['item2']['_props']['StackMaxSize'], 50)
        self.assertEqual(data['item3']['_props']['StackMaxSize'], 30)

if __name__ == '__main__':
    unittest.main()
