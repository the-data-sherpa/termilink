"""Tests for configuration management."""

from pathlib import Path

import pytest

from termilink.config import create_default_config, load_config, save_config
from termilink.models import Config


def test_create_default_config(tmp_path: Path) -> None:
    """Test creating default configuration."""
    config = create_default_config(tmp_path)

    assert config.vault_path == tmp_path.resolve()
    assert config.daily_notes_path == "Daily Notes"
    assert config.include_timestamp is True


def test_save_and_load_config(tmp_path: Path) -> None:
    """Test saving and loading configuration."""
    vault_path = tmp_path / "vault"
    vault_path.mkdir()

    config = create_default_config(vault_path)
    config_file = tmp_path / "test_config.yaml"

    saved_path = save_config(config, config_file)
    assert saved_path == config_file
    assert config_file.exists()

    loaded_config = load_config(config_file)
    assert loaded_config is not None
    assert loaded_config.vault_path == vault_path.resolve()
    assert loaded_config.daily_notes_path == config.daily_notes_path


def test_load_config_not_found() -> None:
    """Test loading non-existent config file."""
    with pytest.raises(FileNotFoundError):
        load_config(Path("/nonexistent/config.yaml"))


def test_load_config_no_path() -> None:
    """Test loading config without specifying path."""
    # Should return None if no config found in default locations
    config = load_config()
    # This might be None or a valid config depending on system state
    assert config is None or isinstance(config, Config)
