"""
Module for handling complex configuration updates for StackMaxSize in JSON files.

Classes:
    ComplexConfigHandler: Handles complex configuration updates for StackMaxSize in JSON files.

Methods:
    __init__(self, config_manager): Initializes the ComplexConfigHandler with a given configuration manager.
    update_ammo_stack_size(self, settings, schema): Updates the StackMaxSize for items in JSON configuration files.
    resolve_full_path(self, file_path): Resolves the full path of a given file path based on the base directory.
"""

import json
import os
import logging
import tkinter as tk

class ComplexConfigHandler:
    """
    Handles complex configuration updates for StackMaxSize in JSON files.
    """

    def __init__(self, config_manager):
        """
        Initializes the ComplexConfigHandler with a given configuration manager.

        Args:
            config_manager: An instance managing configuration settings.
        """
        self.config_manager = config_manager

    def update_ammo_stack_size(self, settings, schema):
        """
        Updates the StackMaxSize for items in JSON configuration files based on given settings.

        Args:
            settings: A dictionary containing the settings from the UI.
            schema: A dictionary representing the schema of the configuration.

        Returns:
            A dictionary with file paths as keys and updated content as values.
        """
        file_changes = {}

        for tab_data in schema['tabs'].values():
            for group_data in tab_data['groups'].values():
                for setting in group_data['settings']:
                    if setting.get('complex', False) and setting['key_path'] == '_props.StackMaxSize':
                        key_path = setting['key_path']
                        file_path = setting['file']
                        if key_path in settings:
                            widget = settings[key_path]
                            value = widget.get() if isinstance(widget, tk.Entry) else widget.get()

                            try:
                                resolved_file_path = self.resolve_full_path(file_path)
                                logging.debug("Applying complex changes to %s", resolved_file_path)

                                # Load current content of the JSON file
                                with open(resolved_file_path, 'r', encoding='utf-8') as file:
                                    data = json.load(file)

                                # Apply the specific complex change
                                for item_id, item_data in data.items():
                                    if item_data.get('_parent') == '5485a8684bdc2da71d8b4567':
                                        item_data['_props']['StackMaxSize'] = int(value)
                                        logging.debug(
                                            "Updated StackMaxSize for item %s to %s", item_id, value
                                        )

                                # Collect changes to pass to BatchApply
                                file_changes[file_path] = data

                                # Write modified content back to the JSON file
                                with open(resolved_file_path, 'w', encoding='utf-8') as file:
                                    json.dump(data, file, ensure_ascii=False, indent=4)

                            except FileNotFoundError as e:
                                logging.error("Error applying complex changes: %s", e)
                            except ValueError as e:
                                logging.error("Error resolving file path: %s", e)

        return file_changes

    def resolve_full_path(self, file_path):
        """
        Resolves the full path of a given file path based on the base directory.

        Args:
            file_path: A string representing the relative file path.

        Returns:
            A string representing the full file path.

        Raises:
            ValueError: If the base directory is unknown.
        """
        file_base = file_path.split('/', 1)[0]
        if file_base == 'database':
            base_path = self.config_manager.get_setting('paths.server_database')
        elif file_base == 'configs':
            base_path = self.config_manager.get_setting('paths.server_config')
        else:
            raise ValueError(f"Unknown base directory for file path: {file_path}")

        return os.path.join(base_path, file_path.split('/', 1)[1])
