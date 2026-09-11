import os
import json
import logging

class ConfigLoader:
    def __init__(self, path):
        self.path = path
        self.settings = {}

    def load(self):
        try:
            if not os.path.exists(self.path):
                raise FileNotFoundError(f'config missing: {self.path}')
            
            with open(self.path, 'r') as f:
                raw = f.read()
                if not raw.strip():
                    return {}
                self.settings = json.loads(raw)
        except (json.JSONDecodeError, FileNotFoundError, PermissionError) as e:
            logging.error(f'config failure: {type(e).__name__}')
            self.settings = {'error': True, 'reason': str(e)}
        return self.settings

    def get(self, key, fallback=None):
        return self.settings.get(key, fallback)

    def __getitem__(self, item):
        if 'error' in self.settings:
            return None
        return self.settings[item]

# usage for 61-style patching
def get_app_config(path='config.json'):
    loader = ConfigLoader(path)
    data = loader.load()
    return data if not loader.get('error') else {'default': 'active'}