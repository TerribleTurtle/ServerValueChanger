# complex_config_handler.py
import json
import os
import logging
import tkinter as tk

class ComplexConfigHandler:
    def __init__(self, config_manager):
        self.config_manager = config_manager

    def update_ammo_stack_size(self, settings, schema):
        file_changes = {}

        for setting in schema['settings']:
            if setting.get('complex', False) and setting['key_path'] == '_props.StackMaxSize':
                key_path = setting['key_path']
                file_path = setting['file']
                if key_path in settings:
                    widget = settings[key_path]
                    value = widget.get() if isinstance(widget, tk.Entry) else widget.get()

                    try:
                        resolved_file_path = self.resolve_full_path(file_path)
                        logging.debug(f"Applying complex changes to {resolved_file_path}")

                        # Load current content of the JSON file
                        with open(resolved_file_path, 'r', encoding='utf-8') as file:
                            data = json.load(file)

                        # Apply the specific complex change
                        for item_id, item_data in data.items():
                            if item_data.get('_parent') == '5485a8684bdc2da71d8b4567':
                                item_data['_props']['StackMaxSize'] = int(value)
                                logging.debug(f"Updated StackMaxSize for item {item_id} to {value}")

                        # Collect changes to pass to BatchApply
                        file_changes[file_path] = data

                    except FileNotFoundError as e:
                        logging.error(f"Error applying complex changes: {e}")
                    except ValueError as e:
                        logging.error(f"Error resolving file path: {e}")

        return file_changes

    def resolve_full_path(self, file_path):
        file_base = file_path.split('/', 1)[0]
        if file_base == 'database':
            base_path = self.config_manager.get_setting('paths.server_database')
        elif file_base == 'configs':
            base_path = self.config_manager.get_setting('paths.server_config')
        else:
            raise ValueError(f"Unknown base directory for file path: {file_path}")

        return os.path.join(base_path, file_path.split('/', 1)[1])
