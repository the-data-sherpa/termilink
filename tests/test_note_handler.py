"""Tests for note handling operations."""

from datetime import datetime
from pathlib import Path

import pytest

from termilink.config import create_default_config
from termilink.models import Note, NoteFormat
from termilink.note_handler import (
    append_to_note,
    create_note_file,
    ensure_directory_exists,
    get_daily_note_path,
    list_recent_notes,
    read_note_file,
    write_note_file,
)


@pytest.fixture
def test_vault(tmp_path: Path) -> Path:
    """Create a test vault directory."""
    vault = tmp_path / "test_vault"
    vault.mkdir()
    return vault


@pytest.fixture
def test_config(test_vault: Path) -> object:
    """Create a test configuration."""
    return create_default_config(test_vault)


def test_ensure_directory_exists(tmp_path: Path) -> None:
    """Test directory creation."""
    nested_file = tmp_path / "a" / "b" / "c" / "test.txt"
    ensure_directory_exists(nested_file)

    assert nested_file.parent.exists()
    assert nested_file.parent.is_dir()


def test_read_write_note_file(tmp_path: Path) -> None:
    """Test reading and writing note files."""
    test_file = tmp_path / "test.md"
    content = "Test content"

    write_note_file(test_file, content)
    assert test_file.exists()

    read_content = read_note_file(test_file)
    assert read_content == content


def test_read_nonexistent_file(tmp_path: Path) -> None:
    """Test reading non-existent file."""
    content = read_note_file(tmp_path / "nonexistent.md")
    assert content == ""


def test_get_daily_note_path(test_config: object) -> None:
    """Test getting daily note path."""
    test_date = datetime(2024, 1, 15)
    daily_note = get_daily_note_path(test_config, test_date)

    expected_path = test_config.vault_path / "Daily Notes" / "2024-01-15.md"
    assert daily_note == expected_path


def test_append_to_note_new_daily(test_config: object) -> None:
    """Test appending to new daily note."""
    note = Note(
        content="First note",
        format_type=NoteFormat.BULLET,
        timestamp=datetime(2024, 1, 15, 14, 30),
        use_daily_note=True,
    )

    result_path = append_to_note(test_config, note)

    assert result_path.exists()
    content = read_note_file(result_path)

    # Should have frontmatter for new daily note
    assert "---" in content
    assert "date: 2024-01-15" in content
    assert "- 14:30 - First note" in content


def test_append_to_note_existing(test_config: object) -> None:
    """Test appending to existing note."""
    # Create initial note
    note1 = Note(
        content="First note",
        format_type=NoteFormat.BULLET,
        use_daily_note=True,
    )
    result_path = append_to_note(test_config, note1)

    # Append second note
    note2 = Note(
        content="Second note",
        format_type=NoteFormat.BULLET,
        use_daily_note=True,
    )
    append_to_note(test_config, note2)

    content = read_note_file(result_path)

    assert "First note" in content
    assert "Second note" in content


def test_append_to_specific_file(test_config: object) -> None:
    """Test appending to specific file."""
    note = Note(
        content="Test note",
        format_type=NoteFormat.PLAIN,
        target_file=Path("test.md"),
        use_daily_note=False,
    )

    result_path = append_to_note(test_config, note)

    assert result_path.name == "test.md"
    assert result_path.parent == test_config.vault_path
    assert result_path.exists()


def test_create_note_file(test_config: object) -> None:
    """Test creating new note file."""
    filename = "new-note"
    content = "Initial content"

    result_path = create_note_file(test_config, filename, content)

    assert result_path.exists()
    assert result_path.name == "new-note.md"

    file_content = read_note_file(result_path)
    assert "Initial content" in file_content
    assert "created:" in file_content


def test_create_note_file_with_subdirectory(test_config: object) -> None:
    """Test creating note file in subdirectory."""
    filename = "new-note"
    content = "Initial content"
    subdirectory = "Projects"

    result_path = create_note_file(test_config, filename, content, subdirectory)

    assert result_path.exists()
    assert result_path.parent.name == "Projects"
    assert result_path.name == "new-note.md"


def test_list_recent_notes(test_config: object) -> None:
    """Test listing recent notes."""
    # Create multiple notes
    for i in range(5):
        note = Note(content=f"Note {i}", use_daily_note=False)
        note.target_file = Path(f"note{i}.md")
        append_to_note(test_config, note)

    recent = list_recent_notes(test_config, limit=3)

    assert len(recent) == 3
    # Should be sorted by modification time
    for note_path in recent:
        assert note_path.exists()
        assert note_path.suffix == ".md"
