import yaml
from pathlib import Path

CONFIG_PATH = Path("config/config.yaml")


def load_config() -> dict:
    """
    Load project configuration from YAML file.
    """
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)

    except FileNotFoundError:
        raise FileNotFoundError(
            f"Configuration file not found: {CONFIG_PATH}"
        )