# gui.py
import tkinter as tk
from tkinter import messagebox
import logging
from config_manager import ConfigManager
from logger_setup import LoggerSetup
from batch_apply import BatchApply
from preset_manager import PresetManager
from ui_updater import UIUpdater
from tooltip import Tooltip

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("JSON Configuration Editor")
        self.geometry("800x600")

        self.config_manager = ConfigManager('config.json', 'config_schema.json')
        LoggerSetup(self.config_manager)

        self.preset_manager = PresetManager('presets')
        self.ui_updater = UIUpdater(self.config_manager)
        self.batch_apply = BatchApply(self.config_manager)
        
        logging.debug("Creating widgets")
        self.create_widgets()
        
        logging.debug("Initializing defaults")
        self.initialize_defaults()

    def create_widgets(self):
        main_frame = tk.Frame(self)
        main_frame.pack(expand=True, fill="both")

        # Left panel for tabs
        left_panel = tk.Frame(main_frame, width=200)
        left_panel.pack(side="left", fill="y")
        
        self.tab_listbox = tk.Listbox(left_panel)
        self.tab_listbox.pack(expand=True, fill="both")
        self.tab_listbox.bind("<<ListboxSelect>>", self.on_tab_select)

        # Right panel for tab content
        self.tab_content = tk.Frame(main_frame)
        self.tab_content.pack(side="right", expand=True, fill="both")

        self.tabs = {}
        self.settings = {}

        schema = self.config_manager.get_schema()
        for tab_name, tab_data in schema['tabs'].items():
            if tab_name not in self.tabs:
                self.tabs[tab_name] = tk.Frame(self.tab_content)
                self.tabs[tab_name].pack(side="top", fill="both", expand=True)
                self.tab_listbox.insert("end", tab_name)
                self.tabs[tab_name].grid_columnconfigure(0, weight=1)
                self.tabs[tab_name].grid_columnconfigure(1, weight=1)

            for group_name, group_data in tab_data['groups'].items():
                col = group_data['column']
                group_frame = tk.LabelFrame(self.tabs[tab_name], text=group_name)
                group_frame.grid(row=len(self.tabs[tab_name].grid_slaves(column=col)), column=col, padx=5, pady=5, sticky="nsew")
                group_frame.grid_columnconfigure(0, weight=1)
                group_frame.grid_columnconfigure(1, weight=1)

                for setting in group_data['settings']:
                    self.create_widget(setting, group_frame)

        logging.debug("Creating bottom panel for buttons")
        # Bottom panel for buttons
        bottom_panel = tk.Frame(self)
        bottom_panel.pack(side="bottom", fill="x")

        self.apply_button = tk.Button(bottom_panel, text="Apply Changes", command=self.apply_changes)
        self.apply_button.pack(side="left", padx=5, pady=5)

        self.save_preset_button = tk.Button(bottom_panel, text="Save Preset", command=self.save_preset)
        self.save_preset_button.pack(side="left", padx=5, pady=5)

        self.load_preset_button = tk.Button(bottom_panel, text="Load Preset", command=self.load_preset)
        self.load_preset_button.pack(side="left", padx=5, pady=5)

        self.show_tab_content(self.tab_listbox.get(0))

    def on_tab_select(self, event):
        if not self.tab_listbox.curselection():
            return  # Return early if there is no selection
        selected_tab = self.tab_listbox.get(self.tab_listbox.curselection())
        self.show_tab_content(selected_tab)

    def show_tab_content(self, tab_name):
        for tab in self.tabs.values():
            tab.pack_forget()
        self.tabs[tab_name].pack(side="top", fill="both", expand=True)

    def create_widget(self, setting, parent):
        ui_element = setting['ui_element']
        
        # Determine the row
        inline_with_previous = ui_element.get('inline_with_previous', False)
        if inline_with_previous:
            row = len(parent.grid_slaves()) // 2 - 1  # Use the previous row
            col = 2  # Place in the next available column
        else:
            row = len(parent.grid_slaves()) // 2  # New row
            col = 0

        # Top label
        top_label_visible = ui_element.get('top_label_visible', False)
        if top_label_visible:
            top_label = tk.Label(parent, text=ui_element.get('top_label', setting['label']))
            top_label.grid(row=row * 2, column=col, columnspan=2, padx=5, pady=5, sticky="e")
            if 'description' in setting:
                Tooltip(top_label, setting['description'])
            widget_row = row * 2 + 1
        else:
            widget_row = row

        # Left label
        left_label_visible = ui_element.get('left_label_visible', True)
        if left_label_visible:
            left_label = tk.Label(parent, text=setting['label'])
            left_label.grid(row=widget_row, column=col, padx=5, pady=5, sticky="e")
            if 'description' in setting:
                Tooltip(left_label, setting['description'])
            widget_col = col + 1
        else:
            widget_col = col

        if ui_element['type'] == 'entry':
            entry = tk.Entry(parent, width=ui_element.get('widget_width', 20))
            entry.grid(row=widget_row, column=widget_col, padx=5, pady=5, sticky="e")
            self.settings[setting['key_path']] = entry
            logging.debug(f"Created entry widget for {setting['key_path']} with default {setting.get('default')}")
        elif ui_element['type'] == 'checkbox':
            var = tk.BooleanVar()
            checkbox = tk.Checkbutton(parent, variable=var)
            checkbox.grid(row=widget_row, column=widget_col, padx=5, pady=5, sticky="e")
            self.settings[setting['key_path']] = var
            logging.debug(f"Created checkbox widget for {setting['key_path']} with default {setting.get('default')}")

    def initialize_defaults(self):
        logging.debug("Calling initialize_with_defaults")
        self.ui_updater.initialize_with_defaults(self.settings)

    def apply_changes(self):
        try:
            schema = self.config_manager.get_schema()
            self.batch_apply.apply_changes(self.settings, schema)
            messagebox.showinfo("Info", "Changes have been applied successfully.")
        except Exception as e:
            logging.error(f"Error applying changes: {str(e)}")
            messagebox.showerror("Error", str(e))

    def save_preset(self):
        changes = self.ui_updater.capture_ui_state(self.settings)
        self.preset_manager.save_preset_dialog(changes)

    def load_preset(self):
        changes = self.preset_manager.load_preset_dialog()
        if changes:
            logging.info(f"Changes loaded: {changes}")
            self.ui_updater.update_ui_with_preset(self.settings, changes)
            messagebox.showinfo("Info", "Preset loaded successfully.")
        else:
            messagebox.showerror("Error", "Failed to load preset.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app = Application()
    app.mainloop()
