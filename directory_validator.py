# directory_validator.py
import os
import logging

class DirectoryValidator:
    def __init__(self, paths):
        self.paths = paths

    def validate(self):
        missing_paths = []
        for path in self.paths:
            if not os.path.exists(path):
                missing_paths.append(path)
        
        if missing_paths:
            logging.error(f"Missing required paths: {missing_paths}")
            raise FileNotFoundError(f"Missing required paths: {missing_paths}")
        else:
            logging.info("All required paths are present.")

# Example usage
if __name__ == "__main__":
    from config_manager import ConfigManager  # Ensure logger is configured
    config_manager = ConfigManager('config.json', 'config_schema.json')
    paths_to_validate = [
        config_manager.get_setting('paths.server_database'),
        config_manager.get_setting('paths.server_config')
    ]

    validator = DirectoryValidator(paths_to_validate)
    try:
        validator.validate()
        print("Directory structure is valid.")
    except FileNotFoundError as e:
        print(e)
