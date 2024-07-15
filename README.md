# ServerValueChanger

## Overview

ServerValueChanger is a powerful GUI tool designed to help players of Single Player Tarkov (SPT) easily manage and edit their server configuration files. This application allows you to customize your gameplay experience by modifying various settings in a user-friendly interface.

## Features

- **Easy Configuration Management**: Load, modify, and apply changes to your SPT server configuration files with ease.
- **Preset Management**: Save your custom settings as presets and load them whenever you want.
- **Schema-Based UI**: Dynamically generated UI based on a JSON schema, making it easy to add or update settings.
- **Complex Setting Handling**: Supports complex settings that require special handling, such as ammo stack sizes.

## Getting Started

### Prerequisites

- Python 3.x
- The following Python libraries: `tkinter`, `json`, `os`, `logging`
- Access to your SPT server configuration files

### Installation

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/yourusername/ServerValueChanger.git
   cd ServerValueChanger
   ```

2. **Install Dependencies**:
   Ensure you have the required Python libraries installed. You can install them using pip:
   ```sh
   pip install -r requirements.txt
   ```
   *(Note: The `requirements.txt` file should list all required libraries.)*

### Setup

1. **Update the Configuration**:
   Edit the `config.json` file to reflect the correct paths of your SPT server database and configuration files. Here’s an example:
   ```json
   {
     "paths": {
       "server_database": "YOUR_PATH/SPT_Data/Server/database",
       "server_config": "YOUR_PATH/SPT_Data/Server/configs"
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
   Replace the paths under `"server_database"` and `"server_config"` with the actual paths where your SPT server database and configuration files are located.

### Running the Application

1. **Launch the Application**:
   ```sh
   python main.py
   ```

   This will start the ServerValueChanger GUI.

## Usage

### Navigating the GUI

- **Tabs and Groups**: The GUI is organized into tabs and groups based on the schema defined in `config_schema.json`. Each tab contains groups of settings.
- **Settings**: Each group contains individual settings that you can modify. These settings are represented by various UI elements like text entries and checkboxes.

### Modifying Settings

1. **Modify Settings**: Use the GUI to modify the settings as needed. Each setting is described with a label and, if available, a tooltip for additional information.
2. **Apply Changes**: Click the "Apply Changes" button to save your modifications to the respective JSON configuration files. The application will validate your changes and update the files accordingly.

### Preset Management

- **Save Preset**: After making changes, you can save the current settings as a preset by clicking the "Save Preset" button. This will open a dialog where you can name and save your preset file.
- **Load Preset**: You can load a previously saved preset by clicking the "Load Preset" button. This will open a dialog to select and load a preset file, applying the saved settings to the GUI.

## Understanding the Schema

The `config_schema.json` file defines the structure, types, and UI elements for each setting in the configuration files. This schema controls how each setting is displayed and managed in the GUI, ensuring that the application can dynamically generate the appropriate interface elements.

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

## Contributing

If you'd like to contribute to ServerValueChanger, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## License

This project is licensed under the CC BY-NC 4.0 - see the LICENSE file for details.

## Contact

For any questions or issues, please open an issue on GitHub or contact the repository owner.

