# Natural Language File Renamer

**A CLI tool to rename files using natural language expressions (e.g., `"today's date + original name"`).**

## Features
- **Natural Language Parsing**: Use expressions like `"today's date + original name"` or `"lowercase + sequential"`.
- **Transformations**:
  - **Date**: Insert today's date (`YYYY-MM-DD`).
  - **Regex**: Replace patterns (e.g., `s/old/new/`).
  - **Case**: Convert to `lowercase`, `UPPERCASE`, or `TitleCase`.
  - **Sequential**: Add sequential numbers (e.g., `file_1.txt`, `file_2.txt`).
- **Dry Run**: Preview changes before applying.
- **Recursive**: Rename files in subdirectories.

## Note

This repository was published under `fairyfemirins/natural-language-file-renamer-1780241103` due to namespace restrictions in cron mode. See [TRANSFER.md](TRANSFER.md) for transfer instructions.

## Installation
```bash
pip install natural-language-file-renamer
```

## Usage
```bash
# Rename files in current directory
nlfr "today's date + original name" *.txt

# Dry run (preview changes)
nlfr --dry-run "lowercase + sequential" *.jpg

# Recursive rename
nlfr --recursive "TitleCase" **/*.md
```

## Examples
| Expression               | Original Name       | Renamed To               |
|--------------------------|---------------------|--------------------------|
| `"today's date + _ + original name"` | `notes.txt`         | `2026-05-31_notes.txt`   |
| `"lowercase"`          | `UPPERCASE.TXT`     | `uppercase.txt`          |
| `"sequential"`         | `file.txt`          | `file_1.txt`             |
| `"s/old/new/"`         | `old_name.txt`      | `new_name.txt`           |

## Technical Architecture
- **Language**: Python 3.10+
- **Dependencies**: `click`, `python-dateutil`
- **Testing**: `pytest`
- **CI/CD**: GitHub Actions

## License
MIT