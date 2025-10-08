"""CLI interface for termiLink."""

from datetime import datetime
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from termilink.config import create_default_config, load_config, save_config
from termilink.models import Config, Note, NoteFormat
from termilink.note_handler import (
    append_to_note,
    create_note_file,
    get_daily_note_path,
    list_recent_notes,
)

app = typer.Typer(
    name="termilink",
    help="CLI tool for taking notes in terminal and appending to Obsidian",
    add_completion=False,
)
console = Console()


def get_config_or_exit() -> Config:
    """Load config or exit with error message.

    Returns:
        Config object

    Raises:
        typer.Exit: If config not found or invalid
    """
    config = load_config()
    if config is None:
        console.print("[red]No configuration found. Run 'termilink config init' first.[/red]")
        raise typer.Exit(1)
    return config


@app.command()
def add(
    content: str = typer.Argument(..., help="Note content to add"),
    file: str | None = typer.Option(None, "--file", "-f", help="Target file name"),
    format_type: NoteFormat = typer.Option(
        NoteFormat.TIMESTAMP, "--format", "-F", help="Note format type"
    ),
    tags: list[str] | None = typer.Option(None, "--tag", "-t", help="Tags to add"),
    no_timestamp: bool = typer.Option(False, "--no-timestamp", help="Disable timestamp"),
    daily: bool = typer.Option(True, "--daily/--no-daily", help="Use daily note"),
) -> None:
    """Add a note to Obsidian."""
    config = get_config_or_exit()

    # Override config timestamp setting if flag is provided
    include_timestamp = config.include_timestamp and not no_timestamp

    note = Note(
        content=content,
        format_type=format_type,
        tags=tags or [],
        use_daily_note=daily and file is None,
        target_file=Path(file) if file else None,
    )

    # Temporarily override config for this note
    original_include_timestamp = config.include_timestamp
    config.include_timestamp = include_timestamp

    try:
        target_path = append_to_note(config, note)
        relative_path = target_path.relative_to(config.vault_path)

        console.print(
            Panel(
                f"[green]✓[/green] Note added to: [cyan]{relative_path}[/cyan]\n\n"
                f"[dim]{note.format_content(include_timestamp, config.timestamp_format)}[/dim]",
                title="Success",
                border_style="green",
            )
        )
    finally:
        config.include_timestamp = original_include_timestamp


@app.command()
def quick(
    content: str = typer.Argument(..., help="Note content to add quickly"),
) -> None:
    """Quickly add a note with default settings (alias for add with defaults)."""
    config = get_config_or_exit()

    note = Note(
        content=content,
        format_type=config.default_format,
        use_daily_note=True,
    )

    target_path = append_to_note(config, note)
    relative_path = target_path.relative_to(config.vault_path)

    console.print(f"[green]✓[/green] Added to {relative_path}")


@app.command()
def create(
    filename: str = typer.Argument(..., help="Name of note file to create"),
    content: str = typer.Argument(
        "", help="Initial content (optional, will prompt if not provided)"
    ),
    subdirectory: str | None = typer.Option(None, "--dir", "-d", help="Subdirectory in vault"),
) -> None:
    """Create a new note file in Obsidian vault."""
    config = get_config_or_exit()

    if not content:
        content = typer.prompt("Enter initial content (or press Enter to skip)", default="")

    target_path = create_note_file(config, filename, content, subdirectory)
    relative_path = target_path.relative_to(config.vault_path)

    console.print(
        Panel(
            f"[green]✓[/green] Created: [cyan]{relative_path}[/cyan]",
            title="Success",
            border_style="green",
        )
    )


@app.command()
def recent(
    limit: int = typer.Option(10, "--limit", "-l", help="Number of recent notes to show"),
) -> None:
    """List recently modified notes."""
    config = get_config_or_exit()

    notes = list_recent_notes(config, limit)

    if not notes:
        console.print("[yellow]No notes found in vault.[/yellow]")
        return

    table = Table(title=f"Recently Modified Notes (Top {limit})")
    table.add_column("File", style="cyan")
    table.add_column("Modified", style="dim")

    for note_path in notes:
        relative_path = note_path.relative_to(config.vault_path)
        modified_time = datetime.fromtimestamp(note_path.stat().st_mtime)
        modified_str = modified_time.strftime("%Y-%m-%d %H:%M")
        table.add_row(str(relative_path), modified_str)

    console.print(table)


@app.command()
def today() -> None:
    """Show path to today's daily note."""
    config = get_config_or_exit()
    daily_note = get_daily_note_path(config)
    relative_path = daily_note.relative_to(config.vault_path)

    exists_indicator = "✓" if daily_note.exists() else "✗"
    status = "exists" if daily_note.exists() else "not created yet"

    console.print(
        Panel(
            f"[cyan]{relative_path}[/cyan]\n\n"
            f"Status: [{('green' if daily_note.exists() else 'yellow')}]{exists_indicator} "
            f"{status}[/]",
            title="Today's Daily Note",
            border_style="blue",
        )
    )


config_app = typer.Typer(help="Configuration management commands")
app.add_typer(config_app, name="config")


@config_app.command("init")
def config_init(
    vault_path: str = typer.Argument(..., help="Path to Obsidian vault"),
    daily_notes_path: str = typer.Option("Daily Notes", help="Relative path to daily notes folder"),
    force: bool = typer.Option(False, "--force", help="Override existing config"),
) -> None:
    """Initialize termiLink configuration."""
    vault = Path(vault_path).expanduser().resolve()

    if not vault.exists():
        console.print(f"[red]Error: Vault path does not exist: {vault}[/red]")
        raise typer.Exit(1)

    if not vault.is_dir():
        console.print(f"[red]Error: Vault path is not a directory: {vault}[/red]")
        raise typer.Exit(1)

    existing_config = load_config()
    if existing_config and not force:
        console.print("[yellow]Configuration already exists. Use --force to override.[/yellow]")
        raise typer.Exit(1)

    config = create_default_config(vault)
    config.daily_notes_path = daily_notes_path

    config_path = save_config(config)

    console.print(
        Panel(
            f"[green]✓[/green] Configuration created at: [cyan]{config_path}[/cyan]\n\n"
            f"Vault: [cyan]{vault}[/cyan]\n"
            f"Daily Notes: [cyan]{daily_notes_path}[/cyan]",
            title="Configuration Initialized",
            border_style="green",
        )
    )


@config_app.command("show")
def config_show() -> None:
    """Show current configuration."""
    config = get_config_or_exit()

    table = Table(title="Current Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="white")

    table.add_row("Vault Path", str(config.vault_path))
    table.add_row("Daily Notes Path", config.daily_notes_path)
    table.add_row("Daily Note Format", config.daily_note_format)
    table.add_row("Default Format", config.default_format.value)
    table.add_row("Include Timestamp", "✓" if config.include_timestamp else "✗")
    table.add_row("Timestamp Format", config.timestamp_format)
    table.add_row("Append Newline", "✓" if config.append_newline else "✗")

    console.print(table)


@config_app.command("set-vault")
def config_set_vault(
    vault_path: str = typer.Argument(..., help="New path to Obsidian vault"),
) -> None:
    """Update vault path in configuration."""
    config = get_config_or_exit()

    vault = Path(vault_path).expanduser().resolve()

    if not vault.exists():
        console.print(f"[red]Error: Vault path does not exist: {vault}[/red]")
        raise typer.Exit(1)

    config.vault_path = vault
    save_config(config)

    console.print(f"[green]✓[/green] Vault path updated to: [cyan]{vault}[/cyan]")


if __name__ == "__main__":
    app()
