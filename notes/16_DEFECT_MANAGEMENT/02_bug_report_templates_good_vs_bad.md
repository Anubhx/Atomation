---
title: High-Impact Bug Report Writing (Excellent vs Poor Examples)
category: 16_DEFECT_MANAGEMENT
subcategory: Bug Reporting
keywords:
  - Bug Report
  - Defect Writing
  - Steps to Reproduce
  - Actual vs Expected
  - Defect Quality
audience:
  - Quality Engineer
  - SDET
  - Manual Tester
difficulty: beginner-intermediate
---

# ✍️ High-Impact Bug Report Writing: Excellent vs. Poor Examples

## 🎯 Overview: What Makes a Great Bug Report?

A well-crafted bug report eliminates developer friction, enables 1-click reproduction, provides exact technical logs, and clearly states business impact.

---

## 🆚 Poor vs. Excellent Bug Report Comparison

### ❌ POOR BUG REPORT (DO NOT DO THIS)
* **Title**: Payment doesn't work
* **Description**: I tried to pay an invoice and it failed. Fix please.
* **Environment**: QA

---

### ✅ EXCELLENT PRODUCTION BUG REPORT
* **Title**: `[P2P][Payment] HTTP 500 Internal Error when approving ACH Payment for Vendor with international IBAN`
* **Environment**: `Staging-v2.4.1 | Chrome 127 (Mac) | PostgreSQL 15`
* **Severity**: `High` | **Priority**: `High`
* **Preconditions**:
  1. Vendor `VEND_INTL_90` exists with international IBAN `DE89370400440532013000`.
  2. Approved Invoice `INV-2026-991` exists for `$12,500.00`.
* **Steps to Reproduce**:
  1. Log into ERP Portal as Finance Manager (`fin_mgr_01`).
  2. Navigate to `Finance > Pending Payments > INV-2026-991`.
  3. Click `Execute Payment Run` select method `ACH`.
* **Expected Result**: System processes payment, displays success toast, and updates invoice status to `PAID`.
* **Actual Result**: Screen displays generic error toast: *"System error occurred"*. Browser console shows `POST /api/v1/payments/execute` returned HTTP 500.
* **Technical Evidence**:
  - API Payload: `{"invoice_id": "INV-2026-991", "method": "ACH"}`
  - Server Log Snippet: `ValueError: IBAN length exceeds ACH routing limit (34 chars > 9 chars)`
  - Screenshot / Trace: `[Link to Playwright Trace zip artifact]`

---

## 🔗 Related Topics
* [01. Defect Lifecycle & Severity](01_defect_lifecycle_severity_priority.md)
* [03. Industry Bug Report Template](../25_TEMPLATES/03_bug_report_template.md)
