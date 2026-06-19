import yaml
from pathlib import Path

CONFIG_PATH = Path("config/parameters.yaml")

def load_config() -> dict:
    """Load parameter configuration from YAML file"""
    try:
        with open(CONFIG_PATH, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"⚠️ Config file not found at {CONFIG_PATH}")
        return {}