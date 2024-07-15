"""
Main module to initialize the configuration manager, set up logging, validate directories,
and launch the GUI application.

Functions:
    main(): Main function to set up and launch the application.
"""

from config_manager import ConfigManager
from logger_setup import LoggerSetup
from directory_validator import DirectoryValidator
from gui import Application

def main():
    """
    Main function to set up and launch the application.
    """
    # Initialize the configuration manager
    config_manager = ConfigManager('config.json', 'config_schema.json')

    # Set up logging
    LoggerSetup(config_manager)

    # Validate required directories
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
        return

    # Initialize and launch the GUI
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    main()
