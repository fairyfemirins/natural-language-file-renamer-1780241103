import pytest
from datetime import datetime
from pathlib import Path
import shutil
from nlfr import parse_natural_language, rename_file


def setup_test_files():
    """Create test files in a temporary directory."""
    test_dir = Path("test_files")
    shutil.rmtree(test_dir, ignore_errors=True)
    test_dir.mkdir()
    
    (test_dir / "file1.txt").touch()
    (test_dir / "FILE2.TXT").touch()
    (test_dir / "old_name.md").touch()
    
    return test_dir


def teardown_test_files():
    """Remove test files."""
    shutil.rmtree("test_files", ignore_errors=True)


def test_parse_natural_language():
    """Test natural language parsing."""
    assert parse_natural_language("today's date + original name", "notes") == f"{datetime.now().strftime('%Y-%m-%d')} + notes"
    assert parse_natural_language("lowercase", "UPPERCASE") == "uppercase"
    assert parse_natural_language("UPPERCASE", "lowercase") == "LOWERCASE"
    assert parse_natural_language("TitleCase", "file name") == "File Name"
    assert parse_natural_language("s/old/new/", "old_name") == "new_name"


def test_rename_file():
    """Test file renaming."""
    test_dir = setup_test_files()
    file_path = test_dir / "file1.txt"
    
    # Test date transformation
    new_name = rename_file(file_path, "today's date + original name")
    assert new_name.startswith(f"{datetime.now().strftime('%Y-%m-%d')} + file1.txt")
    
    # Test sequential numbering
    new_name = rename_file(file_path, "sequential", sequential_counter=1)
    assert new_name == "file1_1.txt"
    
    teardown_test_files()


def test_cli_dry_run(capsys):
    """Test CLI dry run mode."""
    test_dir = setup_test_files()
    
    # Import and run CLI
    from nlfr import main
    from click.testing import CliRunner
    
    runner = CliRunner()
    result = runner.invoke(main, ["today's date + original name", "test_files/file1.txt", "--dry-run"])
    assert "Preview:" in result.output
    
    teardown_test_files()