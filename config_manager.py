"""
Module for managing configuration files.

Classes:
    ConfigManager: Handles loading and retrieving settings from a configuration file and its schema.

Methods:
    __init__(self, config_path, schema_path): Initializes ConfigManager with paths to configuration and schema files.
    load_config(self): Loads the configuration file.
    load_schema(self): Loads the schema file.
    get_setting(self, setting_path): Retrieves a setting from the configuration.
    get_schema(self): Retrieves the schema.
"""

import json
import os
import logging

class ConfigManager:
    """
    ConfigManager handles loading and retrieving settings from a configuration file and its schema.
    """
    def __init__(self, config_path, schema_path):
        """
        Initialize ConfigManager with paths to configuration and schema files.
        """
        self.config_path = config_path
        self.schema_path = schema_path
        self.config = self.load_config()
        self.schema = self.load_schema()

    def load_config(self):
        """
        Load the configuration file.
        """
        if not os.path.exists(self.config_path):
            logging.error("Configuration file not found: %s", self.config_path)
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        with open(self.config_path, 'r', encoding='utf-8') as file:
            config = json.load(file)

        logging.info("Configuration file loaded successfully.")
        return config

    def load_schema(self):
        """
        Load the schema file.
        """
        if not os.path.exists(self.schema_path):
            logging.error("Schema file not found: %s", self.schema_path)
            raise FileNotFoundError(f"Schema file not found: {self.schema_path}")

        with open(self.schema_path, 'r', encoding='utf-8') as file:
            schema = json.load(file)

        logging.info("Schema file loaded successfully.")
        return schema

    def get_setting(self, setting_path):
        """
        Retrieve a setting from the configuration.
        """
        keys = setting_path.split('.')
        value = self.config

        for key in keys:
            value = value.get(key)
            if value is None:
                logging.error("Setting '%s' not found in configuration.", setting_path)
                raise KeyError(f"Setting '{setting_path}' not found in configuration.")

        return value

    def get_schema(self):
        """
        Retrieve the schema.
        """
        return self.schema
