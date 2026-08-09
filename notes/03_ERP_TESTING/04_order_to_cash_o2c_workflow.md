---
title: Order-to-Cash (O2C) End-to-End Workflow Testing Guide
category: 03_ERP_TESTING
subcategory: ERP Business Workflows
keywords:
  - Order-to-Cash
  - O2C Workflow
  - Sales Order
  - Credit Check
  - Fulfillment
  - Billing
  - Cash Application
audience:
  - Quality Engineer
  - ERP Tester
  - SDET
difficulty: advanced
---

# 💸 Order-to-Cash (O2C) End-to-End Workflow Testing Guide

## 🎯 Business Purpose & High-Level Architecture

The **Order-to-Cash (O2C)** workflow governs how an enterprise receives customer orders, verifies creditworthiness, reserves and ships inventory, generates customer invoices, and collects payments.

```
[Customer Order] ──> [1. Credit Check Engine] ──> [2. Sales Order (SO) Creation]
                                                           │
                                                           ▼
[5. Cash Application] <── [4. Customer Invoice] <── [3. Warehouse Pick, Pack & Ship]
```

---

## 🔍 Detailed Workflow Steps & Validation Rules

### Step 1: Sales Order Creation & Credit Limit Lock
* **Validation Rule**: Customer's pending order value + current unpaid balance MUST NOT exceed `credit_limit`.
* **Failure Mode**: If order exceeds limit, status MUST update to `'CREDIT_HOLD'` and block warehouse fulfillment.

### Step 2: Inventory Reservation
* **Validation Rule**: Stock items must be reserved in `inventory_stock` (`available_quantity` drops, `reserved_quantity` increases).

### Step 3: Goods Delivery & Logistics Dispatch
* **Validation Rule**: Shipping generates Outbound Delivery Document (`DELIV-8812`) and updates stock.

### Step 4: Billing & Revenue Recognition
* **Validation Rule**: Invoicing posts debit entry to Accounts Receivable (AR) and credit entry to Sales Revenue GL.

### Step 5: Customer Payment & Cash Application
* **Validation Rule**: Applying payment clears AR balance and updates customer credit availability.

---

## 🧪 Deep-Dive SQL Integrity Validation Query

```sql
-- QA Verification Query for O2C Credit Limit & AR Balance
SELECT 
    c.customer_id,
    c.company_name,
    c.credit_limit,
    COALESCE(SUM(so.total_amount), 0) AS open_order_total,
    COALESCE(SUM(ar.balance_due), 0) AS open_ar_balance,
    (c.credit_limit - COALESCE(SUM(so.total_amount), 0) - COALESCE(SUM(ar.balance_due), 0)) AS remaining_credit
FROM customers c
LEFT JOIN sales_orders so ON c.customer_id = so.customer_id AND so.status = 'CREDIT_HOLD'
LEFT JOIN accounts_receivable ar ON c.customer_id = ar.customer_id AND ar.status = 'UNPAID'
WHERE c.customer_id = 'CUST-10492'
GROUP BY c.customer_id, c.company_name, c.credit_limit;
```

---

## 🔗 Related Topics
* [03. Procure-to-Pay (P2P) Workflow](03_procure_to_pay_p2p_workflow.md)
* [06. Inventory Lifecycle](06_inventory_lifecycle.md)
* [07. ERP Scenario Library](07_erp_scenario_library.md)
