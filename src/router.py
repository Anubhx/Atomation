import re
from enum import Enum
from typing import Dict, Any, List, Optional, Tuple
from src.retrieval import Retriever
from src.chunker import LoadedDocument

class AnswerSource(str, Enum):
    LOCAL = "LOCAL"
    RAG_GEMINI = "RAG_GEMINI"

class RouterDecision:
    def __init__(
        self,
        source: AnswerSource,
        answer: Optional[str] = None,
        source_docs: Optional[List[str]] = None,
        retrieved_chunks: Optional[List[Tuple[Dict[str, Any], float]]] = None,
        rule_name: Optional[str] = None
    ):
        self.source = source
        self.answer = answer
        self.source_docs = source_docs or []
        self.retrieved_chunks = retrieved_chunks or []
        self.rule_name = rule_name

# Fast-path deterministic knowledge rules
DETERMINISTIC_RULES: List[Dict[str, Any]] = [
    {
        "name": "playwright_get_by_role",
        "keywords": ["get_by_role", "get by role"],
        "answer": """### 🎭 Playwright `get_by_role` Syntax & Best Practices

In Playwright Python, `get_by_role` is the **highest priority accessibility-first locator**.

#### Syntax Example:
```python
# Button
page.get_by_role("button", name="Submit Order").click()

# Checkbox
page.get_by_role("checkbox", name="Accept Terms").check()

# Heading
page.get_by_role("heading", name="Purchase Order Details").should_be_visible()

# Dropdown / Select
page.get_by_role("combobox", name="Vendor Status").select_option("Approved")
```

#### Why Use It:
1. Resilient to DOM structural changes and CSS class updates.
2. Reflects actual assistive technology (screen reader) access.
3. Automatically respects ARIA roles.
""",
        "source_doc": "notes/21_CHEAT_SHEETS/cheat-sheet-playwright.md"
    },
    {
        "name": "playwright_strict_mode",
        "keywords": ["strict mode", "strict mode error", "playwright strict mode"],
        "answer": """### ⚠️ Playwright Strict Mode Error Fix

**What it means:** Playwright strict mode throws an error when a locator resolves to **more than one element** on the DOM page.

#### Example Error:
`Error: locator.click: Error: strict mode violation: get_by_role("button") resolved to 3 elements`

#### Solutions & Fixes:

1. **Use `exact=True` for precise text matching:**
```python
page.get_by_role("button", name="Save", exact=True).click()
```

2. **Scope to a parent container:**
```python
po_card = page.get_by_test_id("po-card-1002")
po_card.get_by_role("button", name="Approve").click()
```

3. **Use `.first`, `.last`, or `.nth(i)` (if ordering is guaranteed):**
```python
page.get_by_role("button", name="Delete").first.click()
```

4. **Add specific accessibility label or test-id:**
```python
page.get_by_label("Purchase Order Number").fill("PO-99481")
```
""",
        "source_doc": "notes/22_TROUBLESHOOTING/troubleshooting-playwright.md"
    },
    {
        "name": "playwright_codegen_command",
        "keywords": ["playwright codegen", "codegen command"],
        "answer": """### 🛠️ Playwright Codegen CLI Command

Launch interactive browser recorder to generate Playwright test scripts automatically:

```bash
# Launch codegen on target portal
playwright codegen https://erp-staging.example.com

# Launch codegen with specific device viewport
playwright codegen --device="iPhone 13" https://portal.example.com

# Save recorded output directly to file
playwright codegen --output=tests/test_purchase_order.py https://erp.example.com
```
""",
        "source_doc": "notes/21_CHEAT_SHEETS/cheat-sheet-playwright.md"
    },
    {
        "name": "http_401_403_404",
        "keywords": ["http 401", "http 403", "http 404", "http status 404", "404 meaning"],
        "answer": """### 🌐 HTTP Status Code Fast Reference

- **401 Unauthorized:** Request lacks valid authentication credentials (e.g. missing/invalid Bearer token, expired session cookie).
- **403 Forbidden:** Authenticated user lacks permission to access the requested resource or role (e.g. Buyer attempting Admin PO approval).
- **404 Not Found:** Target endpoint or resource ID does not exist on the server (e.g. GET `/api/v1/purchase-orders/PO-99999` when PO 99999 does not exist).
""",
        "source_doc": "notes/21_CHEAT_SHEETS/cheat-sheet-http-status-codes.md"
    },
    {
        "name": "pytest_fixture_syntax",
        "keywords": ["pytest fixture", "pytest fixture syntax"],
        "answer": """### 🧪 Pytest Fixture Quick Reference

```python
import pytest

@pytest.fixture(scope="module")
def api_client():
    client = ERPClient(base_url="https://api-staging.example.com")
    client.authenticate("qa_user", "Pass123!")
    yield client
    client.cleanup()

def test_create_po(api_client):
    response = api_client.create_purchase_order(vendor_id="V100")
    assert response.status_code == 201
```

#### Fixture Scopes:
- `function` (default): Setup/teardown per test function.
- `class`: Once per test class.
- `module`: Once per test file module.
- `session`: Once per entire test suite run.
""",
        "source_doc": "notes/21_CHEAT_SHEETS/cheat-sheet-pytest.md"
    },
    {
        "name": "sql_inner_join_syntax",
        "keywords": ["sql inner join", "inner join syntax", "sql join syntax"],
        "answer": """### 🗄️ SQL INNER JOIN Cheat Sheet

```sql
SELECT 
    po.po_number,
    po.vendor_id,
    v.vendor_name,
    po.total_amount,
    po.status
FROM purchase_orders po
INNER JOIN vendors v ON po.vendor_id = v.vendor_id
WHERE po.status = 'PENDING_APPROVAL';
```
""",
        "source_doc": "notes/21_CHEAT_SHEETS/cheat-sheet-sql.md"
    },
    {
        "name": "git_status_command",
        "keywords": ["git status", "git status command"],
        "answer": """### 🐙 Git Status Command

Displays working tree status, modified files, untracked files, and staged changes:

```bash
git status
```
""",
        "source_doc": "notes/21_CHEAT_SHEETS/cheat-sheet-git.md"
    },
    {
        "name": "erp_three_way_match_definition",
        "keywords": ["3-way match", "three-way match", "3 way match", "what is 3-way match"],
        "answer": """### 🏢 ERP 3-Way Match Overview

**3-Way Matching** is an automated control verification in ERP Accounts Payable (AP) that validates three core documents before authorizing invoice payment:

1. **Purchase Order (PO)**: Approved quantites, unit prices, terms issued to vendor.
2. **Goods Receipt / Receiving Log (GR)**: Actual physical quantities accepted by warehouse.
3. **Vendor Invoice**: Bill sent by vendor requesting payment.

#### Validation Rule Matrix:
| Parameter | PO vs GR | PO vs Invoice | GR vs Invoice | Tolerances |
| :--- | :--- | :--- | :--- | :--- |
| **Quantity** | Received <= Ordered | Invoiced <= Ordered | Invoiced == Received | 0% over-billing |
| **Unit Price** | N/A | Invoice Price == PO Price | N/A | Configured tolerance (e.g. ±1%) |
| **Currency** | N/A | Invoice Currency == PO Currency | N/A | Must match |
""",
        "source_doc": "notes/03_ERP_TESTING/03_procure_to_pay_p2p_workflow.md"
    }
]

class IntentRouter:
    def __init__(self, retriever: Retriever):
        self.retriever = retriever

    def route(
        self,
        query: str,
        top_k: int = 5,
        target_doc_id: Optional[str] = None,
        force_rag: bool = False
    ) -> RouterDecision:
        """
        Determines whether the query can be answered deterministically from local rules
        or requires RAG + Gemini synthesis.
        """
        q_lower = query.lower().strip()

        # If not forced RAG, check deterministic fast-path rules
        if not force_rag and not target_doc_id:
            for rule in DETERMINISTIC_RULES:
                for kw in rule["keywords"]:
                    if kw in q_lower:
                        return RouterDecision(
                            source=AnswerSource.LOCAL,
                            answer=rule["answer"],
                            source_docs=[rule["source_doc"]],
                            rule_name=rule["name"]
                        )

        # Retrieve relevant chunks from knowledge base via retriever
        chunks = self.retriever.retrieve(query=query, top_k=top_k, target_doc_id=target_doc_id)
        source_docs = list(dict.fromkeys([c[0]["rel_path"] for c in chunks]))

        return RouterDecision(
            source=AnswerSource.RAG_GEMINI,
            answer=None,
            source_docs=source_docs,
            retrieved_chunks=chunks
        )
