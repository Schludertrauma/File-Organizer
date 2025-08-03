'''Test for fileorganizer class'''

import os
import sys
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # noqa: E402
from file_organizer import fileorganizer


@pytest.fixture
def organizer():
    """Fixture to create an instance of fileorganizer."""
    return fileorganizer()


def test_welcome_message(capsys, organizer):
    """Test the welcome message output."""
    organizer.welcome_message()
    captured = capsys.readouterr()
    assert "Welcome to the File Organizer!" in captured.out
    assert "This script will help you organize files in a specified directory by their extensions." in captured.out


def test_add_directory(organizer, capsys):
    """Test adding a directory that does not exist."""
    organizer.add_directory("non_existent_directory")
    captured = capsys.readouterr()
    assert "The directory non_existent_directory does not exist." in captured.out


def test_scan_directory(organizer, tmp_path):
    """Test scanning a directory."""
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()
    (test_dir / "file1.txt").touch()
    (test_dir / "file2.jpg").touch()

    files = organizer.scan_directory(str(test_dir))
    assert len(files) == 2
    assert "file1.txt" in files
    assert "file2.jpg" in files


def test_sort_files_by_extension(organizer):
    """Test sorting files by their extensions."""
    files = ["image1.jpg", "document1.txt",
             "audio1.mp3", "video1.mp4", "unknown.xyz"]
    sorted_files = organizer.sort_files_by_extension(files)

    assert len(sorted_files['images']) == 1
    assert "image1.jpg" in sorted_files['images']

    assert len(sorted_files['documents']) == 1
    assert "document1.txt" in sorted_files['documents']

    assert len(sorted_files['audio']) == 1
    assert "audio1.mp3" in sorted_files['audio']

    assert len(sorted_files['video']) == 1
    assert "video1.mp4" in sorted_files['video']

    assert len(sorted_files['others']) == 1
    assert "unknown.xyz" in sorted_files['others']


def test_organize_files(organizer, tmp_path):
    """Test the complete file organization process."""
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()
    (test_dir / "image1.jpg").touch()
    (test_dir / "document1.txt").touch()
    (test_dir / "audio1.mp3").touch()
    (test_dir / "video1.mp4").touch()
    (test_dir / "unknown.xyz").touch()

    files = organizer.scan_directory(str(test_dir))
    sorted_files = organizer.sort_files_by_extension(files)

    assert len(sorted_files['images']) == 1
    assert len(sorted_files['documents']) == 1
    assert len(sorted_files['audio']) == 1
    assert len(sorted_files['video']) == 1
    assert len(sorted_files['others']) == 1


def test_end_message(capsys, organizer):
    """Test the end message output."""
    # Create a dummy sorted_files for the argument
    sorted_files = {
        'images': ['image1.jpg'],
        'documents': ['document1.txt'],
        'audio': ['audio1.mp3'],
        'video': ['video1.mp4'],
        'others': ['unknown.xyz']
    }
    organizer.end_message(sorted_files)
    captured = capsys.readouterr()
    assert "File organization complete." in captured.out
    assert "Thank you for using the File Organizer!" in captured.out


def test_run(organizer, capsys):
    """Test the run method of the file organizer."""
    # Mock input to avoid OSError
    import builtins
    original_input = builtins.input
    builtins.input = lambda _: "test_dir"
    try:
        organizer.run()
        captured = capsys.readouterr()
        assert "Welcome to the File Organizer" in captured.out
        assert "This script will help you organize files in a specified directory by their extensions." in captured.out
        assert "File organization complete." in captured.out
        assert "Thank you for using the File Organizer!" in captured.out
    finally:
        builtins.input = original_input
