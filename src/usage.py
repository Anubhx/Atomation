import json
import time
import logging
from pathlib import Path
from typing import Dict, Any
from src.config import CACHE_DIR

logger = logging.getLogger("usage")

class UsageTracker:
    def __init__(self, metrics_file: Path = CACHE_DIR / "usage_metrics.json"):
        self.metrics_file = metrics_file
        self.metrics: Dict[str, Any] = self._load_metrics()

    def _load_metrics(self) -> Dict[str, Any]:
        if self.metrics_file.exists():
            try:
                with open(self.metrics_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load usage metrics: {e}")
        return {
            "total_requests": 0,
            "gemini_requests": 0,
            "embedding_requests": 0,
            "cache_hits": 0,
            "local_answers": 0,
            "rag_searches": 0,
            "failed_requests": 0,
            "rate_limited_requests": 0,
            "last_reset": time.time()
        }

    def _save_metrics(self) -> None:
        try:
            with open(self.metrics_file, "w", encoding="utf-8") as f:
                json.dump(self.metrics, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save usage metrics: {e}")

    def log_request(self, req_type: str) -> None:
        self.metrics["total_requests"] += 1
        if req_type == "gemini":
            self.metrics["gemini_requests"] += 1
        elif req_type == "embedding":
            self.metrics["embedding_requests"] += 1
        elif req_type == "cache_hit":
            self.metrics["cache_hits"] += 1
        elif req_type == "local_answer":
            self.metrics["local_answers"] += 1
        elif req_type == "rag_search":
            self.metrics["rag_searches"] += 1
        elif req_type == "failed":
            self.metrics["failed_requests"] += 1
        elif req_type == "rate_limited":
            self.metrics["rate_limited_requests"] += 1
        self._save_metrics()

    def get_summary(self) -> Dict[str, Any]:
        return self.metrics.copy()

    def reset(self) -> None:
        self.metrics = {
            "total_requests": 0,
            "gemini_requests": 0,
            "embedding_requests": 0,
            "cache_hits": 0,
            "local_answers": 0,
            "rag_searches": 0,
            "failed_requests": 0,
            "rate_limited_requests": 0,
            "last_reset": time.time()
        }
        self._save_metrics()
