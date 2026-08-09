import os
import shutil
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from src.config import NOTES_DIR, PERSONAL_DIR, PROJECT_NOTES_DIR, is_path_safe
from src.document_loader import parse_frontmatter

def get_directory_tree(root_dir: Path) -> Dict[str, Any]:
    """Generates recursive directory structure for knowledge base browsing."""
    tree: Dict[str, Any] = {"name": root_dir.name, "type": "folder", "path": str(root_dir), "children": []}
    if not root_dir.exists():
        return tree

    try:
        for entry in sorted(root_dir.iterdir(), key=lambda x: (not x.is_dir(), x.name)):
            if entry.name.startswith((".", "__pycache__")):
                continue
            if entry.is_dir():
                tree["children"].append(get_directory_tree(entry))
            elif entry.suffix.lower() in [".md", ".markdown"]:
                tree["children"].append({
                    "name": entry.name,
                    "type": "file",
                    "path": str(entry),
                    "size": entry.stat().st_size
                })
    except Exception:
        pass

    return tree

def read_markdown_document(file_path: Path) -> Optional[Dict[str, Any]]:
    """Reads a Markdown document with frontmatter and security path validation."""
    if not is_path_safe(file_path):
        return None

    try:
        content = file_path.read_text(encoding="utf-8")
        metadata, body = parse_frontmatter(content)
        return {
            "file_path": str(file_path),
            "filename": file_path.name,
            "raw_content": content,
            "body": body,
            "metadata": metadata,
            "size_bytes": file_path.stat().st_size,
            "is_personal": str(PERSONAL_DIR) in str(file_path)
        }
    except Exception:
        return None

def save_personal_note(file_path: Path, new_content: str) -> Tuple[bool, str]:
    """Safely saves edited personal notes with automatic backup creation."""
    if not is_path_safe(file_path) or str(PERSONAL_DIR) not in str(file_path.resolve()):
        return False, "Access denied: Can only edit files inside personal/ directory."

    try:
        # Create backup if file already exists
        if file_path.exists():
            backup_path = file_path.with_suffix(f".bak_{int(time.time())}.md")
            shutil.copy2(file_path, backup_path)

        file_path.write_text(new_content, encoding="utf-8")
        return True, "Personal note saved successfully."
    except Exception as e:
        return False, f"Failed to save personal note: {e}"
