import unittest
import os
import json
import shutil
from batch_apply import BatchApply
from change_tracker import ChangeTracker

class TestBatchApply(unittest.TestCase):
    def setUp(self):
        self.test_simple_file_path = 'test_simple_file.json'
        self.test_complex_file_path = 'test_complex_file.json'
        self.backup_dir = 'test_backup'
        self.tracker = ChangeTracker()
        self.batch_apply = BatchApply(self.tracker, self.backup_dir)

        # Create a test JSON file for simple change
        with open(self.test_simple_file_path, 'w') as f:
            json.dump({'key1': {'subkey1': 'old_value1'}, 'key2': {'subkey2': 'old_value2'}}, f)

        # Create a test JSON file for complex change
        with open(self.test_complex_file_path, 'w') as f:
            json.dump({
                'item1': {'_parent': '5485a8684bdc2da71d8b4567', '_props': {'StackMaxSize': 10}},
                'item2': {'_parent': '5485a8684bdc2da71d8b4567', '_props': {'StackMaxSize': 20}},
                'item3': {'_parent': 'some_other_parent', '_props': {'StackMaxSize': 30}}
            }, f)

    def tearDown(self):
        # Remove test files and directories after tests
        if os.path.exists(self.test_simple_file_path):
            os.remove(self.test_simple_file_path)
        if os.path.exists(self.test_complex_file_path):
            os.remove(self.test_complex_file_path)
        if os.path.exists(self.backup_dir):
            shutil.rmtree(self.backup_dir)

    def test_apply_simple_changes(self):
        self.tracker.track_change(self.test_simple_file_path, 'key1.subkey1', 'old_value1', 'new_value1')
        self.batch_apply.apply_changes()

        with open(self.test_simple_file_path, 'r') as f:
            data = json.load(f)

        self.assertEqual(data['key1']['subkey1'], 'new_value1')

    def test_create_backup(self):
        self.tracker.track_change(self.test_simple_file_path, 'key1.subkey1', 'old_value1', 'new_value1')
        self.batch_apply.apply_changes()

        backup_file_path = os.path.join(self.backup_dir, os.path.basename(self.test_simple_file_path))
        self.assertTrue(os.path.exists(backup_file_path))

    def test_apply_complex_changes(self):
        criteria = {'_parent': '5485a8684bdc2da71d8b4567'}
        updates = {'_props.StackMaxSize': 100}
        self.tracker.track_complex_change(self.test_complex_file_path, criteria, updates)
        self.batch_apply.apply_changes()

        with open(self.test_complex_file_path, 'r') as f:
            data = json.load(f)

        self.assertEqual(data['item1']['_props']['StackMaxSize'], 100)
        self.assertEqual(data['item2']['_props']['StackMaxSize'], 100)
        self.assertEqual(data['item3']['_props']['StackMaxSize'], 30)  # Should remain unchanged

if __name__ == '__main__':
    unittest.main()
