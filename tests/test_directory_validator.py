import unittest
import os
from directory_validator import DirectoryValidator

class TestDirectoryValidator(unittest.TestCase):
    def setUp(self):
        # Create temporary directories for testing
        self.existing_path = 'test_existing_directory'
        self.missing_path = 'test_missing_directory'
        
        os.makedirs(self.existing_path, exist_ok=True)

    def tearDown(self):
        # Remove temporary directories after tests
        if os.path.exists(self.existing_path):
            os.rmdir(self.existing_path)

    def test_validate_existing_paths(self):
        validator = DirectoryValidator([self.existing_path])
        try:
            validator.validate()
        except FileNotFoundError:
            self.fail("validate() raised FileNotFoundError unexpectedly!")

    def test_validate_missing_paths(self):
        validator = DirectoryValidator([self.missing_path])
        with self.assertRaises(FileNotFoundError):
            validator.validate()

if __name__ == '__main__':
    unittest.main()