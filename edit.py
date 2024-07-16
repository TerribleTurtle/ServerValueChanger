"""
This module provides a Tkinter based GUI to edit JSON configuration files,
allowing users to add, edit, and delete tabs, groups, and settings.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os

CONFIG_FILE = 'config_schema.json'
json_data = {}


def load_json(file_path: str) -> dict:
    """Load JSON data from a file."""
    with open(file_path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


def save_json(json_content: dict, file_path: str) -> None:
    """Save JSON data to a file."""
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_content, json_file, indent=4)


def save_changes() -> None:
    """Add or Update Tab, Group, and Setting on Save."""
    selected_item = tree.selection()
    selected_label = tree.item(selected_item[0], 'text') if selected_item else None

    tab_name = tab_name_entry.get()
    group_name = group_name_entry.get()
    group_column = group_column_entry.get()
    setting_label = setting_label_entry.get()
    setting_description = setting_description_entry.get()
    setting_file = setting_file_entry.get()
    setting_key_path = setting_key_path_entry.get()
    setting_type = setting_type_combobox.get()
    setting_default = setting_default_entry.get()
    setting_complex = complex_checkbox_var.get()

    if setting_default:
        try:
            if setting_type == 'integer':
                setting_default = int(setting_default)
            elif setting_type == 'float':
                setting_default = float(setting_default)
            elif setting_type == 'boolean':
                setting_default = setting_default.lower() in ("yes", "true", "t", "1")
        except ValueError:
            messagebox.showerror("Input Error", "Invalid default value for the selected type")
            return

    if not tab_name:
        messagebox.showerror("Input Error", "Please enter a valid tab name")
        return

    created_new_item = False

    if tab_name not in json_data['tabs']:
        json_data['tabs'][tab_name] = {"groups": {}}
        created_new_item = True

    if group_name:
        if group_name not in json_data['tabs'][tab_name]['groups']:
            json_data['tabs'][tab_name]['groups'][group_name] = {
                "column": int(group_column) if group_column else 1,
                "settings": []
            }
            created_new_item = True
        else:
            json_data['tabs'][tab_name]['groups'][group_name]['column'] = int(group_column) if group_column else 1

    if setting_label:
        new_setting = {
            "label": setting_label,
            "description": setting_description,
            "file": setting_file,
            "key_path": setting_key_path,
            "type": setting_type,
            "default": setting_default,
            "criteria": {},
            "complex": setting_complex,
            "ui_element": {
                "type": ui_type_combobox.get(),
                "widget_width": int(ui_widget_width_entry.get()) if ui_widget_width_entry.get() else 10,
                "inline_with_previous": ui_inline_with_previous_checkbox_var.get(),
                "top_label": ui_top_label_entry.get(),
                "top_label_visible": ui_top_label_visible_checkbox_var.get(),
                "left_label_visible": ui_left_label_visible_checkbox_var.get()
            }
        }
        settings_list = json_data['tabs'][tab_name]['groups'][group_name]['settings']
        for index, setting in enumerate(settings_list):
            if setting['label'] == setting_label:
                settings_list[index] = new_setting
                break
        else:
            settings_list.append(new_setting)
            created_new_item = True

    save_json(json_data, CONFIG_FILE)
    load_config()

    if created_new_item:
        if setting_label:
            select_item_by_label(setting_label)
        elif group_name:
            select_item_by_label(group_name)
        else:
            select_item_by_label(tab_name)
    else:
        if selected_label:
            select_item_by_label(selected_label)

    messagebox.showinfo("File Saved", "The JSON configuration has been saved and reloaded successfully!")


def select_item_by_label(label: str) -> None:
    """Select an item in the tree by its label."""
    for item in tree.get_children():
        if tree.item(item, 'text') == label:
            tree.selection_set(item)
            tree.see(item)
            populate_fields()
            return
        for sub_item in tree.get_children(item):
            if tree.item(sub_item, 'text') == label:
                tree.selection_set(sub_item)
                tree.see(sub_item)
                populate_fields()
                return
            for sub_sub_item in tree.get_children(sub_item):
                if tree.item(sub_sub_item, 'text') == label:
                    tree.selection_set(sub_sub_item)
                    tree.see(sub_sub_item)
                    populate_fields()
                    return


def populate_fields(event=None) -> None:
    """Populate fields for editing when selecting an item in the tree."""
    selected_item = tree.selection()
    if not selected_item:
        return
    item = tree.item(selected_item[0])
    clear_fields()
    if item['values'][0] == "Tab":
        tab_name_entry.insert(0, item['text'])
    elif item['values'][0] == "Group":
        parent_item = tree.parent(selected_item[0])
        tab_name_entry.insert(0, tree.item(parent_item)["text"])
        group_name_entry.insert(0, item['text'])
        group_column_entry.insert(0, json_data['tabs'][tree.item(parent_item)["text"]]['groups'][item['text']]['column'])
    elif item['values'][0] == "Setting":
        setting_label_entry.insert(0, item['text'])
        parent_item = tree.parent(selected_item[0])
        group_name_entry.insert(0, tree.item(parent_item)["text"])
        group_column_entry.insert(0, json_data['tabs'][tree.item(tree.parent(parent_item))["text"]]['groups'][tree.item(parent_item)["text"]]['column'])
        tab_item = tree.parent(parent_item)
        tab_name_entry.insert(0, tree.item(tab_item)["text"])
        for setting in json_data['tabs'][tab_name_entry.get()]['groups'][group_name_entry.get()]['settings']:
            if setting['label'] == item['text']:
                setting_description_entry.insert(0, setting['description'])
                setting_file_entry.insert(0, setting['file'])
                setting_key_path_entry.insert(0, setting['key_path'])
                setting_type_combobox.set(setting['type'])
                setting_default_entry.insert(0, str(setting['default']))
                complex_checkbox_var.set(setting.get('complex', False))

                # Populate UI Element fields
                ui_element = setting['ui_element']
                ui_type_combobox.set(ui_element.get('type', ''))
                ui_widget_width_entry.insert(0, ui_element.get('widget_width', ''))
                ui_inline_with_previous_checkbox_var.set(ui_element.get('inline_with_previous', False))
                ui_top_label_entry.insert(0, ui_element.get('top_label', ''))
                ui_top_label_visible_checkbox_var.set(ui_element.get('top_label_visible', False))
                ui_left_label_visible_checkbox_var.set(ui_element.get('left_label_visible', False))
                break


def delete_item() -> None:
    """Delete the selected item (tab, group, or setting)."""
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Selection Error", "Please select an item to delete")
        return
    item = tree.item(selected_item[0])
    if item['values'][0] == "Tab":
        del json_data['tabs'][item['text']]
    elif item['values'][0] == "Group":
        tab_name = tree.item(tree.parent(selected_item[0]))['text']
        del json_data['tabs'][tab_name]['groups'][item['text']]
    elif item['values'][0] == "Setting":
        group_item = tree.parent(selected_item[0])
        group_name = tree.item(group_item)['text']
        tab_item = tree.parent(group_item)
        tab_name = tree.item(tab_item)['text']
        settings = json_data['tabs'][tab_name]['groups'][group_name]['settings']
        json_data['tabs'][tab_name]['groups'][group_name]['settings'] = [s for s in settings if s['label'] != item['text']]
    update_tree()
    clear_fields()


def update_tree() -> None:
    """Update the tree view with the current JSON data."""
    for item in tree.get_children():
        tree.delete(item)
    for tab, tab_content in json_data['tabs'].items():
        tab_id = tree.insert('', 'end', text=tab, values=("Tab",))
        for group, group_content in tab_content['groups'].items():
            group_id = tree.insert(tab_id, 'end', text=group, values=("Group",))
            for setting in group_content['settings']:
                tree.insert(group_id, 'end', text=setting['label'], values=("Setting",))


def load_config() -> None:
    """Load the configuration from the JSON file."""
    global json_data
    json_data = load_json(CONFIG_FILE)
    update_tree()


def clear_fields() -> None:
    """Clear all input fields."""
    tab_name_entry.delete(0, tk.END)
    group_name_entry.delete(0, tk.END)
    group_column_entry.delete(0, tk.END)
    setting_label_entry.delete(0, tk.END)
    setting_description_entry.delete(0, tk.END)
    setting_file_entry.delete(0, tk.END)
    setting_key_path_entry.delete(0, tk.END)
    setting_type_combobox.set('')
    setting_default_entry.delete(0, tk.END)
    complex_checkbox_var.set(False)
    ui_type_combobox.set('')
    ui_widget_width_entry.delete(0, tk.END)
    ui_inline_with_previous_checkbox_var.set(False)
    ui_top_label_entry.delete(0, tk.END)
    ui_top_label_visible_checkbox_var.set(False)
    ui_left_label_visible_checkbox_var.set(False)


def copy_label_to_top_label() -> None:
    """Copy the Setting Label to the Top Label field."""
    top_label = setting_label_entry.get()
    ui_top_label_entry.delete(0, tk.END)
    ui_top_label_entry.insert(0, top_label)


# Main Application
root = tk.Tk()
root.title("Server Value Changer Changer")

mainframe = ttk.Frame(root, padding="10 10 10 10")
mainframe.grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

tree = ttk.Treeview(mainframe, columns=("Type",))
tree.heading('#0', text='Name')
tree.heading('#1', text='Type')
tree.grid(row=0, column=0, columnspan=5, sticky='nsew')

scrollbar = ttk.Scrollbar(mainframe, orient=tk.VERTICAL, command=tree.yview)
scrollbar.grid(row=0, column=5, sticky=(tk.N, tk.S))
tree.configure(yscroll=scrollbar.set)
tree.bind('<<TreeviewSelect>>', populate_fields)

# UI Elements for Adding, Editing, and Deleting
tab_name_label = ttk.Label(mainframe, text="Tab Name:")
tab_name_label.grid(row=1, column=0, sticky=tk.W)
tab_name_entry = ttk.Entry(mainframe, width=30)
tab_name_entry.grid(row=1, column=1, sticky='ew')

group_name_label = ttk.Label(mainframe, text="Group Name:")
group_name_label.grid(row=2, column=0, sticky=tk.W)
group_name_entry = ttk.Entry(mainframe, width=30)
group_name_entry.grid(row=2, column=1, sticky='ew')

group_column_label = ttk.Label(mainframe, text="Group Column:")
group_column_label.grid(row=2, column=2, sticky=tk.W)
group_column_entry = ttk.Entry(mainframe, width=10)
group_column_entry.grid(row=2, column=3, sticky='ew')

setting_frame = ttk.Labelframe(mainframe, text="Setting Details", padding="10 10 10 10")
setting_frame.grid(row=3, column=0, columnspan=6, sticky='ew')

# Labels and entry fields for setting details
setting_label_label = ttk.Label(setting_frame, text="Setting Label:")
setting_label_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
setting_label_entry = ttk.Entry(setting_frame, width=40)
setting_label_entry.grid(row=0, column=1, sticky='ew', padx=5, pady=5, columnspan=3)

setting_description_label = ttk.Label(setting_frame, text="Description:")
setting_description_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
setting_description_entry = ttk.Entry(setting_frame, width=40)
setting_description_entry.grid(row=1, column=1, sticky='ew', padx=5, pady=5, columnspan=3)

setting_file_label = ttk.Label(setting_frame, text="File:")
setting_file_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
setting_file_entry = ttk.Entry(setting_frame, width=40)
setting_file_entry.grid(row=2, column=1, sticky='ew', padx=5, pady=5, columnspan=3)

setting_key_path_label = ttk.Label(setting_frame, text="Key Path:")
setting_key_path_label.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
setting_key_path_entry = ttk.Entry(setting_frame, width=40)
setting_key_path_entry.grid(row=3, column=1, sticky='ew', padx=5, pady=5, columnspan=3)

setting_type_label = ttk.Label(setting_frame, text="Type:")
setting_type_label.grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
setting_type_combobox = ttk.Combobox(setting_frame, values=["boolean", "integer", "float", "string"])
setting_type_combobox.grid(row=4, column=1, sticky='ew', padx=5, pady=5)

setting_default_label = ttk.Label(setting_frame, text="Default:")
setting_default_label.grid(row=4, column=2, sticky=tk.W, padx=5, pady=5)
setting_default_entry = ttk.Entry(setting_frame, width=20)
setting_default_entry.grid(row=4, column=3, sticky='ew', padx=5, pady=5)

complex_checkbox_var = tk.BooleanVar()
complex_checkbox = ttk.Checkbutton(setting_frame, text="Complex", variable=complex_checkbox_var)
complex_checkbox.grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)

ui_element_frame = ttk.Labelframe(setting_frame, text="UI Element Details", padding="10 10 10 10")
ui_element_frame.grid(row=6, column=0, columnspan=4, sticky='ew')

ui_type_label = ttk.Label(ui_element_frame, text="UI Type:")
ui_type_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
ui_type_combobox = ttk.Combobox(ui_element_frame, values=["checkbox", "entry", "dropdown", "slider"])
ui_type_combobox.grid(row=0, column=1, sticky='ew', padx=5, pady=5)

ui_widget_width_label = ttk.Label(ui_element_frame, text="Widget Width:")
ui_widget_width_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
ui_widget_width_entry = ttk.Entry(ui_element_frame, width=20)
ui_widget_width_entry.grid(row=1, column=1, sticky='ew', padx=5, pady=5)

ui_inline_with_previous_label = ttk.Label(ui_element_frame, text="Inline with Previous:")
ui_inline_with_previous_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
ui_inline_with_previous_checkbox_var = tk.BooleanVar()
ui_inline_with_previous_checkbox = ttk.Checkbutton(ui_element_frame, variable=ui_inline_with_previous_checkbox_var)
ui_inline_with_previous_checkbox.grid(row=2, column=1, sticky='ew', padx=5, pady=5)

ui_top_label_label = ttk.Label(ui_element_frame, text="Top Label:")
ui_top_label_label.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
ui_top_label_entry = ttk.Entry(ui_element_frame, width=30)
ui_top_label_entry.grid(row=3, column=1, sticky='ew', padx=5, pady=5)
copy_button = ttk.Button(ui_element_frame, text="Copy Label", command=copy_label_to_top_label)
copy_button.grid(row=3, column=2, padx=5, pady=5)

ui_top_label_visible_label = ttk.Label(ui_element_frame, text="Top Label Visible:")
ui_top_label_visible_label.grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
ui_top_label_visible_checkbox_var = tk.BooleanVar()
ui_top_label_visible_checkbox = ttk.Checkbutton(ui_element_frame, variable=ui_top_label_visible_checkbox_var)
ui_top_label_visible_checkbox.grid(row=4, column=1, sticky='ew', padx=5, pady=5)

ui_left_label_visible_label = ttk.Label(ui_element_frame, text="Left Label Visible:")
ui_left_label_visible_label.grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
ui_left_label_visible_checkbox_var = tk.BooleanVar()
ui_left_label_visible_checkbox = ttk.Checkbutton(ui_element_frame, variable=ui_left_label_visible_checkbox_var)
ui_left_label_visible_checkbox.grid(row=5, column=1, sticky='ew', padx=5, pady=5)

save_button = ttk.Button(mainframe, text="Save", command=save_changes)
save_button.grid(row=7, column=0)

delete_button = ttk.Button(mainframe, text="Delete Selected Item", command=delete_item)
delete_button.grid(row=7, column=1)

clear_button = ttk.Button(mainframe, text="Clear Fields", command=clear_fields)
clear_button.grid(row=7, column=2)

# Expand the mainframe to accommodate more entries
for i in range(8):
    mainframe.grid_rowconfigure(i, weight=1)
for j in range(6):
    mainframe.grid_columnconfigure(j, weight=1)

if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as json_file:
        json.dump({"tabs": {}}, json_file)

json_data = load_json(CONFIG_FILE)
update_tree()

root.mainloop()
