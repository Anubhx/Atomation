import os
import re
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional
from src.config import NOTES_DIR, PERSONAL_DIR, PROJECT_NOTES_DIR, is_path_safe

class LoadedDocument:
    def __init__(
        self,
        doc_id: str,
        file_path: Path,
        rel_path: str,
        title: str,
        category: str,
        subcategory: str,
        keywords: List[str],
        audience: List[str],
        difficulty: str,
        content: str,
        raw_metadata: Dict[str, Any],
        doc_type: str = "general"
    ):
        self.doc_id = doc_id
        self.file_path = file_path
        self.rel_path = rel_path
        self.title = title
        self.category = category
        self.subcategory = subcategory
        self.keywords = keywords
        self.audience = audience
        self.difficulty = difficulty
        self.content = content
        self.raw_metadata = raw_metadata
        self.doc_type = doc_type

def parse_frontmatter(file_content: str) -> tuple[Dict[str, Any], str]:
    """Extracts YAML frontmatter and body from Markdown content."""
    pattern = r"^---\s*\n(.*?)\n---\s*\n"
    match = re.search(pattern, file_content, re.DOTALL)
    if match:
        yaml_text = match.group(1)
        body = file_content[match.end():]
        try:
            metadata = yaml.safe_load(yaml_text) or {}
            if isinstance(metadata, dict):
                return metadata, body
        except Exception:
            pass
    return {}, file_content

def load_single_markdown_file(file_path: Path, base_dir: Path, doc_type: str = "general") -> Optional[LoadedDocument]:
    """Loads a single Markdown document and parses its frontmatter and body."""
    if not file_path.is_file() or file_path.suffix.lower() not in [".md", ".markdown"]:
        return None

    if not is_path_safe(file_path):
        return None

    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception:
        return None

    metadata, body = parse_frontmatter(content)

    # Relative path calculation
    try:
        rel_path = str(file_path.relative_to(base_dir.parent if base_dir.name in ["notes", "personal", "project_notes"] else base_dir))
    except Exception:
        rel_path = str(file_path)

    # Fallback title extraction from first H1 header or filename
    title = metadata.get("title")
    if not title:
        h1_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
        if h1_match:
            title = h1_match.group(1).strip()
        else:
            title = file_path.stem.replace("_", " ").replace("-", " ").title()

    category = str(metadata.get("category", file_path.parent.name))
    subcategory = str(metadata.get("subcategory", ""))

    raw_keywords = metadata.get("keywords", [])
    if isinstance(raw_keywords, str):
        keywords = [k.strip() for k in raw_keywords.split(",") if k.strip()]
    elif isinstance(raw_keywords, list):
        keywords = [str(k).strip() for k in raw_keywords if k]
    else:
        keywords = []

    raw_audience = metadata.get("audience", [])
    if isinstance(raw_audience, str):
        audience = [a.strip() for a in raw_audience.split(",") if a.strip()]
    elif isinstance(raw_audience, list):
        audience = [str(a).strip() for a in raw_audience if a]
    else:
        audience = []

    difficulty = str(metadata.get("difficulty", "intermediate"))
    doc_id = rel_path.replace("\\", "/").replace("/", "__")

    return LoadedDocument(
        doc_id=doc_id,
        file_path=file_path,
        rel_path=rel_path,
        title=title,
        category=category,
        subcategory=subcategory,
        keywords=keywords,
        audience=audience,
        difficulty=difficulty,
        content=body,
        raw_metadata=metadata,
        doc_type=doc_type
    )

def load_all_knowledge_documents() -> List[LoadedDocument]:
    """Scans notes/, project_notes/, and personal/ directories for markdown files."""
    docs: List[LoadedDocument] = []
    
    # 1. Main Knowledge Base notes/
    if NOTES_DIR.exists():
        for root, _, files in os.walk(NOTES_DIR):
            for file in sorted(files):
                if file.endswith((".md", ".markdown")):
                    p = Path(root) / file
                    doc = load_single_markdown_file(p, NOTES_DIR.parent, doc_type="general")
                    if doc:
                        docs.append(doc)

    # 2. Project Notes project_notes/
    if PROJECT_NOTES_DIR.exists():
        for root, _, files in os.walk(PROJECT_NOTES_DIR):
            for file in sorted(files):
                if file.endswith((".md", ".markdown")) and file != "README.md":
                    p = Path(root) / file
                    doc = load_single_markdown_file(p, PROJECT_NOTES_DIR.parent, doc_type="project")
                    if doc:
                        docs.append(doc)

    # 3. Personal Notes personal/
    if PERSONAL_DIR.exists():
        for root, _, files in os.walk(PERSONAL_DIR):
            for file in sorted(files):
                if file.endswith((".md", ".markdown")) and file != "README.md":
                    p = Path(root) / file
                    doc = load_single_markdown_file(p, PERSONAL_DIR.parent, doc_type="personal")
                    if doc:
                        docs.append(doc)

    return docs
