---
title: Industry Standard Bug Report Template
category: 25_TEMPLATES
subcategory: Bug Templates
keywords:
  - Bug Report Template
  - Defect Form
  - Issue Template
audience:
  - Quality Engineer
  - SDET
  - Manual Tester
difficulty: beginner
---

# 🐛 Industry Standard Bug Report Template

```markdown
### [SUMMARY]: [Component][Action] Brief descriptive summary of failure

**Environment**: `Staging | Chrome 127 | macOS 14.5 | Build v2.4.1`  
**Severity**: `Blocker / Critical / Major / Minor`  
**Priority**: `High / Medium / Low`  
**Jira Component**: `Procurement / Payments`  

---

### Preconditions
1. Active Vendor `VEND_101` exists in database.
2. Approved PO `PO-9941` exists.

---

### Steps to Reproduce
1. Log in as `fin_manager_01`.
2. Navigate to `/finance/invoices/create`.
3. Select PO `PO-9941` and input amount `$15,000.00`.
4. Click `Submit Invoice`.

---

### Expected Result
System accepts invoice, displays success alert, and sets status to `APPROVED`.

### Actual Result
Generic error toast displayed: *"Server Error"*. Network tab shows `POST /api/v1/invoices` returned `HTTP 500`.

---

### Technical Logs & Artifacts
* **API Response**: `{"error": "NullPointerException in TaxEngine.java:42"}`
* **Trace File**: [Link to trace zip artifact]
* **Screenshot**: ![Failure Screenshot](path/to/screenshot.png)
```
