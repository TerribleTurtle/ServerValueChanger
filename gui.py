"""
This module defines the GUI for the JSON Configuration Editor application.

Classes:
    Application: Main application class for the JSON Configuration Editor.

Methods (Application class):
    __init__(self): Initializes the main application window.
    create_widgets(self): Creates the widgets for the GUI.
    on_tab_select(self, _event=None): Handles tab selection in the listbox.
    show_tab_content(self, tab_name): Displays the content of the selected tab.
    create_widget(self, setting, parent): Creates a widget for a given setting.
    initialize_defaults(self): Initializes the UI with default values.
    apply_changes(self): Applies changes made in the GUI to the configuration files.
    save_preset(self): Saves the current settings as a preset.
    load_preset(self): Loads a preset and applies it to the UI.
"""

import tkinter as tk
from tkinter import messagebox
import logging
import json  # Import json to avoid undefined variable error

from config_manager import ConfigManager
from logger_setup import LoggerSetup
from batch_apply import BatchApply
from preset_manager import PresetManager
from ui_updater import UIUpdater
from tooltip import Tooltip

class Application(tk.Tk):
    """
    Main application class for the JSON Configuration Editor.
    """

    def __init__(self):
        super().__init__()
        self.title("Server Value Changer")
        self.geometry("850x850")

        self.config_manager = ConfigManager('config.json', 'config_schema.json')
        LoggerSetup(self.config_manager)

        self.preset_manager = PresetManager('presets')
        self.ui_updater = UIUpdater(self.config_manager)
        self.batch_apply = BatchApply(self.config_manager)

        logging.debug("Creating widgets")
        self.create_widgets()

        logging.debug("Initializing defaults")
        self.initialize_defaults()

        self.center_window()

    def create_widgets(self):
        """
        Creates the widgets for the GUI.
        """
        main_frame = tk.Frame(self)
        main_frame.pack(expand=True, fill="both")

        # Left panel for tabs
        left_panel = tk.Frame(main_frame, width=200)
        left_panel.pack(side="left", fill="y")

        self.tab_listbox = tk.Listbox(left_panel)
        self.tab_listbox.pack(expand=True, fill="both")
        self.tab_listbox.bind("<<ListboxSelect>>", self.on_tab_select)

        # Right panel for tab content
        right_panel = tk.Frame(main_frame)
        right_panel.pack(side="right", expand=True, fill="both")

        # Canvas and scrollbar for right panel
        self.canvas = tk.Canvas(right_panel)
        self.scrollbar = tk.Scrollbar(right_panel, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Bind mouse wheel events
        self.bind_mouse_wheel()

        self.tabs = {}
        self.settings = {}

        schema = self.config_manager.get_schema()
        for tab_name, tab_data in schema['tabs'].items():
            if tab_name not in self.tabs:
                self.tabs[tab_name] = tk.Frame(self.scrollable_frame)
                self.tabs[tab_name].pack(side="top", fill="both", expand=True)
                self.tab_listbox.insert("end", tab_name)
                self.tabs[tab_name].grid_columnconfigure(0, weight=1)
                self.tabs[tab_name].grid_columnconfigure(1, weight=1)

            for group_name, group_data in tab_data['groups'].items():
                col = group_data['column']
                group_frame = tk.LabelFrame(self.tabs[tab_name], text=group_name)
                group_frame.grid(row=len(self.tabs[tab_name].grid_slaves(column=col)),
                                 column=col, padx=5, pady=5, sticky="nsew")
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

    def on_tab_select(self, _event=None):
        """
        Handles tab selection in the listbox.
        """
        if not self.tab_listbox.curselection():
            return  # Return early if there is no selection
        selected_tab = self.tab_listbox.get(self.tab_listbox.curselection())
        self.show_tab_content(selected_tab)

    def show_tab_content(self, tab_name):
        """
        Displays the content of the selected tab.
        """
        for tab in self.tabs.values():
            tab.pack_forget()
        self.tabs[tab_name].pack(side="top", fill="both", expand=True)

    def create_widget(self, setting, parent):
        ui_element = setting['ui_element']
        inline_with_previous = ui_element.get('inline_with_previous', False)
        if inline_with_previous:
            row = len(parent.grid_slaves()) // 2 - 1
            col = 2
        else:
            row = len(parent.grid_slaves()) // 2
            col = 0

        top_label_visible = ui_element.get('top_label_visible', False)
        if top_label_visible:
            top_label_sticky = ui_element.get('top_label_sticky', 'ew')  # Default to 'ew' if not specified
            top_label = tk.Label(parent, text=ui_element.get('top_label', setting['label']))
            top_label.grid(row=row * 2, column=col, columnspan=2, padx=5, pady=5, sticky=top_label_sticky)
            if 'description' in setting:
                Tooltip(top_label, setting['description'])
            widget_row = row * 2 + 1
        else:
            widget_row = row * 2

        left_label_visible = ui_element.get('left_label_visible', True)
        if left_label_visible:
            left_label_sticky = ui_element.get('left_label_sticky', 'w')  # Default to 'w' if not specified
            left_label = tk.Label(parent, text=setting['label'])
            left_label.grid(row=widget_row, column=col, padx=5, pady=5, sticky=left_label_sticky)
            if 'description' in setting:
                Tooltip(left_label, setting['description'])
            widget_col = col + 1
        else:
            widget_col = col

        if ui_element['type'] == 'entry':
            entry = tk.Entry(parent, width=ui_element.get('widget_width', 20))
            entry.grid(row=widget_row, column=widget_col, padx=5, pady=5, sticky="ew")
            self.settings[setting['key_path']] = entry
        elif ui_element['type'] == 'checkbox':
            var = tk.BooleanVar()
            checkbox = tk.Checkbutton(parent, variable=var)
            checkbox.grid(row=widget_row, column=widget_col, padx=5, pady=5, sticky="w")
            self.settings[setting['key_path']] = var

        parent.grid_columnconfigure(col, weight=1)
        parent.grid_columnconfigure(widget_col, weight=1)

    def initialize_defaults(self):
        """
        Initializes the UI with default values.
        """
        logging.debug("Calling initialize_with_defaults")
        self.ui_updater.initialize_with_defaults(self.settings)

    def apply_changes(self):
        """
        Applies changes made in the GUI to the configuration files.
        """
        try:
            schema = self.config_manager.get_schema()
            self.batch_apply.apply_changes(self.settings, schema)
            messagebox.showinfo("Info", "Changes have been applied successfully.")
        except FileNotFoundError as e:
            logging.error("File not found: %s", str(e))
            messagebox.showerror("Error", f"File not found: {str(e)}")
        except json.JSONDecodeError as e:
            logging.error("JSON decoding error: %s", str(e))
            messagebox.showerror("Error", f"JSON decoding error: {str(e)}")
        except KeyError as e:
            logging.error("Key error: %s", str(e))
            messagebox.showerror("Error", f"Key error: {str(e)}")
        except Exception as e:   # pylint: disable=broad-exception-caught
            logging.error("Error applying changes: %s", str(e))
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")

    def save_preset(self):
        """
        Saves the current settings as a preset.
        """
        changes = self.ui_updater.capture_ui_state(self.settings)
        self.preset_manager.save_preset_dialog(changes)

    def load_preset(self):
        """
        Loads a preset and applies it to the UI.
        """
        changes = self.preset_manager.load_preset_dialog()
        if changes:
            logging.info("Changes loaded: %s", changes)
            self.ui_updater.update_ui_with_preset(self.settings, changes)
            messagebox.showinfo("Info", "Preset loaded successfully.")
        else:
            messagebox.showerror("Error", "Failed to load preset.")

    def center_window(self):
        """
        Centers the window on the screen.
        """
        self.update_idletasks()  # Update "requested size" from geometry manager

        window_width = self.winfo_width()
        window_height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def bind_mouse_wheel(self):
        """
        Binds the mouse wheel to the canvas scrollbar.
        """
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)
        self.canvas.bind_all("<Button-4>", self.on_mouse_wheel)
        self.canvas.bind_all("<Button-5>", self.on_mouse_wheel)

    def on_mouse_wheel(self, event):
        """
        Handles the mouse wheel event for scrolling.
        """
        if event.num == 5 or event.delta == -120:
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta == 120:
            self.canvas.yview_scroll(-1, "units")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app = Application()
    app.mainloop()
