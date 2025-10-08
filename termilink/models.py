"""Data models for termiLink configuration and notes."""

from datetime import datetime
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, Field, field_validator


class NoteFormat(str, Enum):
    """Supported note format types."""

    PLAIN = "plain"
    TIMESTAMP = "timestamp"
    BULLET = "bullet"
    TASK = "task"


class Config(BaseModel):
    """Configuration model for termiLink."""

    vault_path: Path = Field(..., description="Path to Obsidian vault")
    daily_notes_path: str = Field(
        default="Daily Notes", description="Relative path to daily notes folder"
    )
    daily_note_format: str = Field(
        default="%Y-%m-%d", description="Date format for daily note filenames"
    )
    default_format: NoteFormat = Field(
        default=NoteFormat.TIMESTAMP, description="Default note format"
    )
    include_timestamp: bool = Field(
        default=True, description="Include timestamp in notes by default"
    )
    timestamp_format: str = Field(default="%H:%M", description="Format for timestamps in notes")
    append_newline: bool = Field(default=True, description="Add newline before appending note")

    @field_validator("vault_path")
    @classmethod
    def validate_vault_path(cls, v: Path) -> Path:
        """Validate that vault path exists."""
        if not v.exists():
            raise ValueError(f"Vault path does not exist: {v}")
        if not v.is_dir():
            raise ValueError(f"Vault path is not a directory: {v}")
        return v.resolve()


class Note(BaseModel):
    """Model representing a note to be added."""

    content: str = Field(..., description="Note content")
    format_type: NoteFormat = Field(
        default=NoteFormat.TIMESTAMP, description="Format type for note"
    )
    tags: list[str] = Field(default_factory=list, description="Tags to include")
    timestamp: datetime | None = Field(
        default_factory=datetime.now, description="Timestamp for note"
    )
    target_file: Path | None = Field(default=None, description="Target file path")
    use_daily_note: bool = Field(default=True, description="Use daily note")

    def format_content(
        self, include_timestamp: bool = True, timestamp_format: str = "%H:%M"
    ) -> str:
        """Format note content based on format type.

        Args:
            include_timestamp: Whether to include timestamp
            timestamp_format: Format string for timestamp

        Returns:
            Formatted note content
        """
        timestamp_str = ""
        if include_timestamp and self.timestamp:
            timestamp_str = self.timestamp.strftime(timestamp_format)

        tags_str = " ".join(f"#{tag}" for tag in self.tags) if self.tags else ""

        match self.format_type:
            case NoteFormat.PLAIN:
                parts = [part for part in [timestamp_str, self.content, tags_str] if part]
                return " ".join(parts)

            case NoteFormat.TIMESTAMP:
                if timestamp_str:
                    parts = [f"**{timestamp_str}**", self.content]
                    if tags_str:
                        parts.append(tags_str)
                    return " - ".join(parts)
                return self.content

            case NoteFormat.BULLET:
                parts = [timestamp_str, self.content] if timestamp_str else [self.content]
                result = "- " + " - ".join(parts)
                if tags_str:
                    result += f" {tags_str}"
                return result

            case NoteFormat.TASK:
                parts = [timestamp_str, self.content] if timestamp_str else [self.content]
                result = "- [ ] " + " - ".join(parts)
                if tags_str:
                    result += f" {tags_str}"
                return result

        return self.content
