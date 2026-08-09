---
title: Enterprise ERP Database Schema & Practical QA Verification Queries
category: 07_DATABASE_TESTING
subcategory: ERP Database Testing
keywords:
  - ERP Schema
  - Purchase Orders DB
  - Invoices DB
  - Audit Logs DB
  - Foreign Keys
  - QA SQL Cookbook
audience:
  - Quality Engineer
  - ERP QA Specialist
  - Database SDET
difficulty: advanced
---

# 🏢 Enterprise ERP Database Schema & Practical QA Verification Queries

## 🎯 Overview: Standard Enterprise ERP Schema Model

The following DDL schema represents a standard enterprise ERP database containing core master tables, transaction tables, role management, and immutable audit logs.

```
 [ customers ] ──────< [ sales_orders ] ──────< [ sales_order_items ]
                            │
 [ vendors ] ────────< [ purchase_orders ] ───< [ purchase_order_items ]
     │                      │
     │                      ▼
     └───────────────< [ invoices ] ──────────< [ payments ]
                            │
                     [ audit_logs ]
```

---

## 🗄️ Standard ERP DDL Database Definition

```sql
-- MASTER: customers
CREATE TABLE customers (
    customer_id VARCHAR(30) PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    credit_limit DECIMAL(15,2) NOT NULL DEFAULT 5000.00,
    is_active BOOLEAN DEFAULT TRUE
);

-- MASTER: vendors
CREATE TABLE vendors (
    vendor_id VARCHAR(30) PRIMARY KEY,
    legal_name VARCHAR(100) NOT NULL,
    tax_id VARCHAR(30) UNIQUE NOT NULL,
    payment_terms VARCHAR(10) DEFAULT 'NET30',
    is_active BOOLEAN DEFAULT TRUE
);

-- TRANSACTION: purchase_orders
CREATE TABLE purchase_orders (
    po_number VARCHAR(30) PRIMARY KEY,
    vendor_id VARCHAR(30) REFERENCES vendors(vendor_id),
    total_amount DECIMAL(15,2) CHECK (total_amount >= 0),
    status VARCHAR(20) DEFAULT 'DRAFT', -- DRAFT, PENDING_APPROVAL, APPROVED, REJECTED, CANCELLED
    created_by VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TRANSACTION: purchase_order_items
CREATE TABLE purchase_order_items (
    item_id SERIAL PRIMARY KEY,
    po_number VARCHAR(30) REFERENCES purchase_orders(po_number) ON DELETE CASCADE,
    sku VARCHAR(50) NOT NULL,
    quantity INT CHECK (quantity > 0),
    unit_price DECIMAL(15,2) CHECK (unit_price >= 0)
);

-- TRANSACTION: invoices
CREATE TABLE invoices (
    invoice_id SERIAL PRIMARY KEY,
    invoice_num VARCHAR(50) NOT NULL,
    vendor_id VARCHAR(30) REFERENCES vendors(vendor_id),
    po_number VARCHAR(30) REFERENCES purchase_orders(po_number),
    invoice_amount DECIMAL(15,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'UNPAID', -- UNPAID, APPROVED, HELD, PAID
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_vendor_invoice UNIQUE (vendor_id, invoice_num)
);

-- TRANSACTION: payments
CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    invoice_id INT REFERENCES invoices(invoice_id),
    amount_paid DECIMAL(15,2) NOT NULL,
    payment_method VARCHAR(20) NOT NULL, -- ACH, WIRE, CHECK
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- INVENTORY: inventory_stock
CREATE TABLE inventory_stock (
    sku VARCHAR(50) PRIMARY KEY,
    available_qty INT CHECK (available_qty >= 0),
    reserved_qty INT CHECK (reserved_qty >= 0),
    warehouse_bin VARCHAR(20) NOT NULL
);

-- AUDIT: audit_logs
CREATE TABLE audit_logs (
    log_id BIGSERIAL PRIMARY KEY,
    entity_name VARCHAR(50) NOT NULL,
    entity_id VARCHAR(50) NOT NULL,
    action_type VARCHAR(30) NOT NULL, -- INSERT, UPDATE, DELETE, SECURITY_ALERT
    performed_by VARCHAR(50) NOT NULL,
    previous_state JSONB,
    new_state JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🧪 Practical QA Verification SQL Cookbook

### 1. Detect Orphaned Purchase Order Line Items (Data Corruption Check)
```sql
SELECT poi.item_id, poi.po_number
FROM purchase_order_items poi
LEFT JOIN purchase_orders po ON poi.po_number = po.po_number
WHERE po.po_number IS NULL;
```

### 2. Verify Sum of Line Items Matches Header Total
```sql
SELECT 
    po.po_number,
    po.total_amount AS header_total,
    SUM(poi.quantity * poi.unit_price) AS calculated_line_total,
    (po.total_amount - SUM(poi.quantity * poi.unit_price)) AS discrepancy
FROM purchase_orders po
INNER JOIN purchase_order_items poi ON po.po_number = poi.po_number
GROUP BY po.po_number, po.total_amount
HAVING po.total_amount != SUM(poi.quantity * poi.unit_price);
```

### 3. Verify Audit Trail Records State Changes
```sql
SELECT log_id, entity_id, action_type, performed_by, previous_state, new_state, created_at
FROM audit_logs
WHERE entity_name = 'invoices' 
  AND entity_id = 'INV-9941'
ORDER BY created_at DESC;
```

---

## 🔗 Related Topics
* [01. SQL Basics for QA](01_sql_for_qa_select_where_joins.md)
* [02. Master Data vs Transaction Data](../03_ERP_TESTING/02_master_data_vs_transaction_data.md)
* [09. ERP Data Integrity Verification](../03_ERP_TESTING/09_erp_data_integrity_ui_api_db_audit.md)
