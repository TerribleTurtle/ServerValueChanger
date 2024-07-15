# preset_manager.py
import json
import os
import logging
from tkinter import filedialog, messagebox

class PresetManager:
    def __init__(self, preset_directory='presets'):
        self.preset_directory = os.path.join(os.path.dirname(__file__), preset_directory)
        if not os.path.exists(self.preset_directory):
            os.makedirs(self.preset_directory)

    def save_preset(self, preset_path, changes):
        try:
            with open(preset_path, 'w', encoding='utf-8') as f:
                json.dump(changes, f, ensure_ascii=False, indent=4)
            logging.info(f"Preset '{os.path.basename(preset_path)}' saved successfully.")
        except Exception as e:
            logging.error(f"Failed to save preset '{os.path.basename(preset_path)}': {str(e)}")

    def load_preset(self, preset_path):
        try:
            logging.info(f"Loading preset from path: {preset_path}")
            with open(preset_path, 'r', encoding='utf-8') as f:
                changes = json.load(f)
            logging.info(f"Preset '{os.path.basename(preset_path)}' loaded successfully.")
            logging.debug(f"Preset contents: {changes}")
            return changes
        except Exception as e:
            logging.error(f"Failed to load preset '{os.path.basename(preset_path)}': {str(e)}")
            return None

    def save_preset_dialog(self, changes):
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

            logging.debug(f"Saving preset with changes: {changes}")
            self.save_preset(preset_path, changes)
            messagebox.showinfo("Info", "Preset saved successfully.")
        except Exception as e:
            logging.error(f"Error saving preset: {str(e)}")
            messagebox.showerror("Error", f"Failed to save preset: {str(e)}")

    def load_preset_dialog(self):
        try:
            preset_path = filedialog.askopenfilename(
                initialdir=self.preset_directory,
                title="Load Preset",
                filetypes=(("JSON files", "*.json"), ("All files", "*.*"))
            )
            if not preset_path:
                return None

            logging.info(f"Selected preset path: {preset_path}")
            return self.load_preset(preset_path)
        except Exception as e:
            logging.error(f"Error loading preset: {str(e)}")
            messagebox.showerror("Error", f"Failed to load preset: {str(e)}")
            return None
