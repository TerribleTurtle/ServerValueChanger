"""
This module provides the UIUpdater class to handle updating and capturing the state of a Tkinter UI
based on a given configuration.

Classes:
    UIUpdater: Handles updating and capturing the state of a Tkinter UI based on a given configuration.

Methods (UIUpdater class):
    __init__(self, config_manager): Initialize the UIUpdater with a configuration manager.
    initialize_with_defaults(self, settings): Initialize the UI with default settings from the configuration schema.
    capture_ui_state(self, settings): Capture the current state of the UI.
    update_ui_with_preset(self, settings, changes): Update the UI with a given preset of changes.
"""

import logging
import tkinter as tk

class UIUpdater:
    """
    Class to handle updating and capturing the state of a Tkinter UI based on a given configuration.
    """
    def __init__(self, config_manager):
        """
        Initialize the UIUpdater with a configuration manager.

        :param config_manager: The configuration manager to use for schema retrieval.
        """
        self.config_manager = config_manager

    def initialize_with_defaults(self, settings):
        """
        Initialize the UI with default settings from the configuration schema.

        :param settings: A dictionary of Tkinter widgets keyed by their setting paths.
        """
        schema = self.config_manager.get_schema()
        for tab_data in schema['tabs'].values():
            for group_data in tab_data['groups'].values():
                for setting in group_data['settings']:
                    default_value = setting.get('default', None)
                    key_path = setting['key_path']
                    logging.debug("Setting default for %s to %s", key_path, default_value)
                    if key_path in settings:
                        if isinstance(settings[key_path], tk.Entry):
                            settings[key_path].delete(0, 'end')
                            settings[key_path].insert(0, str(default_value))  # Ensure the value is a string
                        elif isinstance(settings[key_path], tk.BooleanVar):
                            settings[key_path].set(default_value)

    def capture_ui_state(self, settings):
        """
        Capture the current state of the UI.

        :param settings: A dictionary of Tkinter widgets keyed by their setting paths.
        :return: A dictionary representing the captured state.
        """
        changes = {}
        for key_path, widget in settings.items():
            if isinstance(widget, tk.Entry):
                changes[key_path] = widget.get()
            elif isinstance(widget, tk.BooleanVar):
                changes[key_path] = widget.get()
        return changes

    def update_ui_with_preset(self, settings, changes):
        """
        Update the UI with a given preset of changes.

        :param settings: A dictionary of Tkinter widgets keyed by their setting paths.
        :param changes: A dictionary of changes to apply to the UI.
        """
        for key_path, new_value in changes.items():
            if key_path in settings:
                if isinstance(settings[key_path], tk.Entry):
                    settings[key_path].delete(0, 'end')
                    settings[key_path].insert(0, str(new_value))  # Ensure the value is a string
                elif isinstance(settings[key_path], tk.BooleanVar):
                    settings[key_path].set(new_value)
