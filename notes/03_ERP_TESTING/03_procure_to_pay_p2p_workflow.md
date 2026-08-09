---
title: Procure-to-Pay (P2P) End-to-End Workflow Testing Guide
category: 03_ERP_TESTING
subcategory: ERP Business Workflows
keywords:
  - Procure-to-Pay
  - P2P Workflow
  - 3-Way Match
  - Purchase Requisition
  - Purchase Order
  - Goods Receipt
  - Invoice Verification
  - Vendor Payment
audience:
  - Quality Engineer
  - ERP QA Lead
  - SDET
difficulty: advanced
---

# 🔄 Procure-to-Pay (P2P) End-to-End Workflow Testing Guide

## 🎯 Business Purpose & High-Level Architecture

The **Procure-to-Pay (P2P)** workflow governs how an enterprise requests, approves, purchases, receives, verifies, and pays for raw materials, inventory, or business services from third-party vendors.

```
[Employee Request]
       │
       ▼
[1. Purchase Requisition (PR)] ──> [Approval Hierarchy Engine]
                                           │ (Approved)
                                           ▼
[2. Purchase Order (PO)] ─────────> [Vendor Fulfillment]
                                           │
                                           ▼
[3. Goods Receipt (GR)] <────────── [Warehouse Delivery]
       │
       ▼
[4. Vendor Invoice] ─────────────> [5. 3-Way Matching Engine (PO vs GR vs Invoice)]
                                           │ (Match Success)
                                           ▼
                                   [6. Payment Dispatch (Check/Wire/ACH)]
```

---

## 👥 Roles & Segregation of Duties (SoD)

To prevent internal fraud, ERP systems enforce strict Segregation of Duties across the P2P lifecycle:

| Role | Permitted Actions | Forbidden Actions (SoD Violations) |
| :--- | :--- | :--- |
| **Requester (Employee)** | Create Purchase Requisitions. | Cannot approve own Requisition or create POs. |
| **Buyer / Procurement** | Create & dispatch POs to approved Vendors. | Cannot receive goods at warehouse or approve invoices. |
| **Warehouse Specialist** | Post Goods Receipt (GR) for physical inventory. | Cannot approve vendor payments or edit PO prices. |
| **Accounts Payable (AP)**| Input Vendor Invoice & run 3-Way Match. | Cannot post Goods Receipt or approve own payment runs. |
| **Finance Manager** | Approve high-value invoices & release payment runs.| Cannot create Purchase Orders or modify Vendor Master bank details. |

---

## 🔍 Detailed Step-by-Step Workflow & State Validation

### Step 1: Purchase Requisition (PR) Creation & Approval
* **Trigger**: Department requires 100 laptops @ $1,000/unit (Total: $100,000).
* **Validation Rules**:
  - Requisitioner budget code must be active and have remaining allocation.
  - Requisition total > $50,000 mandates Level-2 VP Approval.
* **DB Impact**: `INSERT INTO purchase_requisitions` with status `'PENDING_APPROVAL'`.

### Step 2: Purchase Order (PO) Conversion
* **Trigger**: Approved PR converted to official Purchase Order dispatched to Vendor `VEND_LOGITECH`.
* **Validation Rules**:
  - Vendor must be `is_active = TRUE` and have verified Tax ID.
  - Unit prices must match active contract terms.
* **DB Impact**: `INSERT INTO purchase_orders` with status `'ISSUED'`.

### Step 3: Goods Receipt (GR) Posting
* **Trigger**: Shipment arrives at Warehouse; Warehouse Specialist inputs received quantity (100 units).
* **Validation Rules**:
  - Received quantity cannot exceed PO quantity by >0% (unless over-delivery tolerance configured).
  - Material batch number generated.
* **DB Impact**: `INSERT INTO goods_receipts`, `UPDATE inventory_stock SET quantity = quantity + 100`.

### Step 4: Invoice Entry & 3-Way Match Verification
* **Trigger**: Vendor sends Invoice `$100,000` for 100 units.
* **3-Way Match Algorithm**:
  $$\text{Invoice Quantity} == \text{Goods Receipt Quantity}$$
  $$\text{Invoice Unit Price} == \text{Purchase Order Unit Price}$$
  $$\text{Invoice Total Amount} == \text{GR Quantity} \times \text{PO Price} \pm \text{Tolerance Threshold}$$

* **Validation Rules**:
  - If discrepancy > 5%, invoice status MUST set to `'HELD_PRICE_VARIANCE'` and trigger an approval hold.

### Step 5: Payment Run Execution
* **Trigger**: Payment run batch program executes for mature Net-30 invoices.
* **Validation Rules**:
  - Invoice must be in status `'APPROVED_FOR_PAYMENT'`.
  - Vendor bank details validated via SHA-256 hash check.
* **DB Impact**: `INSERT INTO payments`, `UPDATE invoices SET status = 'PAID'`.

---

## 🧪 Deep-Dive SQL Integrity Validation Query

```sql
-- QA Verification Query for 3-Way Match Validation
SELECT 
    po.po_number,
    po.vendor_id,
    po.total_amount AS po_amount,
    gr.gr_number,
    gr.quantity_received,
    inv.invoice_num,
    inv.invoice_amount,
    inv.status AS invoice_status,
    CASE 
        WHEN inv.invoice_amount = po.total_amount AND gr.quantity_received = po.total_quantity THEN 'MATCH_SUCCESS'
        WHEN inv.invoice_amount > po.total_amount * 1.05 THEN 'VARIANCE_BLOCKED'
        ELSE 'MISMATCH_UNKNOWN'
    END AS match_result
FROM purchase_orders po
INNER JOIN goods_receipts gr ON po.po_number = gr.po_number
INNER JOIN invoices inv ON po.po_number = inv.po_number
WHERE po.po_number = 'PO-2026-9941';
```

---

## 🛑 Critical P2P Negative Scenarios & Edge Cases

1. **Duplicate Invoice Submission**: Submitting invoice with identical `vendor_id` + `invoice_number` MUST return HTTP 409 Conflict.
2. **Post-Goods-Receipt PO Modification**: Attempting to reduce PO quantity below already received GR quantity MUST throw a validation error.
3. **Inactive Vendor PO Creation**: Attempting to issue a PO to an inactive vendor MUST block submission at both UI and API levels.

---

## 🔗 Related Topics
* [02. Master Data vs Transaction Data](02_master_data_vs_transaction_data.md)
* [07. ERP Scenario Library](07_erp_scenario_library.md)
* [08. RBAC & SoD Testing](08_rbac_security_and_sod_testing.md)
