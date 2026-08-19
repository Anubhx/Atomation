# QE Copilot - Private Personal RAG QA & ERP Testing Assistant

**QE Copilot** is a private, fast, personal Quality Engineering and ERP Testing assistant built on top of your existing local `notes/` knowledge base (90+ structured Markdown documents across 26 modules).

> 🌐 **Live Web Application**: [https://qe-copilot.streamlit.app](https://qe-copilot.streamlit.app)  
> 💻 **Local Development UI**: [http://localhost:8501](http://localhost:8501)

---

## 🌟 Key Architecture & Highlights

- **Two-Layer Answer System**:
  - **Layer 1 (Local Deterministic Fast-Path)**: Answers common Playwright locator queries, HTTP status codes, SQL JOIN syntax, Pytest fixtures, Git commands, and ERP 3-way match rules instantly (<1s) without calling the Gemini API.
  - **Layer 2 (RAG + Gemini)**: Combines intelligent semantic Markdown chunking, content-hash deduplication embedding cache, hybrid vector + keyword retrieval, and the official `google-genai` SDK for complex synthesis.
- **Configurable Personal KeyPool**:
  - Manages multiple Gemini API key slots safely.
  - Handles rate limits (429) with exponential backoff and automatic cooldowns.
  - **Zero Security Exposure**: Logical key slots (e.g. `Key Slot #1`) are logged/displayed; raw API key strings are never logged, printed, or sent to the client.
- **Content-Hash Embedding Cache**:
  - Computes SHA256 hashes of Markdown chunks.
  - Rebuilding the vector index skips API calls for unchanged documents, making re-indexing cost-effective.
- **Built-in Knowledge Base & Code Browser**:
  - Browse all 89+ Markdown notes and project code files directly within Streamlit.
  - Code + Document Linking automatically pairs code files with relevant QA guides.
  - Interactive "Explain this file", "Ask about this file", and "Review this code" (GOOD / IMPROVE / PROBLEM) features.
- **Privacy First & Local-Only Mode**:
  - Supports optional `LOCAL_ONLY = true` mode to completely disable Gemini API calls and query local knowledge offline.

---

## 📁 Project Directory Structure

```
Atomation/
├── app.py                      # Main Streamlit application
├── conftest.py                 # Pytest root path configuration
├── requirements.txt            # Python dependencies
├── README.md                   # Setup & architecture guide
├── plan.md                     # Project specification
├── .gitignore                  # Git ignore rules
├── .streamlit/
│   ├── config.toml             # Streamlit dark theme & layout config
│   └── secrets.toml.example    # Example secrets configuration
│
├── notes/                      # Main QA & ERP Knowledge Base (89 docs)
├── project_notes/              # Project-specific notes (architecture, glossary, roles)
├── personal/                   # Personal notes (editable from Streamlit)
│
├── src/
│   ├── config.py               # Path safety & model configuration
│   ├── document_loader.py      # Frontmatter parser & document loader
│   ├── chunker.py              # Semantic markdown chunker & SHA256 hashing
│   ├── embeddings.py           # Google GenAI embedding manager & cache
│   ├── vector_store.py         # NumPy cosine similarity vector index
│   ├── retrieval.py            # Hybrid keyword + vector retriever
│   ├── cache.py                # Local normalized query answer cache
│   ├── router.py               # Intent router (Local vs RAG+Gemini)
│   ├── key_pool.py             # Safe Gemini key pool rotator
│   ├── llm.py                  # GeminiClient with backoff & retry
│   ├── prompts.py              # System personas & mode templates
│   ├── answer_modes.py         # Specialized mode handlers (Ask, Test Gen, SQL, etc.)
│   ├── citations.py            # Markdown source citation formatter
│   ├── file_browser.py         # Safe markdown file browser & editor
│   ├── code_browser.py         # Code browser & code-doc linking
│   ├── global_search.py        # Search across docs, code, tests, SQL, templates
│   ├── workspace.py            # My Workspace pin manager
│   └── usage.py                # Local cost & usage metrics tracker
│
├── scripts/
│   ├── build_index.py          # Vector index build script
│   └── rebuild_index.py        # Full index clear & rebuild script
│
├── data/
│   ├── vector_index/           # Serialized index & manifest
│   └── cache/                  # Embedding cache & answer cache
│
└── tests/                      # Pytest unit test suite
    ├── test_loader.py
    ├── test_chunker.py
    ├── test_vector_store.py
    ├── test_router.py
    ├── test_key_pool.py
    ├── test_cache.py
    ├── test_modes.py
    └── test_security.py
```

---

## 🛠️ Quick Setup & Installation

### 1. Environment Setup
```bash
# Navigate to project directory
cd /Users/anubhav/Downloads/Atomation

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Gemini API Secrets
Copy the secrets template to `.streamlit/secrets.toml`:
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Edit `.streamlit/secrets.toml`:
```toml
[gemini]
keys = [
    "YOUR_GEMINI_API_KEY_1",
    "YOUR_GEMINI_API_KEY_2"
]

[settings]
generation_model = "gemini-2.5-flash-lite"
embedding_model = "text-embedding-004"
top_k = 5
temperature = 0.2
local_only = false
```

---

## ⚙️ Building the Vector Index

Run `build_index.py` to process the 89+ Markdown notes, extract YAML metadata, chunk content, generate embeddings (cached), and save the vector store:

```bash
python scripts/build_index.py
```

To force clean and rebuild the index from scratch:
```bash
python scripts/rebuild_index.py
```

---

## 🚀 Running the Streamlit Application Locally

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`.

---

## 🧪 Running the Pytest Test Suite

Run all unit tests (offline mocks):
```bash
pytest tests/
```

---

## ☁️ Streamlit Community Cloud Deployment

1. Push your repository to GitHub (ensure `.streamlit/secrets.toml` is in `.gitignore`).
2. Log into [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click **New App**, select your repo, branch (`main`), and main file (`app.py`).
4. Under **Advanced Settings > Secrets**, paste your key configuration:
   ```toml
   [gemini]
   keys = [
       "YOUR_GEMINI_API_KEY_1"
   ]
   ```
5. Click **Deploy**.

---

## ❓ Example Questions to Try

- **ERP 3-Way Match**: `"How do I test a 3-way match?"` (Answered locally <1s!)
- **Playwright Locators**: `"What is Playwright get_by_role syntax?"` (Answered locally <1s!)
- **ERP Purchase Order**: `"What should I test for a purchase order approval workflow?"`
- **Playwright Strict Mode**: `"What does this Playwright strict mode error mean?"`
- **SQL Verification**: `"Which SQL query can verify this transaction?"`
- **RBAC Risk**: `"What should I test when a buyer cannot approve their own PO?"`

---

## ⚠️ Known Limitations

1. **Local-Only Vector Math**: Uses NumPy cosine similarity, ideal for knowledge bases up to ~50,000 chunks. For massive million-vector scale, FAISS/ChromaDB can be swapped in `src/vector_store.py`.
2. **Personal File Editing**: Editing is strictly limited to files in `personal/` for data safety. `notes/` is read-only.
