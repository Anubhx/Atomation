import pytest
from src.cache import AnswerCache

def test_answer_cache_operations(tmp_path):
    cache_file = tmp_path / "answer_cache.json"
    cache = AnswerCache(cache_file=cache_file)

    # Set cache entry
    cache.set(
        query="What is get_by_role?",
        answer="Playwright locator syntax...",
        retrieved_doc_ids=["doc_1"],
        source_type="LOCAL",
        kb_version="v1"
    )

    # Normalized lookup test (ignores case & spaces)
    entry = cache.get("explain GET_BY_ROLE")  # Wait, normalize query trims punctuation and lowers
    entry_exact = cache.get("What is get_by_role?")
    assert entry_exact is not None
    assert entry_exact["answer"] == "Playwright locator syntax..."

    # Version mismatch test
    entry_v2 = cache.get("What is get_by_role?", current_kb_version="v2")
    assert entry_v2 is None
