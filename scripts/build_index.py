#!/usr/bin/env python3
import sys
import time
from pathlib import Path

# Ensure project root is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.document_loader import load_all_knowledge_documents
from src.chunker import chunk_document
from src.embeddings import EmbeddingManager
from src.vector_store import VectorStore

def main():
    print("🚀 Starting QE Copilot Vector Index Build...")
    start_time = time.time()

    print("📄 Loading knowledge base markdown documents...")
    documents = load_all_knowledge_documents()
    print(f"✅ Loaded {len(documents)} documents across notes/, project_notes/, personal/.")

    print("✂️ Chunking documents semantically...")
    all_chunks = []
    for doc in documents:
        chunks = chunk_document(doc)
        all_chunks.extend(chunks)

    print(f"✅ Generated {len(all_chunks)} semantic chunks.")

    print("⚡ Generating/Retrieving embeddings (using content-hash deduplication cache)...")
    embedding_manager = EmbeddingManager()
    chunks_with_vectors = []

    cached_count = 0
    new_count = 0

    for idx, chunk in enumerate(all_chunks, start=1):
        c_hash = chunk.content_hash
        cache_key = embedding_manager._get_cache_key(c_hash)
        if cache_key in embedding_manager.cache:
            cached_count += 1
        else:
            new_count += 1

        vec = embedding_manager.get_embedding(chunk.text, c_hash)
        chunks_with_vectors.append((chunk.to_dict(), vec))

        if idx % 20 == 0 or idx == len(all_chunks):
            print(f"   Processed {idx}/{len(all_chunks)} chunks (Cached: {cached_count}, New: {new_count})...")

    print("💾 Saving vector index and manifest...")
    vector_store = VectorStore()
    vector_store.build_from_chunks(chunks_with_vectors)

    elapsed = time.time() - start_time
    print(f"🎉 Index Build Complete in {elapsed:.2f}s!")
    print(f"📊 Summary: {len(documents)} documents, {len(all_chunks)} chunks indexed.")
    print(f"   Cache Hits: {cached_count} | New API Embeddings: {new_count}")

if __name__ == "__main__":
    main()
