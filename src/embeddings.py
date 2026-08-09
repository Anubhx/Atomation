import json
import logging
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional
from src.config import CACHE_DIR, DEFAULT_EMBEDDING_MODEL
from src.key_pool import KeyPool

logger = logging.getLogger("embeddings")

class EmbeddingManager:
    def __init__(self, key_pool: Optional[KeyPool] = None, model_name: str = DEFAULT_EMBEDDING_MODEL):
        self.key_pool = key_pool or KeyPool()
        self.model_name = model_name
        self.cache_file = CACHE_DIR / "embedding_cache.json"
        self.cache: Dict[str, List[float]] = self._load_cache()

    def _load_cache(self) -> Dict[str, List[float]]:
        if self.cache_file.exists():
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load embedding cache: {e}")
        return {}

    def _save_cache(self) -> None:
        try:
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(self.cache, f)
        except Exception as e:
            logger.error(f"Failed to save embedding cache: {e}")

    def _get_cache_key(self, content_hash: str) -> str:
        return f"{self.model_name}__{content_hash}"

    def get_embedding(self, text: str, content_hash: str) -> List[float]:
        """
        Retrieves embedding for text.
        First checks local cache. If cached, returns cached vector without calling Gemini API!
        """
        cache_key = self._get_cache_key(content_hash)
        if cache_key in self.cache:
            return self.cache[cache_key]

        # Call Gemini Embedding API if KeyPool has active key
        vector = self._generate_gemini_embedding(text)
        if vector is not None:
            self.cache[cache_key] = vector
            self._save_cache()
            return vector

        # Deterministic fallback vector if API unavailable or offline
        vector = self._generate_fallback_vector(text)
        self.cache[cache_key] = vector
        self._save_cache()
        return vector

    def _generate_gemini_embedding(self, text: str) -> Optional[List[float]]:
        if not self.key_pool.has_keys:
            return None

        slot = self.key_pool.get_available_key()
        if not slot:
            return None

        try:
            from google import genai
            client = genai.Client(api_key=slot.key_str)
            response = client.models.embed_content(
                model=self.model_name,
                contents=text
            )
            if hasattr(response, "embedding") and response.embedding:
                self.key_pool.mark_healthy(slot.slot_id)
                if hasattr(response.embedding, "values"):
                    return list(response.embedding.values)
                elif isinstance(response.embedding, list):
                    return response.embedding
            elif hasattr(response, "embeddings") and response.embeddings:
                emb = response.embeddings[0]
                self.key_pool.mark_healthy(slot.slot_id)
                if hasattr(emb, "values"):
                    return list(emb.values)
                elif isinstance(emb, list):
                    return emb
        except Exception as e:
            err_msg = str(e)
            if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg or "quota" in err_msg.lower():
                self.key_pool.mark_rate_limited(slot.slot_id)
            else:
                self.key_pool.mark_failed(slot.slot_id)
            logger.warning(f"Embedding API call failed on {slot.get_masked_name()}: {e}")

        return None

    def _generate_fallback_vector(self, text: str, dim: int = 768) -> List[float]:
        """Generates a deterministic normalized pseudo-embedding using char hashing for local offline operation."""
        v = np.zeros(dim, dtype=np.float32)
        words = text.lower().split()
        for idx, word in enumerate(words):
            h = int(np.frombuffer(word.encode("utf-8"), dtype=np.uint8).sum())
            dim_idx = h % dim
            v[dim_idx] += 1.0 / (idx + 1.0)
        norm = np.linalg.norm(v)
        if norm > 0:
            v = v / norm
        return v.tolist()
