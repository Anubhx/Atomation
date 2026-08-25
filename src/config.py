import os
from pathlib import Path
from typing import List, Dict, Any, Optional

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
except ImportError:
    pass

BASE_DIR = Path(__file__).resolve().parent.parent

# Knowledge Base Directories
NOTES_DIR = BASE_DIR / "notes"
PERSONAL_DIR = BASE_DIR / "personal"
PROJECT_NOTES_DIR = BASE_DIR / "project_notes"

# Data Directories
DATA_DIR = BASE_DIR / "data"
VECTOR_INDEX_DIR = DATA_DIR / "vector_index"
CACHE_DIR = DATA_DIR / "cache"

# Ensure runtime data directories exist
VECTOR_INDEX_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)
PERSONAL_DIR.mkdir(parents=True, exist_ok=True)
PROJECT_NOTES_DIR.mkdir(parents=True, exist_ok=True)

# Security: Allowed root directories for file browser (relative to BASE_DIR or absolute resolved)
ALLOWED_ROOT_NAMES = [
    "notes",
    "personal",
    "project_notes",
    "automation",
    "tests",
    "pages",
    "api",
    "utils"
]

# Model Configuration
DEFAULT_GENERATION_MODEL = "gemini-3.5-flash-lite"
DEFAULT_EMBEDDING_MODEL = "text-embedding-004"

# RAG & LLM Settings
DEFAULT_TOP_K = 5
DEFAULT_TEMPERATURE = 0.2
MAX_RETRIES = 3
LOCAL_ONLY_DEFAULT = False

def get_allowed_roots() -> List[Path]:
    """Returns absolute Path objects for allowed directory roots."""
    roots = []
    for name in ALLOWED_ROOT_NAMES:
        path = (BASE_DIR / name).resolve()
        roots.append(path)
    return roots

def is_path_safe(path: Path) -> bool:
    """Verifies that a given path is within one of the allowed roots and prevents path traversal."""
    try:
        resolved = path.resolve()
    except Exception:
        return False
    
    allowed = get_allowed_roots()
    for root in allowed:
        if root.exists():
            try:
                resolved.relative_to(root)
                return True
            except ValueError:
                continue
    return False

def get_gemini_keys() -> List[str]:
    """
    Safely retrieves Gemini API keys from Streamlit secrets or environment variables.
    Supports key pool format:
    [gemini]
    keys = ["KEY1", "KEY2"]
    or GEMINI_API_KEY env var.
    """
    keys = []
    
    # Check Streamlit secrets if available
    try:
        import streamlit as st
        if hasattr(st, "secrets") and st.secrets is not None:
            if "gemini" in st.secrets:
                gemini_sec = st.secrets["gemini"]
                if "keys" in gemini_sec:
                    raw_keys = gemini_sec["keys"]
                    if isinstance(raw_keys, list):
                        keys.extend([str(k).strip() for k in raw_keys if k])
                    elif isinstance(raw_keys, str):
                        keys.append(raw_keys.strip())
                elif "api_key" in gemini_sec:
                    keys.append(str(gemini_sec["api_key"]).strip())
            elif "GEMINI_API_KEY" in st.secrets:
                keys.append(str(st.secrets["GEMINI_API_KEY"]).strip())
    except Exception:
        pass

    # Fallback to environment variables if no keys found from st.secrets
    if not keys:
        env_key = os.getenv("GEMINI_API_KEY")
        if env_key:
            keys.append(env_key.strip())
        env_keys = os.getenv("GEMINI_API_KEYS")
        if env_keys:
            keys.extend([k.strip() for k in env_keys.split(",") if k.strip()])

    # Deduplicate while preserving order
    seen = set()
    deduped = []
    for k in keys:
        if k and k not in seen:
            seen.add(k)
            deduped.append(k)

    return deduped
