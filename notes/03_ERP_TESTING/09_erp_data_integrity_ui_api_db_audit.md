---
title: ERP Data Integrity Verification (UI -> API -> DB -> Audit Log)
category: 03_ERP_TESTING
subcategory: ERP Data Validation
keywords:
  - Data Integrity
  - UI API DB Audit
  - State Verification
  - Financial Ledger
  - Audit Trail
  - Full-Stack Testing
audience:
  - Quality Engineer
  - SDET
  - Database QA
difficulty: advanced
---

# 🔍 ERP Data Integrity Verification: Full-Stack Pipeline

## 🎯 Overview: The 5-Layer Integrity Pipeline

Validating an enterprise transaction requires verifying consistency across five interconnected layers:

```
  [ Layer 1: UI Display ] ──> Frontend forms, table rows, toast notifications.
            │
  [ Layer 2: API Payload ] ──> HTTP request/response JSON schema & status codes.
            │
  [ Layer 3: Database ] ──> Relational tables, foreign keys, transaction commits.
            │
  [ Layer 4: Audit Log ] ──> Immutable system action logs (`user_id`, `timestamp`, `old_val`, `new_val`).
            │
  [ Layer 5: BI Reports ] ──> Nightly data warehouse ETL & financial summary reports.
```

---

## 🔬 Step-by-Step Practical Validation Walkthrough

### Scenario: Approving a Vendor Invoice `$50,000`

```python
import psycopg2
from playwright.sync_api import Page, expect

def test_full_stack_invoice_approval_integrity(page: Page, db_connection):
    # 1. UI LAYER VALIDATION
    page.goto("/finance/invoices/INV-2026-881")
    page.get_by_role("button", name="Approve Invoice").click()
    expect(page.get_by_text("Invoice Approved Successfully")).to_be_visible()

    # 2. API LAYER VALIDATION (Verified via network interception or response logger)
    # Status code == 200 OK, payload status == "APPROVED"

    # 3. DATABASE LAYER VALIDATION
    cursor = db_connection.cursor()
    cursor.execute(
        "SELECT status, approved_by, approved_at FROM invoices WHERE invoice_num = %s",
        ("INV-2026-881",)
    )
    row = cursor.fetchone()
    assert row[0] == "APPROVED", f"Expected DB status APPROVED, got {row[0]}"
    assert row[1] == "fin_manager_01", f"Expected approver fin_manager_01, got {row[1]}"

    # 4. AUDIT LOG VALIDATION
    cursor.execute(
        "SELECT action, previous_state, new_state FROM audit_logs WHERE entity_id = %s ORDER BY created_at DESC LIMIT 1",
        ("INV-2026-881",)
    )
    audit_row = cursor.fetchone()
    assert audit_row[0] == "INVOICE_STATE_CHANGE"
    assert audit_row[1] == '{"status": "PENDING"}'
    assert audit_row[2] == '{"status": "APPROVED"}'
```

---

## 🔗 Related Topics
* [03. Procure-to-Pay (P2P) Workflow](03_procure_to_pay_p2p_workflow.md)
* [03. ERP Database Schema](../07_DATABASE_TESTING/03_erp_database_schema_and_qa_queries.md)
* [03. Combined UI+API+DB Testing](../10_AUTOMATION_ARCHITECTURE/03_combined_ui_api_db_testing_pattern.md)
