# termiLink

A powerful CLI tool for taking notes in your terminal and seamlessly appending them to your Obsidian vault.

## Features

- 🚀 **Quick Note Taking** - Add notes instantly from your terminal
- 📅 **Daily Notes Support** - Automatic daily note creation and appending
- 🎨 **Multiple Formats** - Plain, timestamped, bullet, and task formats
- 🏷️ **Tag Support** - Add tags to organize your notes
- ⚙️ **Flexible Configuration** - Customize paths, formats, and timestamps
- 📝 **File Management** - Create new notes or append to existing ones
- 🔍 **Recent Notes** - View recently modified notes

## Installation

### From Source

```bash
# Clone the repository
git clone git@github.com:the-data-sherpa/termilink.git
cd termilink

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Using pip (once published)

```bash
pip install termilink
```

## Quick Start

### 1. Initialize Configuration

First, set up termiLink with your Obsidian vault path:

```bash
termilink config init /path/to/your/obsidian/vault
```

Or use the short alias:

```bash
tl config init ~/Documents/ObsidianVault
```

### 2. Add Your First Note

```bash
# Quick note with default settings
tl quick "This is my first note!"

# Add a formatted note
tl add "Important meeting notes" --format bullet --tag meeting

# Add a task
tl add "Review PR #123" --format task --tag work
```

## Usage

### Basic Commands

#### Quick Note

The fastest way to add a note:

```bash
tl quick "Your note here"
```

#### Add Note with Options

```bash
# Add with bullet format
tl add "Note content" --format bullet

# Add with tags
tl add "Note content" --tag work --tag important

# Add to specific file
tl add "Note content" --file "Project Notes.md"

# Add without timestamp
tl add "Note content" --no-timestamp
```

#### Create New Note

```bash
# Create a new note file
tl create "Meeting Notes" "Initial content here"

# Create in subdirectory
tl create "Project Ideas" --dir Projects
```

#### View Recent Notes

```bash
# Show 10 most recently modified notes
tl recent

# Show more notes
tl recent --limit 20
```

#### Today's Daily Note

```bash
# Show path to today's daily note
tl today
```

### Format Types

termiLink supports multiple note formats:

- **plain**: `14:30 Note content #tag`
- **timestamp**: `**14:30** - Note content #tag`
- **bullet**: `- 14:30 - Note content #tag`
- **task**: `- [ ] 14:30 - Note content #tag`

### Configuration Commands

#### Show Current Configuration

```bash
tl config show
```

#### Update Vault Path

```bash
tl config set-vault /new/path/to/vault
```

#### Initialize with Custom Settings

```bash
tl config init ~/vault --daily-notes-path "Journal"
```

## Configuration

Configuration is stored in YAML format at one of these locations:

- `~/.termilink.yaml`
- `~/.config/termilink/config.yaml`
- `./.termilink.yaml` (current directory)

### Example Configuration

```yaml
vault_path: /Users/username/Documents/ObsidianVault
daily_notes_path: Daily Notes
daily_note_format: "%Y-%m-%d"
default_format: timestamp
include_timestamp: true
timestamp_format: "%H:%M"
append_newline: true
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `vault_path` | string | - | Path to Obsidian vault (required) |
| `daily_notes_path` | string | `Daily Notes` | Relative path to daily notes folder |
| `daily_note_format` | string | `%Y-%m-%d` | Date format for daily note filenames |
| `default_format` | string | `timestamp` | Default note format |
| `include_timestamp` | boolean | `true` | Include timestamp in notes |
| `timestamp_format` | string | `%H:%M` | Format for timestamps |
| `append_newline` | boolean | `true` | Add newline before appending |

## Examples

### Daily Workflow

```bash
# Morning - add meeting notes
tl add "Team standup at 9am" --format task --tag meeting

# During work - quick thoughts
tl quick "Great idea for new feature"

# End of day - review what you worked on
tl recent --limit 5
```

### Project Notes

```bash
# Create project note
tl create "Project Alpha" "# Project Alpha\n\nGoals and objectives" --dir Projects

# Add updates throughout the day
tl add "Completed user authentication" --file "Projects/Project Alpha.md"
tl add "Started API integration" --file "Projects/Project Alpha.md"
```

### Tagged Notes

```bash
# Work notes
tl add "Reviewed codebase" --tag work --tag review

# Personal notes
tl add "Book recommendation: Thinking Fast and Slow" --tag personal --tag books

# Quick ideas
tl add "New blog post idea" --tag ideas --tag blog
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone git@github.com:the-data-sherpa/termilink.git
cd termilink

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies including dev tools
pip install -r requirements.txt
pip install -e ".[dev]"
```

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=termilink --cov-report=term-missing

# Run specific test file
pytest tests/test_note_handler.py
```

### Code Quality

```bash
# Format code
black termilink tests

# Lint code
ruff check termilink tests

# Type checking
mypy termilink
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- Built with [Typer](https://typer.tiangolo.com/) for CLI interface
- [Rich](https://rich.readthedocs.io/) for beautiful terminal output
- [Pydantic](https://docs.pydantic.dev/) for data validation
- Inspired by the [Obsidian](https://obsidian.md/) note-taking app

