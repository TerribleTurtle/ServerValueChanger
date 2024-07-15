import unittest
from change_tracker import ChangeTracker

class TestChangeTracker(unittest.TestCase):
    def setUp(self):
        self.tracker = ChangeTracker()

    def test_track_change(self):
        self.tracker.track_change('path/to/file.json', 'key1.subkey1', 'old_value1', 'new_value1')
        changes = self.tracker.get_changes()
        self.assertIn('path/to/file.json', changes)
        self.assertEqual(changes['path/to/file.json'][0]['key_path'], 'key1.subkey1')
        self.assertEqual(changes['path/to/file.json'][0]['old_value'], 'old_value1')
        self.assertEqual(changes['path/to/file.json'][0]['new_value'], 'new_value1')

    def test_track_complex_change(self):
        criteria = {'_parent': '5485a8684bdc2da71d8b4567'}
        updates = {'_props.StackMaxSize': 100}
        self.tracker.track_complex_change('path/to/file.json', criteria, updates)
        changes = self.tracker.get_changes()
        self.assertIn('path/to/file.json', changes)
        self.assertEqual(changes['path/to/file.json'][0]['criteria'], criteria)
        self.assertEqual(changes['path/to/file.json'][0]['updates'], updates)

    def test_clear_changes(self):
        self.tracker.track_change('path/to/file.json', 'key1.subkey1', 'old_value1', 'new_value1')
        self.tracker.clear_changes()
        changes = self.tracker.get_changes()
        self.assertEqual(len(changes), 0)

if __name__ == '__main__':
    unittest.main()
