---
title: ERP Role-Based Access (RBAC) & Segregation of Duties (SoD) Testing
category: 03_ERP_TESTING
subcategory: ERP Security
keywords:
  - RBAC
  - Role-Based Access Control
  - Segregation of Duties
  - SoD
  - Permission Matrix
  - Least Privilege
  - ERP Authorization
audience:
  - Quality Engineer
  - ERP Security Tester
  - SDET
difficulty: advanced
---

# 🔐 ERP Role-Based Access (RBAC) & Segregation of Duties (SoD) Testing

## 🎯 Overview: Authentication vs. Authorization vs. SoD

Enterprise ERP security relies on three defense tiers:
1. **Authentication (Who are you?)**: Verifying user identity via SSO / OAuth2 / SAML.
2. **Authorization (What can you do?)**: Restricting UI elements, API endpoints, and SQL tables based on assigned Roles.
3. **Segregation of Duties (SoD) (What combinations are forbidden?)**: Ensuring a single user account cannot hold mutually conflicting permissions that allow undetected fraud (e.g., creating a vendor AND approving payment to that vendor).

---

## 📋 Comprehensive Enterprise Role Permission Matrix

| Role | Create PO | Approve PO | Post Goods Receipt | Input Invoice | Approve Payment | Modify Vendor Master |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Buyer** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Purchasing Manager** | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Warehouse Specialist**| ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| **Accounts Payable (AP)**| ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| **Finance Manager** | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |
| **Vendor Administrator**| ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **System Auditor** | 👁️ Read | 👁️ Read | 👁️ Read | 👁️ Read | 👁️ Read | 👁️ Read |

---

## 🔬 Multi-Layer Security Validation Strategy

When testing an RBAC rule (e.g., "Warehouse Specialist cannot approve invoices"), validate across ALL three layers:

```
[1. UI Layer Check]: Verify "Approve Invoice" button is hidden/disabled in frontend DOM.
         │
[2. API Layer Check]: Execute POST /api/v1/invoices/104/approve with Warehouse Bearer Token.
                     Assert response HTTP 403 Forbidden.
         │
[3. DB / Audit Check]: Query database to verify status remains 'UNAPPROVED' and audit log records 'UNAUTHORIZED_ACCESS_ATTEMPT'.
```

---

## 🧪 Playwright + Pytest Authorization Test Example

```python
import pytest
from playwright.sync_api import Page, expect

def test_buyer_cannot_approve_own_po(page: Page, buyer_auth_headers):
    """
    Security Test: Verify Buyer role cannot approve Purchase Order via API.
    """
    # Attempt API approval using Buyer credentials
    response = page.request.post(
        "/api/v1/purchase-orders/PO-99412/approve",
        headers=buyer_auth_headers
    )
    
    # Assert HTTP 403 Forbidden status code
    assert response.status == 403, f"Expected 403, got {response.status}"
    
    # Assert error payload body
    data = response.json()
    assert data["error_code"] == "INSUFFICIENT_PRIVILEGES"
    assert "Buyer role cannot approve Purchase Orders" in data["message"]
```

---

## 🔗 Related Topics
* [03. Procure-to-Pay (P2P) Workflow](03_procure_to_pay_p2p_workflow.md)
* [01. QA Security Testing](../13_SECURITY/01_qa_security_testing_rbac_idor_session_inputs.md)
* [09. Data Integrity Verification](09_erp_data_integrity_ui_api_db_audit.md)
