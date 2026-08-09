import pytest
from src.router import IntentRouter, AnswerSource
from src.retrieval import Retriever
from src.vector_store import VectorStore
from src.embeddings import EmbeddingManager

def test_router_deterministic_fast_paths(tmp_path):
    store = VectorStore(index_dir=tmp_path)
    emb_mgr = EmbeddingManager()
    retriever = Retriever(vector_store=store, embedding_manager=emb_mgr)
    router = IntentRouter(retriever=retriever)

    # 1. Playwright get_by_role fast-path
    decision = router.route("What is Playwright get_by_role syntax?")
    assert decision.source == AnswerSource.LOCAL
    assert decision.rule_name == "playwright_get_by_role"
    assert "get_by_role" in decision.answer

    # 2. Strict mode fast-path
    decision_strict = router.route("How to fix Playwright strict mode error?")
    assert decision_strict.source == AnswerSource.LOCAL
    assert decision_strict.rule_name == "playwright_strict_mode"

    # 3. HTTP 404 fast-path
    decision_http = router.route("What is HTTP 404 meaning?")
    assert decision_http.source == AnswerSource.LOCAL
    assert decision_http.rule_name == "http_401_403_404"

    # 4. ERP 3-way match fast-path
    decision_erp = router.route("Explain 3-way match")
    assert decision_erp.source == AnswerSource.LOCAL
    assert decision_erp.rule_name == "erp_three_way_match_definition"
