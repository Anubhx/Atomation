import pytest
from pathlib import Path
from src.document_loader import LoadedDocument
from src.chunker import chunk_document, compute_sha256

def test_compute_sha256():
    h1 = compute_sha256("hello world")
    h2 = compute_sha256("hello world")
    h3 = compute_sha256("different text")
    assert h1 == h2
    assert h1 != h3

def test_chunk_document():
    doc = LoadedDocument(
        doc_id="test__doc",
        file_path=Path("/tmp/test.md"),
        rel_path="test.md",
        title="ERP Testing Guide",
        category="ERP",
        subcategory="Workflows",
        keywords=["ERP", "P2P"],
        audience=["QA"],
        difficulty="advanced",
        content="""# ERP Testing Guide

## 1. Procurement Section
This section covers purchase requisitions and approval hierarchies.

## 2. Inventory Section
This section covers goods receipt and warehouse stock validation.
""",
        raw_metadata={}
    )

    chunks = chunk_document(doc)
    assert len(chunks) >= 2
    assert any("Procurement Section" in c.section_heading for c in chunks)
    assert any("Inventory Section" in c.section_heading for c in chunks)
    assert all(c.content_hash != "" for c in chunks)
