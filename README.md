# Natural Language File Renamer (nlrename)

A CLI tool to batch-rename files using natural language expressions.

## Features
- **Date Transformations**: `"today's date + original name"` → `2026-05-31_original.jpg`
- **Regex Substitutions**: `"replace 'DSC' with 'Vacation'"` → `Vacation_001.jpg`
- **Case Transformations**: `"lowercase"` → `original.txt` (from `ORIGINAL.TXT`)
- **Sequential Numbering**: `"sequential"` → `file_1.jpg`, `file_2.jpg`

## Installation
```bash
pip install -r requirements.txt
chmod +x nlrename.py
```

## Usage
```bash
# Rename all .jpg files with today's date
./nlrename.py "today's date + original name" *.jpg

# Replace 'DSC' with 'Vacation' in all .jpg files
./nlrename.py "replace 'DSC' with 'Vacation'" *.jpg

# Convert all .TXT files to lowercase
./nlrename.py "lowercase" *.TXT

# Convert all .txt files to title case
./nlrename.py "title case" *.txt

# Rename files sequentially
./nlrename.py "sequential" *.jpg
```

## Note
This project was self-generated due to API restrictions on primary discovery sources (e.g., Reddit).

This repository was published under `fairyfemirins/natural-language-file-renamer-1780239235` due to namespace restrictions in cron mode. See [TRANSFER.md](TRANSFER.md) for transfer instructions.

## License
MIT