# termiLink Architecture

## Overview

termiLink is a CLI tool that bridges the gap between terminal-based note-taking and Obsidian knowledge management. It's designed with modularity, type safety, and ease of use in mind.

## Design Principles

1. **Functional & Declarative**: Following Python/FastAPI best practices with minimal class usage
2. **Type-Safe**: Full type hints with Pydantic v2 for validation
3. **Modular**: Clear separation of concerns across modules
4. **User-Friendly**: Beautiful terminal UI with Rich
5. **Tested**: Comprehensive test coverage (95%+ on core modules)

## Project Structure

```
termiLink/
├── termilink/              # Main package
│   ├── __init__.py        # Package initialization
│   ├── models.py          # Data models (Config, Note, NoteFormat)
│   ├── config.py          # Configuration management
│   ├── note_handler.py    # Core note operations
│   └── cli.py             # CLI interface (Typer)
├── tests/                 # Test suite
│   ├── test_models.py     # Model tests
│   ├── test_config.py     # Config tests
│   └── test_note_handler.py  # Note handler tests
├── docs/                  # Documentation
├── pyproject.toml        # Project metadata & dependencies
├── requirements.txt      # Package requirements
├── README.md            # Full documentation
├── QUICKSTART.md        # Quick start guide
└── LICENSE              # MIT License
```

## Module Breakdown

### models.py

**Purpose**: Data models and validation

**Key Components**:
- `NoteFormat`: Enum for note format types (plain, timestamp, bullet, task)
- `Config`: Configuration model with validation
- `Note`: Note model with formatting logic

**Key Features**:
- Pydantic v2 models for validation
- Smart format_content() method for different note styles
- Path validation for vault location

### config.py

**Purpose**: Configuration file management

**Key Components**:
- `find_config_file()`: Search for config in standard locations
- `load_config()`: Load and validate config from YAML/JSON
- `save_config()`: Persist configuration
- `create_default_config()`: Generate default settings

**Key Features**:
- Multiple config locations support
- YAML and JSON format support
- Validation on load

### note_handler.py

**Purpose**: Core note operations

**Key Components**:
- `get_daily_note_path()`: Calculate daily note path
- `append_to_note()`: Add content to notes
- `create_note_file()`: Create new note files
- `list_recent_notes()`: Find recent notes
- File I/O utilities

**Key Features**:
- Daily note support with frontmatter
- Automatic directory creation
- Safe file operations
- Recent notes tracking

### cli.py

**Purpose**: Command-line interface

**Key Components**:
- `add`: Add notes with options
- `quick`: Fast note addition
- `create`: Create new note files
- `recent`: View recent notes
- `today`: Show daily note path
- `config`: Configuration subcommands

**Key Features**:
- Typer-based CLI framework
- Rich terminal UI
- Command aliases (tl, termilink)
- Comprehensive help text

## Data Flow

### Adding a Note

```
User Command (CLI)
    ↓
Parse Arguments (Typer)
    ↓
Load Config (config.py)
    ↓
Create Note Model (models.py)
    ↓
Format Content (models.py)
    ↓
Append to File (note_handler.py)
    ↓
Display Success (Rich UI)
```

### Configuration Flow

```
User Command (config init)
    ↓
Validate Vault Path
    ↓
Create Config Model
    ↓
Save to YAML (~/.termilink.yaml)
    ↓
Display Confirmation
```

## Note Formatting

The tool supports four format types:

1. **Plain**: `14:30 Note content #tag`
2. **Timestamp**: `**14:30** - Note content #tag`
3. **Bullet**: `- 14:30 - Note content #tag`
4. **Task**: `- [ ] 14:30 - Note content #tag`

Formatting is handled by `Note.format_content()` with pattern matching for clean, maintainable code.

## Configuration Management

### Config Locations (Priority Order)

1. `~/.termilink.yaml`
2. `~/.config/termilink/config.yaml`
3. `./.termilink.yaml` (current directory)

### Config Schema

```yaml
vault_path: string         # Path to Obsidian vault (required)
daily_notes_path: string   # Relative path to daily notes
daily_note_format: string  # strftime format for filenames
default_format: string     # Default note format
include_timestamp: bool    # Include timestamps
timestamp_format: string   # strftime format for timestamps
append_newline: bool       # Add newline before appending
```

## Testing Strategy

### Test Coverage

- **Models**: 95% coverage - Format logic, validation
- **Config**: 86% coverage - Save, load, validation
- **Note Handler**: 95% coverage - File operations, note creation
- **CLI**: 0% coverage - Requires integration tests (future work)

### Test Approach

- Unit tests for all core functions
- Pytest fixtures for test data
- Temporary directories for file operations
- Edge case coverage (invalid paths, missing files)

## Dependencies

### Core Dependencies

- **Typer**: CLI framework with type hints
- **Pydantic v2**: Data validation and settings
- **Rich**: Beautiful terminal output
- **PyYAML**: YAML configuration support
- **python-dateutil**: Enhanced date handling

### Dev Dependencies

- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting
- **black**: Code formatting
- **ruff**: Fast linting
- **mypy**: Type checking

## Extension Points

The architecture is designed for future enhancements:

1. **Template Support**: Add template system for note creation
2. **Search**: Implement full-text search across vault
3. **Sync**: Cloud sync for config
4. **Plugins**: Plugin system for custom formats
5. **Interactive Mode**: TUI for browsing/editing notes
6. **AI Integration**: Smart tagging and categorization

## Performance Considerations

- **File I/O**: Minimal reads/writes, append-only for notes
- **Lazy Loading**: Config loaded once per command
- **Type Checking**: Validation happens at boundaries
- **Caching**: Recent notes uses filesystem metadata

## Security Considerations

- **Path Validation**: All paths validated and sanitized
- **Vault Containment**: Notes must be within vault
- **No Remote Code**: Pure data operations
- **Config Permissions**: Standard user file permissions

## Error Handling

- **Early Returns**: Guard clauses for preconditions
- **Type Safety**: Pydantic validation prevents invalid data
- **User Feedback**: Clear error messages via Rich
- **Graceful Degradation**: Missing config prompts initialization

## Future Roadmap

### v0.2.0
- Interactive TUI mode
- Template system
- Search functionality

### v0.3.0
- Plugin architecture
- Cloud sync
- Mobile companion app

### v1.0.0
- AI-powered features
- Multi-vault support
- Team collaboration features

