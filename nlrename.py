#!/usr/bin/env python3
"""
Natural Language File Renamer (nlrename)

A CLI tool to batch-rename files using natural language expressions.
Supports:
- Date transformations (e.g., "today's date + original name")
- Regex substitutions (e.g., "replace 'DSC' with 'Vacation'")
- Case transformations (e.g., "lowercase", "title case")
- Sequential numbering (e.g., "sequential")

Usage:
  nlrename.py "<expression>" <files>...

Examples:
  nlrename.py "today's date + original name" *.jpg
  nlrename.py "replace 'DSC' with 'Vacation'" *.jpg
  nlrename.py "lowercase" *.TXT
  nlrename.py "title case" *.txt
  nlrename.py "sequential" *.jpg
"""

import os
import re
import sys
from datetime import datetime
from pathlib import Path

import click
from dateutil.relativedelta import relativedelta


@click.command()
@click.argument("expression", type=str)
@click.argument("files", type=click.Path(exists=True), nargs=-1)
def cli(expression: str, files: tuple) -> None:
    """Rename files using natural language expressions."""
    if not files:
        click.echo("Error: No files provided.", err=True)
        sys.exit(1)
    
    # Parse expression
    try:
        transformer = parse_expression(expression)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    
    # Apply transformation
    for i, file_path in enumerate(files):
        try:
            new_name = transformer(Path(file_path).name, i)
            if new_name == Path(file_path).name:
                continue  # Skip if no change
            
            new_path = Path(file_path).with_name(new_name)
            if new_path.exists():
                click.echo(f"Warning: {new_path} already exists. Skipping.", err=True)
                continue
            
            Path(file_path).rename(new_path)
            click.echo(f"Renamed: {file_path} -> {new_path}")
        except Exception as e:
            click.echo(f"Error renaming {file_path}: {e}", err=True)


def parse_expression(expression: str) -> callable:
    """Parse natural language expression into a transformer function."""
    expression = expression.lower().strip()
    
    # Date transformations
    if "today's date" in expression:
        date_format = "%Y-%m-%d"
        if "+" in expression:
            # Check if the offset is valid (e.g., "1 day")
            offset_part = expression.split("+")[1].strip()
            if any(unit in offset_part for unit in ["day", "week", "month", "year"]):
                offset = parse_offset(offset_part)
                today = datetime.now() + offset
            else:
                today = datetime.now()
        else:
            today = datetime.now()
        date_str = today.strftime(date_format)
        
        if "original name" in expression:
            return lambda name, _: f"{date_str}_{name}"
        else:
            return lambda name, _: f"{date_str}_{Path(name).stem}{Path(name).suffix}"
    
    # Regex substitutions
    elif "replace" in expression and "with" in expression:
        pattern = expression.split("replace")[1].split("with")[0].strip().strip("'\"")
        replacement = expression.split("with")[1].strip().strip("'\"")
        return lambda name, _: name.replace(pattern, replacement)
    
    # Case transformations
    elif expression == "lowercase":
        return lambda name, _: name.lower()
    elif expression == "uppercase":
        return lambda name, _: name.upper()
    elif expression == "title case":
        return lambda name, _: name.title()
    
    # Sequential numbering
    elif expression == "sequential":
        return lambda name, i: f"{Path(name).stem}_{i+1}{Path(name).suffix}"
    
    # Default: prepend/append expression
    else:
        if "original name" in expression:
            return lambda name, _: f"{expression.replace('original name', name)}"
        else:
            return lambda name, _: f"{expression}_{name}"


def parse_offset(offset_str: str) -> relativedelta:
    """Parse offset string (e.g., "1 day", "2 weeks") into relativedelta."""
    offset_str = offset_str.strip()
    match = re.search(r"\d+", offset_str)
    if not match:
        raise ValueError(f"No numeric value in offset: {offset_str}")
    value = int(match.group())
    
    if "day" in offset_str:
        return relativedelta(days=value)
    elif "week" in offset_str:
        return relativedelta(weeks=value)
    elif "month" in offset_str:
        return relativedelta(months=value)
    elif "year" in offset_str:
        return relativedelta(years=value)
    else:
        raise ValueError(f"Unsupported offset: {offset_str}")


if __name__ == "__main__":
    cli()