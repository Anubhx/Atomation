---
title: ERP Test Scenario Library (Edge Cases & Failure Modes)
category: 03_ERP_TESTING
subcategory: Test Scenarios
keywords:
  - ERP Test Scenarios
  - Duplicate PO
  - Duplicate Invoice
  - Inactive Vendor
  - Unauthorized Approval
  - Zero Quantity
  - Negative Quantity
  - ERP Edge Cases
audience:
  - Quality Engineer
  - ERP Tester
  - SDET
difficulty: advanced
---

# 📚 ERP Test Scenario Library: 50+ Enterprise Edge Cases & Failure Modes

## 🎯 Overview

This scenario library provides ready-to-use, practical edge cases for testing ERP financial, procurement, sales, and warehouse systems.

---

## 🏬 Module 1: Procurement & Vendor Management Scenarios

| Scenario ID | Test Scenario | Input / Action | Expected System Behavior | Validation Method |
| :--- | :--- | :--- | :--- | :--- |
| `SC_PROC_001` | Duplicate Invoice Submission | Submit Invoice `INV-9901` twice for same Vendor `VEND_88`. | System rejects 2nd submission with HTTP 409 / UI message: *"Duplicate Invoice detected"*. | API Status + SQL `SELECT COUNT(*)` |
| `SC_PROC_002` | Inactive Vendor PO Creation | Select Vendor where `is_active = FALSE`. | System blocks PO creation; dropdown suppresses inactive vendors. | UI Element state + API Schema check |
| `SC_PROC_003` | Self-Approval Violation | Buyer attempts to approve own PO `$25,000`. | Approval button disabled / API returns HTTP 403 Forbidden. | API Role authorization check |
| `SC_PROC_004` | Quantity Below Zero | Input PO Item quantity `-5`. | Form validation blocks submission: *"Quantity must be > 0"*. | UI Form validation + DB Constraint check |
| `SC_PROC_005` | Zero Quantity | Input PO Item quantity `0`. | System rejects payload with HTTP 422 Unprocessable Entity. | API Payload error response |
| `SC_PROC_006` | Maximum Integer Quantity | Input PO Item quantity `999,999,999,999`. | System handles gracefully or caps at Max PO limit; no numeric overflow crash. | DB Integer field inspection |
| `SC_PROC_007` | Invalid Currency Code | Submit PO with currency `XYZ`. | System rejects invalid ISO currency code. | API Payload error response |
| `SC_PROC_008` | Expired Vendor Contract | Issue PO referencing Contract `CTR-2022` (expired 2025). | System displays *"Contract Expired"* and blocks line item entry. | DB Contract status check |
| `SC_PROC_009` | Over-Delivery Exceeds Tolerance | Post Goods Receipt for 150 units on PO of 100 (Tolerance = 5%). | System blocks GR posting: *"Over-delivery tolerance (+50%) exceeded"*. | UI Toast + DB Goods Receipt record |
| `SC_PROC_010` | Partial Goods Receipt | Post GR for 40 units on PO of 100. | PO status updates to `PARTIALLY_DELIVERED`; remaining open quantity set to 60. | SQL `SELECT open_quantity FROM purchase_orders` |

---

## 💰 Module 2: Finance & Accounts Payable Scenarios

| Scenario ID | Test Scenario | Input / Action | Expected System Behavior | Validation Method |
| :--- | :--- | :--- | :--- | :--- |
| `SC_FIN_001` | Duplicate Payment Execution | Trigger payment run for Invoice `INV-772` twice. | System flags invoice as `ALREADY_PAID` and excludes from payment file. | Payment Audit Log + SQL check |
| `SC_FIN_002` | Closed Accounting Period Posting | Post Journal Entry dated 2025-12-31 into locked period. | System rejects posting with error: *"Accounting Period 2025-12 is closed"*. | GL Posting engine response |
| `SC_FIN_003` | Unbalanced Journal Entry | Submit Journal Entry with Debits = $1,000 and Credits = $950. | System blocks posting: *"Journal Entry out of balance ($50.00)"*. | API GL validation check |
| `SC_FIN_004` | Tax Rounding Discrepancy | Calculate 8.875% tax on 3 line items ($10.33, $14.11, $99.05). | System applies standard banker's rounding (`HALF_EVEN`); grand total balances to penny. | DB Decimal precision audit |

---

## 📦 Module 3: Sales, Credit & Inventory Scenarios

| Scenario ID | Test Scenario | Input / Action | Expected System Behavior | Validation Method |
| :--- | :--- | :--- | :--- | :--- |
| `SC_SD_001` | Credit Limit Violation | Create Sales Order exceeding Customer credit limit. | Order automatically placed on `CREDIT_HOLD`; email sent to Credit Manager. | Order Status + Email Log |
| `SC_SD_002` | Concurrent Stock Reservation | Two users order last 10 items simultaneously. | DB transaction lock allows 1st user; 2nd user receives *"Stock backordered"*. | DB Isolation level & concurrent test |
| `SC_SD_003` | Partial Shipment Billing | Ship 5 out of 10 items on Sales Order. | Invoicing generates bill for 5 shipped items only; open balance maintained. | Customer Billing Document verification |

---

## 🔗 Related Topics
* [03. Procure-to-Pay (P2P) Workflow](03_procure_to_pay_p2p_workflow.md)
* [04. Order-to-Cash (O2C) Workflow](04_order_to_cash_o2c_workflow.md)
* [08. RBAC & SoD Testing](08_rbac_security_and_sod_testing.md)
