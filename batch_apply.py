"""
BatchApply module for applying configuration settings to JSON files.

This module contains the BatchApply class, which handles the batch application of configuration
settings to JSON files. It includes methods for resolving file paths, applying changes, and
handling complex settings.

Classes:
    BatchApply: Handles the batch application of configuration settings to JSON files.

Methods (BatchApply class):
    __init__(self, config_manager): Initializes BatchApply with a configuration manager.
    resolve_full_path(self, file_path): Resolves the full file path based on the base directory.
    apply_changes(self, settings, schema): Apply changes to configuration files based on settings and schema.
    handle_complex_settings(self, settings, schema): Handle specific complex settings like Ammo Stack Size.
    organize_changes_by_file(self, settings, schema): Organize changes by file based on settings and schema.
"""

import json
import os
import logging
import tkinter as tk
from complex_config_handler import ComplexConfigHandler

class BatchApply:
    """
    Class to handle the batch application of configuration settings.
    """

    def __init__(self, config_manager):
        """
        Initialize BatchApply with a configuration manager.

        :param config_manager: The configuration manager instance.
        """
        self.config_manager = config_manager
        self.complex_handler = ComplexConfigHandler(config_manager)

    def resolve_full_path(self, file_path):
        """
        Resolve the full file path based on the base directory.

        :param file_path: The relative file path.
        :return: The full file path.
        :raises ValueError: If the base directory is unknown.
        """
        file_base = file_path.split('/', 1)[0]
        if file_base == 'database':
            base_path = self.config_manager.get_setting('paths.server_database')
        elif file_base == 'configs':
            base_path = self.config_manager.get_setting('paths.server_config')
        else:
            raise ValueError(f"Unknown base directory for file path: {file_path}")

        return os.path.join(base_path, file_path.split('/', 1)[1])

    def apply_changes(self, settings, schema):
        """
        Apply changes to configuration files based on settings and schema.

        :param settings: The settings to apply.
        :param schema: The schema defining the structure of the settings.
        :raises Exception: If an error occurs during the application of changes.
        """
        try:
            # Handle complex configurations specifically
            self.handle_complex_settings(settings, schema)

            # Handle simple configurations
            file_changes = self.organize_changes_by_file(settings, schema)

            for relative_path, changes in file_changes.items():
                try:
                    file_path = self.resolve_full_path(relative_path)
                    logging.debug("Applying changes to %s", file_path)

                    # Load current content of the JSON file
                    with open(file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)

                    # Apply changes
                    for change in changes:
                        keys = change['key_path'].split('.')
                        d = data
                        for key in keys[:-1]:
                            if key not in d:
                                d[key] = {}
                            d = d[key]
                        d[keys[-1]] = change['value']
                        logging.debug(
                            "Applied change for %s - %s: %s",
                            file_path, change['key_path'], change['value']
                        )

                    # Write modified content back to the JSON file
                    with open(file_path, 'w', encoding='utf-8') as file:
                        json.dump(data, file, ensure_ascii=False, indent=4)

                    logging.info("Changes applied for %s", file_path)

                except FileNotFoundError:
                    logging.error("File not found: %s", file_path)
                    raise  # Re-raise the exception to stop the process
                except json.JSONDecodeError:
                    logging.error("Error decoding JSON from file: %s", file_path)
                    raise  # Re-raise the exception to stop the process
                except Exception as e:
                    logging.error("Unexpected error applying changes to %s: %s", relative_path, e)
                    raise  # Re-raise the exception to stop the process

        except Exception as e:
            logging.error("Error applying changes: %s", e)
            raise  # Re-raise the exception to be handled by the caller

    def handle_complex_settings(self, settings, schema):
        """
        Handle specific complex settings like Ammo Stack Size.

        :param settings: The settings to handle.
        :param schema: The schema defining the structure of the settings.
        """
        self.complex_handler.update_ammo_stack_size(settings, schema)

    def organize_changes_by_file(self, settings, schema):
        """
        Organize changes by file based on settings and schema.

        :param settings: The settings to apply.
        :param schema: The schema defining the structure of the settings.
        :return: A dictionary of file changes.
        """
        file_changes = {}
        for tab_data in schema['tabs'].values():
            for group_data in tab_data['groups'].values():
                for setting in group_data['settings']:
                    if not setting.get('complex', False):  # Skip complex settings
                        key_path = setting['key_path']
                        file_path = setting['file']
                        if key_path in settings:
                            if file_path not in file_changes:
                                file_changes[file_path] = []
                            widget = settings[key_path]
                            value = widget.get() if isinstance(widget, tk.Entry) else widget.get()
                            file_changes[file_path].append({
                                'key_path': key_path,
                                'value': value
                            })
        return file_changes
