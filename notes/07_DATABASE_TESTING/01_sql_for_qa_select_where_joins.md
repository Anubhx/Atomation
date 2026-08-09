---
title: SQL Basics for QA Engineers (SELECT, WHERE, Aggregations & JOINs)
category: 07_DATABASE_TESTING
subcategory: SQL Fundamentals
keywords:
  - SQL for QA
  - SELECT WHERE
  - INNER JOIN
  - LEFT JOIN
  - RIGHT JOIN
  - FULL JOIN
  - GROUP BY
  - HAVING
audience:
  - Quality Engineer
  - SDET
  - Database QA
difficulty: beginner-intermediate
---

# 🗄️ SQL Basics for QA Engineers: SELECT, WHERE & JOINs

## 🎯 Overview: Why SQL is Mandatory for Enterprise QA

A Quality Engineer cannot rely solely on the UI displaying "Success". SQL queries allow you to audit raw database state, verify foreign key relationships, validate math aggregations, and confirm data retention rules.

---

## 🛠️ The 4 Core SQL JOIN Types

```
  INNER JOIN (Intersection)          LEFT JOIN (All Left + Matching Right)
     ┌───────┐ ┌───────┐                ┌───────┐ ┌───────┐
     │   A   │█│   B   │                │███████│█│   B   │
     │       │█│       │                │██ A ██│█│       │
     └───────┘ └───────┘                └───────┘ └───────┘

  RIGHT JOIN (All Right + Matching Left) FULL JOIN (Union of Both)
     ┌───────┐ ┌───────┐                ┌───────┐ ┌───────┐
     │   A   │█│███████│                │███████│█│███████│
     │       │█│██ B ██│                │██ A ██│█│██ B ██│
     └───────┘ └───────┘                └───────┘ └───────┘
```

| JOIN Type | Result Description | Enterprise QA Use Case |
| :--- | :--- | :--- |
| `INNER JOIN` | Rows with matching keys in BOTH tables. | Fetch Purchase Orders that have corresponding Vendor Master records. |
| `LEFT JOIN` | ALL rows from Left table + matching Right table (NULL if no match). | Find Customers who have NEVER placed a Sales Order (`WHERE order_id IS NULL`). |
| `RIGHT JOIN` | ALL rows from Right table + matching Left table. | Audit orphaned invoice lines without parent Purchase Orders. |
| `FULL JOIN` | All rows from BOTH tables regardless of match. | Reconcile external payment transactions against internal ERP ledgers. |

---

## 💻 Practical SQL Queries for QA Validation

### 1. Basic Filtering & Pattern Matching (`WHERE`, `IN`, `LIKE`, `BETWEEN`)
```sql
-- Find active vendors in USD or EUR created in 2026
SELECT vendor_id, legal_name, currency_code 
FROM vendors 
WHERE is_active = TRUE 
  AND currency_code IN ('USD', 'EUR')
  AND created_at BETWEEN '2026-01-01' AND '2026-12-31'
  AND legal_name LIKE 'Tech%';
```

### 2. Grouping & Aggregation (`GROUP BY`, `HAVING`)
```sql
-- Find Vendors who have been issued more than 5 Purchase Orders with Total Value > $50,000
SELECT vendor_id, COUNT(po_number) AS total_pos, SUM(total_amount) AS total_spend
FROM purchase_orders
WHERE po_status != 'CANCELLED'
GROUP BY vendor_id
HAVING COUNT(po_number) > 5 AND SUM(total_amount) > 50000.00
ORDER BY total_spend DESC;
```

---

## 🔗 Related Topics
* [02. Advanced SQL for QA](02_advanced_sql_subqueries_aggregations_transactions.md)
* [03. ERP Database Schema](03_erp_database_schema_and_qa_queries.md)
* [SQL for QA Cheat Sheet](../21_CHEAT_SHEETS/cheat-sheet-sql.md)
