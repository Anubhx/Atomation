import json
import time
import logging
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from src.config import VECTOR_INDEX_DIR, DEFAULT_EMBEDDING_MODEL

logger = logging.getLogger("vector_store")

class VectorStore:
    def __init__(self, index_dir: Path = VECTOR_INDEX_DIR):
        self.index_dir = index_dir
        self.metadata_file = self.index_dir / "index_metadata.json"
        self.vectors_file = self.index_dir / "vectors.npy"
        
        self.chunks: List[Dict[str, Any]] = []
        self.vectors: Optional[np.ndarray] = None
        self.manifest: Dict[str, Any] = {}

    def is_built(self) -> bool:
        return self.metadata_file.exists() and self.vectors_file.exists()

    def build_from_chunks(
        self,
        chunks_with_vectors: List[Tuple[Dict[str, Any], List[float]]],
        embedding_model: str = DEFAULT_EMBEDDING_MODEL
    ) -> None:
        """Builds index from list of (chunk_dict, vector) tuples."""
        self.chunks = []
        vectors_list = []

        for chunk_dict, vec in chunks_with_vectors:
            self.chunks.append(chunk_dict)
            vectors_list.append(vec)

        if vectors_list:
            # Normalize vectors for cosine similarity
            mat = np.array(vectors_list, dtype=np.float32)
            norms = np.linalg.norm(mat, axis=1, keepdims=True)
            norms[norms == 0] = 1.0
            self.vectors = mat / norms
        else:
            self.vectors = np.empty((0, 768), dtype=np.float32)

        unique_docs = set(c["doc_id"] for c in self.chunks)
        self.manifest = {
            "total_chunks": len(self.chunks),
            "total_docs": len(unique_docs),
            "build_timestamp": time.time(),
            "embedding_model": embedding_model,
            "content_hashes": [c["content_hash"] for c in self.chunks]
        }

        self.save()

    def save(self) -> None:
        self.index_dir.mkdir(parents=True, exist_ok=True)
        data_to_save = {
            "manifest": self.manifest,
            "chunks": self.chunks
        }
        with open(self.metadata_file, "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, indent=2)

        if self.vectors is not None:
            np.save(self.vectors_file, self.vectors)

    def load(self) -> bool:
        if not self.is_built():
            return False

        try:
            with open(self.metadata_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.manifest = data.get("manifest", {})
                self.chunks = data.get("chunks", [])

            self.vectors = np.load(self.vectors_file)
            return True
        except Exception as e:
            logger.error(f"Failed to load vector store: {e}")
            return False

    def search(
        self,
        query_vector: List[float],
        top_k: int = 5,
        metadata_filter: Optional[Dict[str, Any]] = None,
        min_similarity: float = -1.0
    ) -> List[Tuple[Dict[str, Any], float]]:
        """
        Searches index for top_k most similar chunks using cosine similarity.
        Optionally applies metadata filters (e.g. category, doc_id, doc_type).
        """
        if self.vectors is None or len(self.chunks) == 0:
            return []

        q_vec = np.array(query_vector, dtype=np.float32)
        q_norm = np.linalg.norm(q_vec)
        if q_norm > 0:
            q_vec = q_vec / q_norm

        scores = np.dot(self.vectors, q_vec)

        # Sort indices by score descending
        sorted_indices = np.argsort(scores)[::-1]

        results = []
        for idx in sorted_indices:
            score = float(scores[idx])
            if score < min_similarity:
                continue

            chunk = self.chunks[idx]

            # Metadata filtering check
            if metadata_filter:
                match = True
                for k, v in metadata_filter.items():
                    if k in chunk:
                        if isinstance(v, list):
                            if chunk[k] not in v:
                                match = False
                                break
                        elif chunk[k] != v:
                            match = False
                            break
                if not match:
                    continue

            results.append((chunk, score))
            if len(results) >= top_k:
                break

        return results
