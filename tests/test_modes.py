import pytest
from src.answer_modes import ModeHandler
from src.router import IntentRouter
from src.retrieval import Retriever
from src.vector_store import VectorStore
from src.embeddings import EmbeddingManager
from src.llm import GeminiClient

def test_quiz_mode_local(tmp_path):
    store = VectorStore(index_dir=tmp_path)
    emb_mgr = EmbeddingManager()
    retriever = Retriever(vector_store=store, embedding_manager=emb_mgr)
    router = IntentRouter(retriever=retriever)
    llm = GeminiClient(local_only=True)

    handler = ModeHandler(router=router, llm_client=llm)
    res = handler.execute_study_quiz("3-Way Match")
    assert "3-Way Match" in res["answer"]
    assert res["used_gemini"] is False
