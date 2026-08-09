import os
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from src.config import BASE_DIR, is_path_safe

SUPPORTED_CODE_EXTENSIONS = {".py", ".sql", ".yaml", ".yml", ".json", ".js", ".ts", ".tsx", ".sh", ".toml", ".ini"}
SENSITIVE_FILES = {"secrets.toml", ".env", "id_rsa", "credentials", "private_key"}

# Code to Document Linking Rules
CODE_LINKING_RULES = [
    {
        "keywords": ["purchase_order", "po_", "p2p", "procure"],
        "related_docs": [
            "notes/03_ERP_TESTING/03_procure_to_pay_p2p_workflow.md",
            "notes/03_ERP_TESTING/08_rbac_security_and_sod_testing.md",
            "notes/21_CHEAT_SHEETS/cheat-sheet-erp.md"
        ]
    },
    {
        "keywords": ["playwright", "locator", "page.", "click", "get_by_"],
        "related_docs": [
            "notes/21_CHEAT_SHEETS/cheat-sheet-playwright.md",
            "notes/22_TROUBLESHOOTING/troubleshooting-playwright.md",
            "notes/08_PLAYWRIGHT/01_playwright_python_architecture.md"
        ]
    },
    {
        "keywords": ["pytest", "fixture", "conftest", "assert"],
        "related_docs": [
            "notes/21_CHEAT_SHEETS/cheat-sheet-pytest.md",
            "notes/09_PYTHON_PYTEST/01_pytest_enterprise_framework.md"
        ]
    },
    {
        "keywords": ["sql", "select", "join", "where", "group by"],
        "related_docs": [
            "notes/21_CHEAT_SHEETS/cheat-sheet-sql.md",
            "notes/07_DATABASE_TESTING/01_sql_testing_for_qa.md"
        ]
    },
    {
        "keywords": ["api", "request", "response", "endpoint", "http"],
        "related_docs": [
            "notes/21_CHEAT_SHEETS/cheat-sheet-api-testing.md",
            "notes/21_CHEAT_SHEETS/cheat-sheet-http-status-codes.md",
            "notes/06_API_TESTING/01_api_testing_fundamentals.md"
        ]
    }
]

def list_code_files(base_dir: Path = BASE_DIR) -> List[Dict[str, Any]]:
    """Crawls directory for allowed code files."""
    code_files = []
    
    for root, dirs, files in os.walk(base_dir):
        # Ignore hidden/venv/git directories
        dirs[:] = [d for d in dirs if not d.startswith((".", "__pycache__", "venv", "node_modules", "data"))]
        
        for file in sorted(files):
            if file in SENSITIVE_FILES:
                continue
            
            file_path = Path(root) / file
            if file_path.suffix.lower() in SUPPORTED_CODE_EXTENSIONS:
                if is_path_safe(file_path):
                    try:
                        rel_path = str(file_path.relative_to(base_dir))
                        code_files.append({
                            "filename": file,
                            "path": str(file_path),
                            "rel_path": rel_path,
                            "extension": file_path.suffix.lower(),
                            "size_bytes": file_path.stat().st_size
                        })
                    except Exception:
                        pass
    return code_files

def get_related_documents_for_code(code_filename: str, code_content: str) -> List[str]:
    """Finds related KB documents for a given code file based on syntax and keywords."""
    combined_text = (code_filename + "\n" + code_content).lower()
    related = set()

    for rule in CODE_LINKING_RULES:
        if any(kw in combined_text for kw in rule["keywords"]):
            for doc in rule["related_docs"]:
                related.add(doc)

    return list(related)
