import re
import logging
from typing import List, Dict, Any, Optional, Tuple
from src.vector_store import VectorStore
from src.embeddings import EmbeddingManager
from src.chunker import compute_sha256

logger = logging.getLogger("retrieval")

class Retriever:
    def __init__(self, vector_store: VectorStore, embedding_manager: EmbeddingManager):
        self.vector_store = vector_store
        self.embedding_manager = embedding_manager

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        target_doc_id: Optional[str] = None,
        category_filter: Optional[str] = None,
        prefer_project_notes: bool = False
    ) -> List[Tuple[Dict[str, Any], float]]:
        """
        Performs hybrid retrieval combining keyword matching, metadata filtering,
        and vector similarity search.
        """
        if not self.vector_store.is_built() and not self.vector_store.chunks:
            self.vector_store.load()

        if not self.vector_store.chunks:
            return []

        # 1. Prepare query embedding
        query_hash = compute_sha256(query)
        query_vector = self.embedding_manager.get_embedding(query, query_hash)

        # 2. Prepare metadata filter
        meta_filter: Dict[str, Any] = {}
        if target_doc_id:
            meta_filter["doc_id"] = target_doc_id
        elif category_filter:
            meta_filter["category"] = category_filter

        # 3. Perform vector search (fetch top_k * 3 for hybrid reranking)
        candidates = self.vector_store.search(
            query_vector=query_vector,
            top_k=max(top_k * 3, 15),
            metadata_filter=meta_filter if meta_filter else None
        )

        # 4. Keyword boost & hybrid scoring
        query_terms = set(re.findall(r"\w+", query.lower()))
        reranked: List[Tuple[Dict[str, Any], float]] = []

        for chunk, v_score in candidates:
            k_score = 0.0
            chunk_text_lower = chunk["text"].lower()
            title_lower = chunk["title"].lower()
            heading_lower = chunk["section_heading"].lower()
            keywords_lower = [k.lower() for k in chunk.get("keywords", [])]

            # Matching term frequency
            for term in query_terms:
                if len(term) <= 2:
                    continue
                if term in heading_lower:
                    k_score += 0.3
                if term in title_lower:
                    k_score += 0.2
                if any(term in kw for kw in keywords_lower):
                    k_score += 0.25
                if term in chunk_text_lower:
                    k_score += 0.1

            # Project notes preference boost if flagged
            project_boost = 0.2 if prefer_project_notes and chunk.get("doc_type") == "project" else 0.0

            # Combined score: 60% vector + 30% keyword + 10% project boost
            combined_score = (0.6 * v_score) + (0.3 * min(k_score, 1.0)) + project_boost
            reranked.append((chunk, combined_score))

        # Sort by combined score descending
        reranked.sort(key=lambda x: x[1], reverse=True)
        return reranked[:top_k]
