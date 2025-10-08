# termiLink Quick Start Guide

## Installation

### Step 1: Set up virtual environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows
```

### Step 2: Install termiLink

```bash
# Install in development mode
pip install -e .

# Or install from PyPI (when published)
pip install termilink
```

## Initial Configuration

### Configure your Obsidian vault

```bash
tl config init /path/to/your/obsidian/vault
```

Example:
```bash
tl config init ~/Documents/MyVault
```

### Verify configuration

```bash
tl config show
```

## Basic Usage

### Quick note (fastest method)

```bash
tl quick "This is a quick note"
```

### Add formatted notes

```bash
# Bullet point
tl add "Meeting with team" --format bullet --tag meeting

# Task item
tl add "Review PR #123" --format task --tag work

# With multiple tags
tl add "New project idea" --tag ideas --tag project --tag urgent
```

### Create new note files

```bash
# Create a new note
tl create "Project Planning" "Initial thoughts and goals"

# Create in a subdirectory
tl create "Sprint Retrospective" --dir "Projects/TeamAlpha"
```

### View recent notes

```bash
# Show 10 most recent
tl recent

# Show more
tl recent --limit 20
```

### Check today's daily note

```bash
tl today
```

## Common Workflows

### Daily journaling

```bash
# Morning
tl quick "Started working on feature X"

# Throughout the day
tl add "Completed task Y" --format task
tl add "Meeting notes" --tag meeting

# End of day
tl today  # View today's note location
```

### Project tracking

```bash
# Create project note
tl create "Project Alpha" --dir Projects

# Add updates
tl add "Milestone 1 completed" --file "Projects/Project Alpha.md"
```

### Task management

```bash
# Add tasks
tl add "Write documentation" --format task --tag todo
tl add "Review code" --format task --tag urgent
```

## Tips

1. **Use aliases**: Both `tl` and `termilink` work
2. **Tab completion**: Use shell tab completion for file paths
3. **Multiple tags**: Add as many `--tag` flags as needed
4. **Quick daily notes**: `tl quick` is perfect for fast logging
5. **Custom formats**: Check `tl add --help` for all options

## Troubleshooting

### Config not found

```bash
# Re-initialize config
tl config init /path/to/vault --force
```

### Update vault path

```bash
tl config set-vault /new/vault/path
```

### View current settings

```bash
tl config show
```

## Next Steps

- Customize your config file at `~/.termilink.yaml`
- Create shell aliases for common workflows
- Integrate with your daily routine
- Explore format options with `tl add --help`

For full documentation, see [README.md](README.md)

