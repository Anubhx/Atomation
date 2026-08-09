---
title: Master Data vs Transaction Data Testing in ERP Systems
category: 03_ERP_TESTING
subcategory: ERP Data Model
keywords:
  - Master Data
  - Transaction Data
  - ERP Data Model
  - Customer Master
  - Vendor Master
  - Purchase Orders
audience:
  - Quality Engineer
  - ERP Tester
  - Database QA
difficulty: intermediate
---

# 💾 Master Data vs. Transaction Data Testing in ERP

## 🎯 Overview & Data Taxonomy

In ERP systems, database tables strictly separate **Master Data** (static, long-term business entities) from **Transaction Data** (dynamic operational events referencing Master Data). Understanding this distinction is essential for setting up test data and writing database validation queries.

```
       ┌─────────────────────────────────────────────────────────────┐
       │                       MASTER DATA                           │
       │ Static / Reference Entities (Rarely change, created once)   │
       │ (Customers, Vendors, Materials, Chart of Accounts, Tax Rules)│
       └──────────────────────────────┬──────────────────────────────┘
                                      │
                                      ▼ Referenced By
       ┌─────────────────────────────────────────────────────────────┐
       │                     TRANSACTION DATA                        │
       │ Dynamic Operational Records (Created continuously)           │
       │ (Purchase Orders, Invoices, Goods Receipts, Payments, Stock)│
       └─────────────────────────────────────────────────────────────┘
```

---

## 📊 Structural Comparison Matrix

| Feature | Master Data | Transaction Data |
| :--- | :--- | :--- |
| **Lifecycle** | Long-term (Years/Decades). | Short-term / Event-driven. |
| **Change Frequency**| Low (Modified via formal update requests). | Extremely High (Thousands of writes/minute). |
| **Primary Keys** | Entity IDs (`vendor_id`, `material_sku`). | Transaction IDs (`po_number`, `invoice_id`). |
| **Foreign Keys** | References configuration & tax codes. | Mandatory FK links to Master Data IDs. |
| **Deletion Rules** | Hard deletion strictly prohibited; marked `status='INACTIVE'`. | Cannot delete post-posting; requires reversal entry (`STORNORM`). |

---

## 🔬 Practical ERP Database Schema Mapping

```sql
-- MASTER DATA TABLE: vendors
CREATE TABLE vendors (
    vendor_id VARCHAR(20) PRIMARY KEY,
    legal_name VARCHAR(100) NOT NULL,
    tax_identifier VARCHAR(30) UNIQUE NOT NULL,
    payment_terms VARCHAR(10) DEFAULT 'NET30',
    currency_code VARCHAR(3) DEFAULT 'USD',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TRANSACTION DATA TABLE: purchase_orders
CREATE TABLE purchase_orders (
    po_number VARCHAR(30) PRIMARY KEY,
    vendor_id VARCHAR(20) REFERENCES vendors(vendor_id), -- FK to Master Data
    total_amount DECIMAL(15,2) CHECK (total_amount >= 0),
    po_status VARCHAR(20) DEFAULT 'DRAFT',
    created_by VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🧪 QA Validation Strategies

### 1. Master Data Testing Rules
- Verify unique constraints on Tax IDs and Business Registration numbers.
- Verify that setting a Vendor to `is_active = FALSE` prevents new Purchase Orders from selecting that vendor.
- Verify audit log triggers whenever bank routing numbers in Vendor Master are modified.

### 2. Transaction Data Testing Rules
- Verify referential integrity: attempting to create a Purchase Order for a non-existent `vendor_id` MUST trigger a DB Foreign Key constraint error.
- Verify state machine constraints: a Purchase Order with status `CANCELLED` cannot transition to `GOODS_RECEIVED`.

---

## 🔗 Related Topics
* [01. ERP Architecture](01_erp_architecture_and_concepts.md)
* [03. Procure-to-Pay (P2P) Workflow](03_procure_to_pay_p2p_workflow.md)
* [03. ERP Database Schema](../07_DATABASE_TESTING/03_erp_database_schema_and_qa_queries.md)
