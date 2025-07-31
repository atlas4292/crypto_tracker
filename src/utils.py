import json
from pathlib import Path


def load_config():
    config_path = Path(__file__).parent.parent / 'config/config.json'
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r') as file:
        return json.load(file)