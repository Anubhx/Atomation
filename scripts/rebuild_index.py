#!/usr/bin/env python3
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.config import CACHE_DIR, VECTOR_INDEX_DIR

def main():
    print("🧹 Cleaning existing vector index and embedding cache...")
    index_meta = VECTOR_INDEX_DIR / "index_metadata.json"
    index_vecs = VECTOR_INDEX_DIR / "vectors.npy"
    cache_file = CACHE_DIR / "embedding_cache.json"

    if index_meta.exists():
        index_meta.unlink()
    if index_vecs.exists():
        index_vecs.unlink()
    if cache_file.exists():
        cache_file.unlink()

    print("✅ Existing index cleared. Triggering full build...")
    from scripts.build_index import main as build_main
    build_main()

if __name__ == "__main__":
    main()
