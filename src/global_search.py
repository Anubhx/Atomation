import re
from pathlib import Path
from typing import Dict, Any, List
from src.config import BASE_DIR
from src.document_loader import load_all_knowledge_documents
from src.code_browser import list_code_files

class GlobalSearchResult:
    def __init__(
        self,
        category: str,  # "Documentation", "Code", "Tests", "SQL", "Templates"
        title: str,
        path: str,
        snippet: str,
        match_type: str
    ):
        self.category = category
        self.title = title
        self.path = path
        self.snippet = snippet
        self.match_type = match_type

    def to_dict(self) -> Dict[str, Any]:
        return {
            "category": self.category,
            "title": self.title,
            "path": self.path,
            "snippet": self.snippet,
            "match_type": self.match_type
        }

def perform_global_search(query: str) -> Dict[str, List[GlobalSearchResult]]:
    """Performs global search across documentation and code files."""
    q_terms = [t.lower() for t in re.findall(r"\w+", query) if len(t) > 1]
    if not q_terms:
        return {
            "📚 Documentation": [],
            "💻 Code": [],
            "🧪 Tests": [],
            "🗄 SQL": [],
            "📋 Templates": []
        }

    grouped_results: Dict[str, List[GlobalSearchResult]] = {
        "📚 Documentation": [],
        "💻 Code": [],
        "🧪 Tests": [],
        "🗄 SQL": [],
        "📋 Templates": []
    }

    # 1. Search Knowledge Base Markdown Documents
    docs = load_all_knowledge_documents()
    for doc in docs:
        combined = (doc.title + " " + doc.rel_path + " " + " ".join(doc.keywords) + " " + doc.content).lower()
        if all(term in combined for term in q_terms):
            # Categorize
            if "25_TEMPLATES" in doc.rel_path:
                cat_key = "📋 Templates"
            else:
                cat_key = "📚 Documentation"

            # Snippet extraction
            snippet = ""
            for line in doc.content.splitlines():
                if any(term in line.lower() for term in q_terms):
                    snippet = line.strip()[:150]
                    break
            if not snippet:
                snippet = doc.content[:150].replace("\n", " ")

            grouped_results[cat_key].append(GlobalSearchResult(
                category=cat_key,
                title=doc.title,
                path=doc.rel_path,
                snippet=snippet,
                match_type="Markdown & Metadata"
            ))

    # 2. Search Code Files
    code_files = list_code_files(BASE_DIR)
    for code in code_files:
        try:
            content = Path(code["path"]).read_text(encoding="utf-8")
        except Exception:
            continue

        combined = (code["filename"] + " " + code["rel_path"] + " " + content).lower()
        if all(term in combined for term in q_terms):
            # Categorize
            rel = code["rel_path"].lower()
            if "test" in rel:
                cat_key = "🧪 Tests"
            elif code["extension"] == ".sql":
                cat_key = "🗄 SQL"
            else:
                cat_key = "💻 Code"

            # Snippet
            snippet = ""
            for line in content.splitlines():
                if any(term in line.lower() for term in q_terms):
                    snippet = line.strip()[:150]
                    break
            if not snippet:
                snippet = content[:150].replace("\n", " ")

            grouped_results[cat_key].append(GlobalSearchResult(
                category=cat_key,
                title=code["filename"],
                path=code["rel_path"],
                snippet=snippet,
                match_type="Code Content"
            ))

    return grouped_results
