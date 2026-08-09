import pytest
from pathlib import Path
from src.config import is_path_safe, BASE_DIR
from src.file_browser import read_markdown_document, save_personal_note

def test_path_traversal_prevention():
    # Attempt path traversal out of allowed roots
    bad_path1 = BASE_DIR / ".." / ".." / "etc" / "passwd"
    bad_path2 = BASE_DIR / ".env"
    bad_path3 = BASE_DIR / ".streamlit" / "secrets.toml"

    assert is_path_safe(bad_path1) is False
    assert is_path_safe(bad_path2) is False

    # Verify read_markdown_document rejects forbidden files
    res = read_markdown_document(bad_path3)
    assert res is None

    # Verify save_personal_note rejects saving outside personal/
    ok, msg = save_personal_note(bad_path3, "hacked")
    assert ok is False
    assert "Access denied" in msg
