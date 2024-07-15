# app_logic.py
import logging
from tkinter import messagebox

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
