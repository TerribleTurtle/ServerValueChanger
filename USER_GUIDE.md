# ServerValueChanger User Guide

## Overview

The ServerValueChanger is a GUI tool designed to help users easily manage and edit settings in SPT (Single Player Tarkov) server configuration files. This guide will walk you through the steps of setting up the configuration, loading, applying, and saving changes, and understanding the schema.

## Setup

### Update the Configuration with Your File Paths

Before using the application, you need to update the `config.json` file to reflect the correct paths of your SPT server database and server configuration files. Here’s an example of what the `config.json` file looks like:

```json
{
  "paths": {
    "server_database": "S:/server config test/SPT_Data/Server/database",
    "server_config": "S:/server config test/SPT_Data/Server/configs"
  },
  "logging": {
    "level": "DEBUG",
    "file": "app.log"
  },
  "backup": {
    "directory": "backup"
  }
}
```

Replace the paths under `"server_database"` and `"server_config"` with the actual paths where your SPT server database and configuration files are located. Ensure these paths are accessible by the application.

## Using the GUI

### Loading the Application

1. Ensure you have Python installed on your system.
2. Navigate to the directory containing the application's files.
3. Run the application by executing the following command in your terminal or command prompt:

   ```sh
   python main.py
   ```

This will launch the ServerValueChanger GUI.

### Navigating the GUI

- **Tabs and Groups**: The GUI is organized into tabs and groups based on the schema defined in `config_schema.json`. Each tab contains groups of settings.
- **Settings**: Each group contains individual settings that you can modify. These settings are represented by various UI elements like text entries and checkboxes.

### Applying Changes

1. **Modify Settings**: Use the GUI to modify the settings as needed. Each setting is described with a label and, if available, a tooltip for additional information.
2. **Apply Changes**: Click the "Apply Changes" button to save your modifications to the respective JSON configuration files. The application will validate your changes and update the files accordingly.

### Saving and Loading Presets

- **Save Preset**: After making changes, you can save the current settings as a preset by clicking the "Save Preset" button. This will open a dialog where you can name and save your preset file.
- **Load Preset**: You can load a previously saved preset by clicking the "Load Preset" button. This will open a dialog to select and load a preset file, applying the saved settings to the GUI.

## Understanding the Schema

The `config_schema.json` file defines the structure, types, and UI elements for each setting in the configuration files. Here's a breakdown of its structure and values:

```json
{
  "tabs": {
    "Gameplay": {
      "groups": {
        "Ammo Settings": {
          "column": 1,
          "settings": [
            {
              "label": "Ammo - Max Stack Size",
              "description": "The maximum number of ammo stacks.",
              "file": "database/templates/items.json",
              "key_path": "_props.StackMaxSize",
              "type": "integer",
              "default": 60,
              "criteria": {"_parent": "5485a8684bdc2da71d8b4567"},
              "complex": true,
              "ui_element": {
                "type": "entry",
                "widget_width": 10,
                "inline_with_previous": false,
                "top_label": "Ammo - Max Stack Size",
                "top_label_visible": false,
                "left_label_visible": true
              }
            }
          ]
        }
      }
    }
  }
}
```

### Schema Elements

- **Tabs**: The top-level keys under `"tabs"` represent different tabs in the GUI.
- **Groups**: Each tab contains groups, which are defined under `"groups"`. Groups are used to organize related settings.
- **Settings**: Each group contains multiple settings. Each setting has several attributes:

  - **label**: The display name of the setting in the GUI.
  - **description**: A tooltip description for the setting.
  - **file**: The path to the JSON file where the setting is located.
  - **key_path**: The JSON key path within the file where the setting is stored.
  - **type**: The data type of the setting (e.g., `"integer"`, `"boolean"`).
  - **default**: The default value of the setting.
  - **criteria**: Optional criteria to filter specific items in the JSON file (used for complex settings).
  - **complex**: A boolean indicating whether this setting requires complex handling.
  - **ui_element**: Defines the UI element for the setting, including:
    - **type**: The type of UI element (e.g., `"entry"`, `"checkbox"`).
    - **widget_width**: The width of the UI element.
    - **inline_with_previous**: Whether this setting should be displayed inline with the previous one.
    - **top_label**: The text for the top label.
    - **top_label_visible**: Whether the top label is visible.
    - **left_label_visible**: Whether the left label is visible.

This schema controls how each setting is displayed and managed in the GUI, ensuring that the application can dynamically generate the appropriate interface elements.

## Conclusion

This user guide provides you with the necessary information to set up, use, and understand the ServerValueChanger. By following these instructions, you should be able to efficiently manage and edit your SPT server configuration files. If you encounter any issues or have further questions, please refer to the source code or seek assistance from the support team.