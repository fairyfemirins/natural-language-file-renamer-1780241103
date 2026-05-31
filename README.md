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

## Why?
- **Demand**: Recurring requests for natural language file renaming tools (confirmed via `web_search`).
- **Novelty**: No open-source Python CLI tool exists (only Node.js or regex-based alternatives).
- **Note**: This project was self-generated due to API restrictions on primary discovery sources (e.g., Reddit).

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