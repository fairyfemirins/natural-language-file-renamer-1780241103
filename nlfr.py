#!/usr/bin/env python3
"""
Natural Language File Renamer (nlfr)

A CLI tool to rename files using natural language expressions (e.g., "today's date + original name").
"""

import re
import click
from datetime import datetime
from pathlib import Path
from typing import List, Optional


def parse_natural_language(expression: str, original_name: str) -> str:
    """
    Parse a natural language expression and apply transformations to the original filename.
    
    Supported transformations:
    - "today's date": Insert today's date (YYYY-MM-DD).
    - "lowercase": Convert to lowercase.
    - "UPPERCASE": Convert to uppercase.
    - "TitleCase": Convert to title case.
    - "sequential": Add a sequential number (e.g., file_1.txt).
    - Regex: Replace patterns (e.g., "s/old/new/").
    
    Args:
        expression: Natural language expression (e.g., "today's date + original name").
        original_name: Original filename (without extension).
        
    Returns:
        Transformed filename.
    """
    transformed = original_name
    
    # Date transformation
    if "today's date" in expression:
        today = datetime.now().strftime("%Y-%m-%d")
        transformed = expression.replace("today's date", today).replace("original name", transformed)
    
    # Case transformations
    if "lowercase" in expression:
        transformed = transformed.lower()
    if "UPPERCASE" in expression:
        transformed = transformed.upper()
    if "TitleCase" in expression:
        transformed = transformed.title()
    
    # Regex replacement
    regex_match = re.search(r's/(.*?)/(.*?)/', expression)
    if regex_match:
        pattern, replacement = regex_match.groups()
        transformed = re.sub(pattern, replacement, transformed)
    
    return transformed


def rename_file(file_path: Path, expression: str, sequential_counter: Optional[int] = None) -> str:
    """
    Rename a single file using a natural language expression.
    
    Args:
        file_path: Path to the file.
        expression: Natural language expression.
        sequential_counter: Optional sequential number.
        
    Returns:
        New filename.
    """
    original_stem = file_path.stem
    extension = file_path.suffix
    
    new_stem = parse_natural_language(expression, original_stem)
    
    # Sequential numbering
    if sequential_counter is not None:
        new_stem = f"{new_stem}_{sequential_counter}"
    
    return f"{new_stem}{extension}"


@click.command()
@click.argument('expression', type=str)
@click.argument('files', type=click.Path(exists=True), nargs=-1)
@click.option('--dry-run', is_flag=True, help="Preview changes without renaming.")
@click.option('--recursive', is_flag=True, help="Rename files in subdirectories.")
@click.option('--sequential', is_flag=True, help="Add sequential numbers to filenames.")
def main(expression: str, files: List[str], dry_run: bool, recursive: bool, sequential: bool) -> None:
    """
    Rename files using natural language expressions.
    
    Example:
        nlfr "today's date + original name" *.txt
        nlfr --dry-run "lowercase" *.jpg
        nlfr --recursive "TitleCase" **/*.md
    """
    file_paths = []
    
    for file_pattern in files:
        path = Path(file_pattern)
        if recursive and path.is_dir():
            file_paths.extend(path.rglob("*"))
        else:
            file_paths.extend(path.parent.glob(path.name))
    
    sequential_counter = 1
    for file_path in file_paths:
        if file_path.is_file():
            new_name = rename_file(file_path, expression, sequential_counter if sequential else None)
            new_path = file_path.with_name(new_name)
            
            if dry_run:
                click.echo(f"Preview: {file_path.name} -> {new_name}")
            else:
                file_path.rename(new_path)
                click.echo(f"Renamed: {file_path.name} -> {new_name}")
            
            if sequential:
                sequential_counter += 1


if __name__ == '__main__':
    main()