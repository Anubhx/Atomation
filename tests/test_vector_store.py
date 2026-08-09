import pytest
import numpy as np
from pathlib import Path
from src.vector_store import VectorStore

def test_vector_store_build_and_search(tmp_path):
    store = VectorStore(index_dir=tmp_path)
    
    chunk1 = {
        "chunk_id": "c1",
        "doc_id": "d1",
        "title": "Playwright Locators",
        "category": "CHEAT_SHEETS",
        "section_heading": "Locators",
        "text": "page.get_by_role('button').click()",
        "content_hash": "h1",
        "rel_path": "playwright.md"
    }
    chunk2 = {
        "chunk_id": "c2",
        "doc_id": "d2",
        "title": "SQL Join",
        "category": "CHEAT_SHEETS",
        "section_heading": "Joins",
        "text": "SELECT * FROM orders INNER JOIN vendors ON...",
        "content_hash": "h2",
        "rel_path": "sql.md"
    }

    vec1 = [1.0, 0.0, 0.0]
    vec2 = [0.0, 1.0, 0.0]

    store.build_from_chunks([(chunk1, vec1), (chunk2, vec2)])
    assert store.is_built()

    # Search for vector close to vec1
    results = store.search(query_vector=[0.9, 0.1, 0.0], top_k=1)
    assert len(results) == 1
    assert results[0][0]["chunk_id"] == "c1"

    # Test metadata filter
    results_filtered = store.search(query_vector=[0.9, 0.1, 0.0], top_k=2, metadata_filter={"category": "CHEAT_SHEETS"})
    assert len(results_filtered) == 2
