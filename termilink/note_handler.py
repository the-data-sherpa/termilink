"""Core note handling operations for termiLink."""

from datetime import datetime
from pathlib import Path

from termilink.models import Config, Note


def get_daily_note_path(config: Config, date: datetime | None = None) -> Path:
    """Get path to daily note file.

    Args:
        config: Configuration object
        date: Date for daily note. Uses today if None.

    Returns:
        Path to daily note file
    """
    if date is None:
        date = datetime.now()

    filename = date.strftime(config.daily_note_format) + ".md"
    daily_notes_dir = config.vault_path / config.daily_notes_path
    return daily_notes_dir / filename


def ensure_directory_exists(file_path: Path) -> None:
    """Ensure directory for file path exists.

    Args:
        file_path: Path to file
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)


def read_note_file(file_path: Path) -> str:
    """Read content from note file.

    Args:
        file_path: Path to note file

    Returns:
        File content or empty string if file doesn't exist
    """
    if not file_path.exists():
        return ""

    with open(file_path, encoding="utf-8") as f:
        return f.read()


def write_note_file(file_path: Path, content: str) -> None:
    """Write content to note file.

    Args:
        file_path: Path to note file
        content: Content to write
    """
    ensure_directory_exists(file_path)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)


def append_to_note(
    config: Config,
    note: Note,
    target_path: Path | None = None,
) -> Path:
    """Append note to file.

    Args:
        config: Configuration object
        note: Note to append
        target_path: Optional specific path to append to. Uses daily note if None.

    Returns:
        Path to file that was modified
    """
    if target_path is None:
        if note.use_daily_note:
            target_path = get_daily_note_path(config)
        elif note.target_file:
            target_path = config.vault_path / note.target_file
        else:
            target_path = get_daily_note_path(config)

    # Ensure target path is within vault
    if not str(target_path.resolve()).startswith(str(config.vault_path.resolve())):
        target_path = config.vault_path / target_path.name

    # Read existing content
    existing_content = read_note_file(target_path)

    # Format new note
    formatted_note = note.format_content(
        include_timestamp=config.include_timestamp,
        timestamp_format=config.timestamp_format,
    )

    # Build new content
    if existing_content:
        if config.append_newline:
            new_content = f"{existing_content}\n{formatted_note}\n"
        else:
            new_content = f"{existing_content}{formatted_note}\n"
    else:
        # Create new file with frontmatter for daily notes
        if note.use_daily_note and note.timestamp:
            date_str = note.timestamp.strftime("%Y-%m-%d")
            frontmatter = f"---\ndate: {date_str}\n---\n\n"
            new_content = f"{frontmatter}{formatted_note}\n"
        else:
            new_content = f"{formatted_note}\n"

    # Write updated content
    write_note_file(target_path, new_content)

    return target_path


def create_note_file(
    config: Config,
    filename: str,
    content: str,
    subdirectory: str | None = None,
) -> Path:
    """Create a new note file.

    Args:
        config: Configuration object
        filename: Name of file to create (without .md extension)
        content: Initial content
        subdirectory: Optional subdirectory within vault

    Returns:
        Path to created file
    """
    if not filename.endswith(".md"):
        filename = f"{filename}.md"

    if subdirectory:
        target_path = config.vault_path / subdirectory / filename
    else:
        target_path = config.vault_path / filename

    ensure_directory_exists(target_path)

    # Add basic frontmatter
    frontmatter = f"---\ncreated: {datetime.now().isoformat()}\n---\n\n"
    full_content = f"{frontmatter}{content}\n"

    write_note_file(target_path, full_content)

    return target_path


def list_recent_notes(config: Config, limit: int = 10) -> list[Path]:
    """List recently modified notes in vault.

    Args:
        config: Configuration object
        limit: Maximum number of notes to return

    Returns:
        List of paths to recent notes
    """
    md_files = list(config.vault_path.rglob("*.md"))

    # Sort by modification time, most recent first
    md_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)

    return md_files[:limit]
