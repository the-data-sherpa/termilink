"""Tests for data models."""

from datetime import datetime
from pathlib import Path

import pytest
from pydantic import ValidationError

from termilink.models import Config, Note, NoteFormat


def test_note_format_plain() -> None:
    """Test plain note formatting."""
    note = Note(
        content="Test note",
        format_type=NoteFormat.PLAIN,
        timestamp=datetime(2024, 1, 1, 14, 30),
    )

    formatted = note.format_content(include_timestamp=True, timestamp_format="%H:%M")
    assert formatted == "14:30 Test note"


def test_note_format_timestamp() -> None:
    """Test timestamp note formatting."""
    note = Note(
        content="Test note",
        format_type=NoteFormat.TIMESTAMP,
        timestamp=datetime(2024, 1, 1, 14, 30),
    )

    formatted = note.format_content(include_timestamp=True, timestamp_format="%H:%M")
    assert formatted == "**14:30** - Test note"


def test_note_format_bullet() -> None:
    """Test bullet note formatting."""
    note = Note(
        content="Test note",
        format_type=NoteFormat.BULLET,
        timestamp=datetime(2024, 1, 1, 14, 30),
    )

    formatted = note.format_content(include_timestamp=True, timestamp_format="%H:%M")
    assert formatted == "- 14:30 - Test note"


def test_note_format_task() -> None:
    """Test task note formatting."""
    note = Note(
        content="Test note",
        format_type=NoteFormat.TASK,
        timestamp=datetime(2024, 1, 1, 14, 30),
    )

    formatted = note.format_content(include_timestamp=True, timestamp_format="%H:%M")
    assert formatted == "- [ ] 14:30 - Test note"


def test_note_format_with_tags() -> None:
    """Test note formatting with tags."""
    note = Note(
        content="Test note",
        format_type=NoteFormat.TIMESTAMP,
        tags=["important", "work"],
        timestamp=datetime(2024, 1, 1, 14, 30),
    )

    formatted = note.format_content(include_timestamp=True, timestamp_format="%H:%M")
    assert formatted == "**14:30** - Test note - #important #work"


def test_note_format_without_timestamp() -> None:
    """Test note formatting without timestamp."""
    note = Note(
        content="Test note",
        format_type=NoteFormat.TIMESTAMP,
        timestamp=datetime(2024, 1, 1, 14, 30),
    )

    formatted = note.format_content(include_timestamp=False)
    assert formatted == "Test note"


def test_config_validation_invalid_path(tmp_path: Path) -> None:
    """Test config validation with invalid path."""
    invalid_path = tmp_path / "nonexistent"

    with pytest.raises(ValidationError) as exc_info:
        Config(vault_path=invalid_path)

    assert "Vault path does not exist" in str(exc_info.value)


def test_config_validation_file_not_dir(tmp_path: Path) -> None:
    """Test config validation with file instead of directory."""
    file_path = tmp_path / "test.txt"
    file_path.write_text("test")

    with pytest.raises(ValidationError) as exc_info:
        Config(vault_path=file_path)

    assert "not a directory" in str(exc_info.value)


def test_config_valid(tmp_path: Path) -> None:
    """Test valid config creation."""
    config = Config(vault_path=tmp_path)

    assert config.vault_path == tmp_path.resolve()
    assert config.daily_notes_path == "Daily Notes"
    assert config.default_format == NoteFormat.TIMESTAMP
    assert config.include_timestamp is True
