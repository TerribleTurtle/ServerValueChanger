import unittest
import os
import json
from preset_manager import PresetManager

class TestPresetManager(unittest.TestCase):
    """Test cases for the PresetManager class."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        cls.preset_directory = 'test_presets'
        if not os.path.exists(cls.preset_directory):
            os.makedirs(cls.preset_directory)

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment."""
        if os.path.exists(cls.preset_directory):
            for file in os.listdir(cls.preset_directory):
                os.remove(os.path.join(cls.preset_directory, file))
            os.rmdir(cls.preset_directory)

    def setUp(self):
        """Set up for each test."""
        self.preset_manager = PresetManager(self.preset_directory)

    def test_save_preset(self):
        """Test saving a preset."""
        preset_path = os.path.join(self.preset_directory, 'test_preset.json')
        changes = {'key1': 'value1', 'key2': 'value2'}
        self.preset_manager.save_preset(preset_path, changes)

        with open(preset_path, 'r', encoding='utf-8') as f:
            loaded_changes = json.load(f)
        self.assertEqual(changes, loaded_changes)

    def test_load_preset(self):
        """Test loading a preset."""
        preset_path = os.path.join(self.preset_directory, 'test_preset.json')
        changes = {'key1': 'value1', 'key2': 'value2'}
        with open(preset_path, 'w', encoding='utf-8') as f:
            json.dump(changes, f)

        loaded_changes = self.preset_manager.load_preset(preset_path)
        self.assertEqual(changes, loaded_changes)

if __name__ == '__main__':
    unittest.main()
