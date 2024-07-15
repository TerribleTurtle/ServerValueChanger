# ui_updater.py
import logging
import tkinter as tk

class UIUpdater:
    def __init__(self, config_manager):
        self.config_manager = config_manager

    def initialize_with_defaults(self, settings):
        schema = self.config_manager.get_schema()
        for tab_name, tab_data in schema['tabs'].items():
            for group_name, group_data in tab_data['groups'].items():
                for setting in group_data['settings']:
                    default_value = setting.get('default', None)
                    key_path = setting['key_path']
                    logging.debug(f"Setting default for {key_path} to {default_value}")
                    if key_path in settings:
                        if isinstance(settings[key_path], tk.Entry):
                            settings[key_path].delete(0, 'end')
                            settings[key_path].insert(0, str(default_value))  # Ensure the value is a string
                        elif isinstance(settings[key_path], tk.BooleanVar):
                            settings[key_path].set(default_value)

    def capture_ui_state(self, settings):
        changes = {}
        for key_path, widget in settings.items():
            if isinstance(widget, tk.Entry):
                changes[key_path] = widget.get()
            elif isinstance(widget, tk.BooleanVar):
                changes[key_path] = widget.get()
        return changes

    def update_ui_with_preset(self, settings, changes):
        for key_path, new_value in changes.items():
            if key_path in settings:
                if isinstance(settings[key_path], tk.Entry):
                    settings[key_path].delete(0, 'end')
                    settings[key_path].insert(0, str(new_value))  # Ensure the value is a string
                elif isinstance(settings[key_path], tk.BooleanVar):
                    settings[key_path].set(new_value)
