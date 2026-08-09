import pytest
from pathlib import Path
from src.document_loader import parse_frontmatter, load_single_markdown_file, load_all_knowledge_documents
from src.config import NOTES_DIR

def test_parse_frontmatter():
    content = """---
title: Test Title
category: ERP
keywords:
  - P2P
  - Approval
---
# Main Heading
Body text goes here.
"""
    meta, body = parse_frontmatter(content)
    assert meta["title"] == "Test Title"
    assert meta["category"] == "ERP"
    assert "P2P" in meta["keywords"]
    assert "# Main Heading" in body

def test_load_single_markdown_file():
    from src.config import PERSONAL_DIR
    doc_path = PERSONAL_DIR / "test_doc_sample.md"
    doc_path.write_text("""---
title: Sample Note
category: TESTING
keywords: qa, pytest
---
# Sample Title
This is sample content.
""", encoding="utf-8")

    try:
        doc = load_single_markdown_file(doc_path, PERSONAL_DIR)
        assert doc is not None
        assert doc.title == "Sample Note"
        assert doc.category == "TESTING"
        assert "qa" in doc.keywords
    finally:
        if doc_path.exists():
            doc_path.unlink()

def test_load_all_knowledge_documents():
    docs = load_all_knowledge_documents()
    assert len(docs) > 0
    assert any(d.category == "03_ERP_TESTING" for d in docs)
