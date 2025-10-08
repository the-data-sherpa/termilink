"""Configuration management for termiLink."""

import json
from pathlib import Path

import yaml

from termilink.models import Config

CONFIG_LOCATIONS = [
    Path.home() / ".termilink.yaml",
    Path.home() / ".config" / "termilink" / "config.yaml",
    Path.cwd() / ".termilink.yaml",
]


def find_config_file() -> Path | None:
    """Find the first existing config file.

    Returns:
        Path to config file or None if not found
    """
    for config_path in CONFIG_LOCATIONS:
        if config_path.exists():
            return config_path
    return None


def load_config(config_path: Path | None = None) -> Config | None:
    """Load configuration from file.

    Args:
        config_path: Optional path to config file. If None, searches default locations.

    Returns:
        Config object or None if no config found

    Raises:
        ValidationError: If config file is invalid
        ValueError: If config file format is not supported
    """
    if config_path is None:
        config_path = find_config_file()

    if config_path is None:
        return None

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, encoding="utf-8") as f:
        if config_path.suffix in [".yaml", ".yml"]:
            data = yaml.safe_load(f)
        elif config_path.suffix == ".json":
            data = json.load(f)
        else:
            raise ValueError(f"Unsupported config file format: {config_path.suffix}")

    return Config(**data)


def save_config(config: Config, config_path: Path | None = None) -> Path:
    """Save configuration to file.

    Args:
        config: Config object to save
        config_path: Optional path to save config. If None, uses default location.

    Returns:
        Path where config was saved
    """
    if config_path is None:
        config_path = Path.home() / ".termilink.yaml"

    config_path.parent.mkdir(parents=True, exist_ok=True)

    # Convert to dict and handle Path serialization
    config_dict = config.model_dump(mode="json")
    config_dict["vault_path"] = str(config.vault_path)

    with open(config_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(config_dict, f, default_flow_style=False, sort_keys=False)

    return config_path


def create_default_config(vault_path: Path) -> Config:
    """Create a default configuration.

    Args:
        vault_path: Path to Obsidian vault

    Returns:
        Default Config object
    """
    return Config(vault_path=vault_path)
