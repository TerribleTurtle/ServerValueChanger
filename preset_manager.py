"""
A module to manage saving and loading presets using JSON files.

Classes:
    PresetManager: A class to handle preset saving and loading operations, including
                   file dialogs for user interaction.

Methods (PresetManager class):
    __init__(self, preset_directory='presets', config_schema_path='config_schema.json'): Initializes the PresetManager with a preset directory and loads the config schema.
    _load_labels_mapping(self): Loads the labels mapping from the config schema file.
    save_preset(self, preset_path, changes): Saves the given changes to the specified preset path in JSON format, including labels.
    load_preset(self, preset_path): Loads and returns the changes from the specified preset path in JSON format.
    save_preset_dialog(self, changes): Opens a dialog to save the preset and saves the given changes.
    load_preset_dialog(self): Opens a dialog to load a preset and returns the loaded changes.
"""

import json
import os
import logging
from tkinter import filedialog, messagebox

class PresetManager:
    """
    Manages saving and loading of presets.
    """
    def __init__(self, preset_directory='presets', config_schema_path='config_schema.json'):
        """
        Initializes the PresetManager with a preset directory and loads the config schema.
        """
        self.preset_directory = os.path.join(os.path.dirname(__file__), preset_directory)
        if not os.path.exists(self.preset_directory):
            os.makedirs(self.preset_directory)

        # Load the configuration schema
        self.config_schema_path = config_schema_path
        self.labels_mapping = self._load_labels_mapping()

    def _load_labels_mapping(self):
        """
        Loads the labels mapping from the config schema file.
        """
        try:
            with open(self.config_schema_path, 'r', encoding='utf-8') as f:
                config_schema = json.load(f)

            labels_mapping = {}
            for tab_data in config_schema.get("tabs", {}).values():
                for group_data in tab_data.get("groups", {}).values():
                    for setting in group_data.get("settings", []):
                        key_path = setting.get("key_path")
                        label = setting.get("label")
                        if key_path and label:
                            labels_mapping[key_path] = label

            return labels_mapping
        except (IOError, json.JSONDecodeError) as e:
            logging.error("Failed to load config schema: %s", str(e))
            return {}

    def save_preset(self, preset_path, changes):
        """
        Saves the given changes to the specified preset path in JSON format, including labels.
        """
        try:
            annotated_changes = {}
            for key_path, value in changes.items():
                label = self.labels_mapping.get(key_path, "Unknown")
                annotated_changes[key_path] = {
                    "label": label,
                    "value": value
                }

            with open(preset_path, 'w', encoding='utf-8') as f:
                json.dump(annotated_changes, f, ensure_ascii=False, indent=4)
            logging.info("Preset '%s' saved successfully.", os.path.basename(preset_path))
        except (IOError, json.JSONDecodeError) as e:
            logging.error("Failed to save preset '%s': %s", os.path.basename(preset_path), str(e))

    def load_preset(self, preset_path):
        """
        Loads and returns the changes from the specified preset path in JSON format.
        """
        try:
            logging.info("Loading preset from path: %s", preset_path)
            with open(preset_path, 'r', encoding='utf-8') as f:
                annotated_changes = json.load(f)

            changes = {key_path: data["value"] for key_path, data in annotated_changes.items()}
            logging.info("Preset '%s' loaded successfully.", os.path.basename(preset_path))
            logging.debug("Preset contents: %s", changes)
            return changes
        except (IOError, json.JSONDecodeError) as e:
            logging.error("Failed to load preset '%s': %s", os.path.basename(preset_path), str(e))
            return None

    def save_preset_dialog(self, changes):
        """
        Opens a dialog to save the preset and saves the given changes.
        """
        try:
            preset_path = filedialog.asksaveasfilename(
                initialdir=self.preset_directory,
                title="Save Preset",
                filetypes=(("JSON files", "*.json"), ("All files", "*.*"))
            )
            if not preset_path:
                return

            if not preset_path.lower().endswith(".json"):
                preset_path += ".json"

            logging.debug("Saving preset with changes: %s", changes)
            self.save_preset(preset_path, changes)
            messagebox.showinfo("Info", "Preset saved successfully.")
        except (IOError, json.JSONDecodeError) as e:
            logging.error("Error saving preset: %s", str(e))
            messagebox.showerror("Error", f"Failed to save preset: {str(e)}")

    def load_preset_dialog(self):
        """
        Opens a dialog to load a preset and returns the loaded changes.
        """
        try:
            preset_path = filedialog.askopenfilename(
                initialdir=self.preset_directory,
                title="Load Preset",
                filetypes=(("JSON files", "*.json"), ("All files", "*.*"))
            )
            if not preset_path:
                return None

            logging.info("Selected preset path: %s", preset_path)
            return self.load_preset(preset_path)
        except (IOError, json.JSONDecodeError) as e:
            logging.error("Error loading preset: %s", str(e))
            messagebox.showerror("Error", f"Failed to load preset: {str(e)}")
            return None
