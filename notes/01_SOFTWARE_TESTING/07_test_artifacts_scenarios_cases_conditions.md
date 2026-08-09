---
title: Test Artifacts (Scenarios, Test Cases, Conditions & Data)
category: 01_SOFTWARE_TESTING
subcategory: Test Documentation
keywords:
  - Test Artifacts
  - Test Scenario
  - Test Case
  - Test Condition
  - Test Data
  - Actual vs Expected Result
audience:
  - Quality Engineer
  - SDET
  - Manual Tester
difficulty: beginner-intermediate
---

# 📑 Test Artifacts: Scenarios, Test Cases, Conditions & Data

## 🎯 Overview: The Artifact Hierarchy

Enterprise QA requires clear distinction between high-level conditions, test scenarios, detailed test cases, and supporting test data.

```
       ┌─────────────────────────────────────────────────────────────┐
       │                   TEST CONDITION                            │
       │  High-level item or event to verify (e.g., Vendor Login).   │
       └──────────────────────────────┬──────────────────────────────┘
                                      │
                                      ▼
       ┌─────────────────────────────────────────────────────────────┐
       │                   TEST SCENARIO                             │
       │  End-to-end user story journey (e.g., Procure-to-Pay workflow)│
       └──────────────────────────────┬──────────────────────────────┘
                                      │
                                      ▼
       ┌─────────────────────────────────────────────────────────────┐
       │                    TEST CASE                                │
       │  Specific step-by-step inputs, preconditions, expected result│
       └──────────────────────────────┬──────────────────────────────┘
                                      │
                                      ▼
       ┌─────────────────────────────────────────────────────────────┐
       │                    TEST DATA                                │
       │  Concrete input values (e.g., Tax ID, PO #, JSON payload).   │
       └─────────────────────────────────────────────────────────────┘
```

---

## 📐 Anatomical Breakdown of a Production-Grade Test Case

A test case must be clear enough that **any QA engineer can execute it without ambiguity**.

### Production Test Case Template: `TC_ERP_P2P_009`

* **Test Case ID**: `TC_ERP_P2P_009`
* **Title**: Validate Procure-to-Pay 3-Way Match Block when Invoice Amount exceeds PO Amount by >5%
* **Module / Component**: Procurement / Invoice Matching Engine
* **Priority**: High | **Severity**: Major
* **Preconditions**:
  1. Active Vendor `VEND_8841` exists in database.
  2. Approved PO `PO-2026-104` exists for 10 units @ $100/unit (Total: $1,000).
  3. Goods Receipt `GR-2026-005` created for 10 units.
* **Test Data**:
  - Invoice Number: `INV-TAX-998`
  - Vendor Invoice Line: 10 units @ $110/unit (Total: $1,100 -> +10% discrepancy)
* **Execution Steps**:
  1. Log into ERP Portal as Finance Specialist (`fin_spec_01`).
  2. Navigate to `Finance > Invoices > Create New Invoice`.
  3. Select Vendor `VEND_8841` and reference PO `PO-2026-104`.
  4. Input Invoice Amount `$1,100.00` and click `Submit for Matching`.
* **Expected Result**:
  1. UI displays alert banner: *"Invoice held: 3-Way Match tolerance exceeded (+10.0%)"*.
  2. API response `POST /api/v1/invoices/match` returns HTTP 200 with status `"HELD_VARIANCE_EXCEEDED"`.
  3. SQL Query `SELECT status FROM invoices WHERE invoice_num='INV-TAX-998'` returns `'HELD'`.
  4. `audit_logs` records entry `VARIANCE_BLOCK_TRIGGERED`.
* **Actual Result**: *(Filled during execution)*
* **Status**: `PASS` / `FAIL` | **Executed By**: `Anubhav` | **Date**: `2026-08-09`

---

## 🛑 Expected Result vs. Actual Result

| Term | Definition | Common Mistake |
| :--- | :--- | :--- |
| **Expected Result** | What the system **should** do according to specifications, requirements, and acceptance criteria. | Writing "System works properly" (Too vague!). Must state exact UI, API, DB values. |
| **Actual Result** | What the system **actually** does when the test case is executed. | Omitting log files, status codes, or SQL query output when a step fails. |

---

## 🔗 Related Topics
* [06. User Stories & Acceptance Criteria](06_user_stories_ac_dor_dod.md)
* [01. Black-Box Test Design](../05_TEST_DESIGN/01_black_box_design_techniques.md)
* [03. Industry Bug Report Template](../25_TEMPLATES/03_bug_report_template.md)
