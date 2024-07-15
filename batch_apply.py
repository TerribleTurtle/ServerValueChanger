# batch_apply.py
import json
import os
import logging
import tkinter as tk
from tkinter import messagebox
from complex_config_handler import ComplexConfigHandler

class BatchApply:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.complex_handler = ComplexConfigHandler(config_manager)

    def resolve_full_path(self, file_path):
        file_base = file_path.split('/', 1)[0]
        if file_base == 'database':
            base_path = self.config_manager.get_setting('paths.server_database')
        elif file_base == 'configs':
            base_path = self.config_manager.get_setting('paths.server_config')
        else:
            raise ValueError(f"Unknown base directory for file path: {file_path}")

        return os.path.join(base_path, file_path.split('/', 1)[1])

    def apply_changes(self, settings, schema):
        # Handle complex configurations first
        complex_changes = self.complex_handler.update_ammo_stack_size(settings, schema)

        # Apply complex changes using BatchApply
        for relative_path, data in complex_changes.items():
            try:
                file_path = self.resolve_full_path(relative_path)
                logging.debug(f"Applying complex changes to {file_path}")

                # Write modified content back to the JSON file
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)

                logging.info(f"Complex changes applied for {file_path}")
            except FileNotFoundError as e:
                logging.error(f"Error applying complex changes: {e}")
            except ValueError as e:
                logging.error(f"Error resolving file path: {e}")

        # Handle simple configurations
        file_changes = self.organize_changes_by_file(settings, schema)

        for relative_path, changes in file_changes.items():
            try:
                file_path = self.resolve_full_path(relative_path)
                logging.debug(f"Applying changes to {file_path}")

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
                    logging.debug(f"Applied change for {file_path} - {change['key_path']}: {change['value']}")

                # Write modified content back to the JSON file
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)

                logging.info(f"Changes applied for {file_path}")
            except FileNotFoundError as e:
                logging.error(f"Error applying changes: {e}")
            except ValueError as e:
                logging.error(f"Error resolving file path: {e}")

    def organize_changes_by_file(self, settings, schema):
        file_changes = {}
        for setting in schema['settings']:
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

class AppLogic:
    def __init__(self, batch_apply, ui_updater, config_manager):
        self.batch_apply = batch_apply
        self.ui_updater = ui_updater
        self.config_manager = config_manager

    def apply_changes(self, settings):
        try:
            schema = self.config_manager.get_schema()
            self.batch_apply.apply_changes(settings, schema)
            messagebox.showinfo("Info", "Changes have been applied successfully.")
        except Exception as e:
            logging.error(f"Error applying changes: {str(e)}")
            messagebox.showerror("Error", str(e))
            raise
