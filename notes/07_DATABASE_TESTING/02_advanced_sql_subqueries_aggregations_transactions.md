---
title: Advanced SQL for QA (Subqueries, Window Functions & DB Transactions)
category: 07_DATABASE_TESTING
subcategory: Advanced SQL
keywords:
  - Advanced SQL
  - Subqueries
  - Window Functions
  - DB Transactions
  - ACID Properties
  - NULL Handling
audience:
  - Quality Engineer
  - SDET
  - Database QA
difficulty: advanced
---

# 🚀 Advanced SQL for QA: Subqueries, Window Functions & Transactions

## 🎯 Overview

Enterprise QA database testing frequently requires complex data analysis using **Subqueries**, **Window Functions (`ROW_NUMBER`, `DENSE_RANK`)**, **`CASE` conditional statements**, and verifying **ACID Transaction Isolation**.

---

## 💻 Advanced Query Patterns for QA

### 1. Subqueries & Exists Check
```sql
-- Find Purchase Orders whose amount exceeds the vendor's average PO amount
SELECT po_number, vendor_id, total_amount
FROM purchase_orders po1
WHERE total_amount > (
    SELECT AVG(total_amount) 
    FROM purchase_orders po2 
    WHERE po2.vendor_id = po1.vendor_id
);
```

### 2. Window Functions: Finding Duplicate Entries
```sql
-- Identify duplicate payments issued to the same vendor for the same amount within 24 hours
WITH RankedPayments AS (
    SELECT 
        payment_id,
        vendor_id,
        amount,
        created_at,
        ROW_NUMBER() OVER(
            PARTITION BY vendor_id, amount 
            ORDER BY created_at ASC
        ) AS rank_num
    FROM payments
)
SELECT * FROM RankedPayments WHERE rank_num > 1;
```

### 3. Conditional Aggregation via `CASE`
```sql
-- Reconcile Invoice Status counts per Vendor
SELECT 
    vendor_id,
    COUNT(CASE WHEN status = 'PAID' THEN 1 END) AS paid_count,
    COUNT(CASE WHEN status = 'HELD' THEN 1 END) AS held_count,
    COUNT(CASE WHEN status = 'CANCELLED' THEN 1 END) AS cancelled_count
FROM invoices
GROUP BY vendor_id;
```

---

## 🔒 Testing Database Transactions (ACID Validation)

When testing financial transactions, verify that a failure mid-transaction triggers a complete **ROLLBACK**:

```sql
BEGIN TRANSACTION;

-- Step 1: Deduct $500 from Account A
UPDATE bank_accounts SET balance = balance - 500 WHERE account_id = 'ACC_A';

-- Simulated Failure Point (System crash or unhandled foreign key error)
-- ROLLBACK must execute automatically

ROLLBACK;

-- QA Assertion: Verify ACC_A balance remains unchanged!
```

---

## 🔗 Related Topics
* [01. SQL Basics for QA](01_sql_for_qa_select_where_joins.md)
* [03. ERP Database Schema](03_erp_database_schema_and_qa_queries.md)
* [04. Database Data Integrity Testing](04_database_data_integrity_testing.md)
