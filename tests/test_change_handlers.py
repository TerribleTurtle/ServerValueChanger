import unittest
from change_handlers import apply_simple_change, apply_complex_change

class TestChangeHandlers(unittest.TestCase):
    def test_apply_simple_change(self):
        data = {'key1': {'subkey1': 'old_value1'}}
        change = {'key_path': 'key1.subkey1', 'new_value': 'new_value1'}
        updated_data = apply_simple_change(data, change)
        self.assertEqual(updated_data['key1']['subkey1'], 'new_value1')

    def test_apply_complex_change(self):
        data = {
            'item1': {'_parent': '5485a8684bdc2da71d8b4567', '_props': {'StackMaxSize': 10}},
            'item2': {'_parent': '5485a8684bdc2da71d8b4567', '_props': {'StackMaxSize': 20}},
            'item3': {'_parent': 'some_other_parent', '_props': {'StackMaxSize': 30}}
        }
        change = {
            'criteria': {'_parent': '5485a8684bdc2da71d8b4567'},
            'updates': {'_props.StackMaxSize': 100}
        }
        updated_data = apply_complex_change(data, change)
        self.assertEqual(updated_data['item1']['_props']['StackMaxSize'], 100)
        self.assertEqual(updated_data['item2']['_props']['StackMaxSize'], 100)
        self.assertEqual(updated_data['item3']['_props']['StackMaxSize'], 30)  # Should remain unchanged

if __name__ == '__main__':
    unittest.main()
