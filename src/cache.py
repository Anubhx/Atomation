import re
import json
import time
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from src.config import CACHE_DIR

logger = logging.getLogger("cache")

class AnswerCache:
    def __init__(self, cache_file: Path = CACHE_DIR / "answer_cache.json", ttl_seconds: float = 86400 * 7):
        self.cache_file = cache_file
        self.ttl_seconds = ttl_seconds
        self.cache: Dict[str, Dict[str, Any]] = self._load_cache()

    def _normalize_query(self, query: str) -> str:
        q = query.lower().strip()
        q = re.sub(r"[^\w\s]", "", q)
        q = re.sub(r"\s+", " ", q)
        return q

    def _load_cache(self) -> Dict[str, Dict[str, Any]]:
        if self.cache_file.exists():
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load answer cache: {e}")
        return {}

    def _save_cache(self) -> None:
        try:
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(self.cache, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save answer cache: {e}")

    def get(self, query: str, current_kb_version: str = "v1") -> Optional[Dict[str, Any]]:
        norm_q = self._normalize_query(query)
        if norm_q not in self.cache:
            return None

        entry = self.cache[norm_q]

        # Invalidate error responses from cache
        answer_text = entry.get("answer", "")
        if "Gemini API Error" in answer_text or "Request failed" in answer_text or answer_text.startswith("❌"):
            del self.cache[norm_q]
            self._save_cache()
            return None

        # Check KB version
        if entry.get("kb_version") != current_kb_version:
            return None

        # Check TTL
        if time.time() - entry.get("timestamp", 0) > self.ttl_seconds:
            return None

        return entry

    def set(
        self,
        query: str,
        answer: str,
        retrieved_doc_ids: List[str],
        source_type: str = "LOCAL",
        kb_version: str = "v1"
    ) -> None:
        # Never cache error responses
        if "Gemini API Error" in answer or "Request failed" in answer or answer.startswith("❌"):
            return

        norm_q = self._normalize_query(query)
        self.cache[norm_q] = {
            "query": query,
            "normalized_query": norm_q,
            "answer": answer,
            "retrieved_doc_ids": retrieved_doc_ids,
            "source_type": source_type,
            "timestamp": time.time(),
            "kb_version": kb_version
        }
        self._save_cache()

    def clear(self) -> None:
        self.cache = {}
        self._save_cache()
