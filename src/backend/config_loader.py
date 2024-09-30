import os
import importlib.util

class ConfigLoader:
    def __init__(self):
        if os.name == "nt":
            config_file_path = 'c:/config.py'
        elif os.name == "posix":
            config_file_path = '/home/alikashash/config.py'
        
        spec = importlib.util.spec_from_file_location("config", config_file_path)
        self.config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.config)

    @property
    def openai_api_key(self):
        return self.config.OPENAI_API_KEY

# Instantiate the loader
config_loader = ConfigLoader()
