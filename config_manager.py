# config_manager.py
import json
import os
import logging

class ConfigManager:
    def __init__(self, config_path, schema_path):
        self.config_path = config_path
        self.schema_path = schema_path
        self.config = self.load_config()
        self.schema = self.load_schema()

    def load_config(self):
        if not os.path.exists(self.config_path):
            logging.error(f"Configuration file not found: {self.config_path}")
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as file:
            config = json.load(file)
        
        logging.info("Configuration file loaded successfully.")
        return config

    def load_schema(self):
        if not os.path.exists(self.schema_path):
            logging.error(f"Schema file not found: {self.schema_path}")
            raise FileNotFoundError(f"Schema file not found: {self.schema_path}")
        
        with open(self.schema_path, 'r') as file:
            schema = json.load(file)
        
        logging.info("Schema file loaded successfully.")
        return schema

    def get_setting(self, setting_path):
        keys = setting_path.split('.')
        value = self.config

        for key in keys:
            value = value.get(key)
            if value is None:
                logging.error(f"Setting '{setting_path}' not found in configuration.")
                raise KeyError(f"Setting '{setting_path}' not found in configuration.")

        return value

    def get_schema(self):
        return self.schema
