---
title: Combined UI + API + Database Automation Testing Pattern
category: 10_AUTOMATION_ARCHITECTURE
subcategory: Full-Stack Testing Patterns
keywords:
  - Combined UI API DB
  - Full-Stack Testing
  - Fast Data Seeding
  - Multi-Tier Validation
  - Hybrid Automation
audience:
  - Quality Engineer
  - SDET
  - Automation Architect
difficulty: advanced
---

# ⚡ Combined UI + API + Database Automation Testing Pattern

## 🎯 Overview: Why Hybrid Testing Dominates Enterprise Automation

Executing 100% of setup steps via the UI makes test suites slow, brittle, and prone to random network failures. The **Combined UI + API + DB Pattern** uses the fastest tier for each step:

```
[ Step 1: SETUP ] ──> Fast API Call creates Customer & Vendor in 200ms (Bypasses 5 UI pages).
         │
[ Step 2: ACTION ] ──> UI Execution triggers actual business workflow step (Submits PO via Playwright).
         │
[ Step 3: ASSERT ] ──> API Call validates status == 'APPROVED'.
         │
[ Step 4: AUDIT ] ──> SQL Query verifies DB tables & Audit logs contain exact transaction records.
```

---

## 💻 Full-Stack Hybrid Test Implementation Example

```python
import pytest
from playwright.sync_api import Page, expect

def test_combined_p2p_invoice_approval(page: Page, api_client, db_connection):
    """
    Hybrid Test Pattern:
    1. API creates test Vendor & Purchase Order (Fast Setup).
    2. UI submits Invoice against the PO (User Experience Action).
    3. API verifies Invoice match status (API Assertion).
    4. SQL verifies Financial Ledger & Audit Trail (Database Integrity).
    """
    # 1. SETUP: Fast API Seeding (Takes ~150ms instead of 45 seconds of UI clicks)
    vendor_data = api_client.create_vendor({"name": "FastSeeded Vendor Inc"})
    po_data = api_client.create_purchase_order({
        "vendor_id": vendor_data["vendor_id"],
        "total": 5000.00
    })
    po_number = po_data["po_number"]

    # 2. ACTION: UI Execution (Testing actual user interface)
    page.goto(f"/finance/invoices/create?po={po_number}")
    page.get_by_label("Invoice Number").fill("INV-HYBRID-991")
    page.get_by_label("Invoice Amount").fill("5000.00")
    page.get_by_role("button", name="Submit Invoice").click()
    
    expect(page.get_by_text("Invoice Submitted Successfully")).to_be_visible()

    # 3. API VERIFICATION: Verify backend status via API call
    inv_response = api_client.get_invoice("INV-HYBRID-991")
    assert inv_response.json()["status"] == "MATCH_SUCCESS"

    # 4. DB & AUDIT VERIFICATION: Verify database state & immutable audit log
    cursor = db_connection.cursor()
    cursor.execute("SELECT status FROM invoices WHERE invoice_num = %s", ("INV-HYBRID-991",))
    assert cursor.fetchone()[0] == "MATCH_SUCCESS"
    
    cursor.execute("SELECT action_type FROM audit_logs WHERE entity_id = %s", ("INV-HYBRID-991",))
    assert cursor.fetchone()[0] == "INVOICE_SUBMITTED"
```

---

## 🔗 Related Topics
* [01. Framework Architecture](01_enterprise_automation_framework_design.md)
* [09. ERP Data Integrity Verification](../03_ERP_TESTING/09_erp_data_integrity_ui_api_db_audit.md)
