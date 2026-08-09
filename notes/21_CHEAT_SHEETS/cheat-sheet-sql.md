---
title: SQL for QA Engineers Cheat Sheet
category: 21_CHEAT_SHEETS
subcategory: SQL
keywords:
  - SQL Cheat Sheet
  - SELECT WHERE JOIN
  - Aggregations
  - Transactions
audience:
  - Quality Engineer
  - SDET
difficulty: beginner-intermediate
---

# 🗄️ SQL for QA Engineers Cheat Sheet

## 🔍 Select, Filter & Aggregate
```sql
SELECT vendor_id, COUNT(po_number) AS total_pos, SUM(total_amount) AS total_val
FROM purchase_orders
WHERE status = 'APPROVED' AND created_at >= '2026-01-01'
GROUP BY vendor_id
HAVING COUNT(po_number) > 5
ORDER BY total_val DESC;
```

## 🔗 JOIN Syntax
```sql
-- Inner Join: Matching rows in both tables
SELECT po.po_number, v.legal_name 
FROM purchase_orders po
INNER JOIN vendors v ON po.vendor_id = v.vendor_id;

-- Left Join: Find records in Left with NO match in Right
SELECT c.customer_id FROM customers c
LEFT JOIN sales_orders so ON c.customer_id = so.customer_id
WHERE so.order_id IS NULL;
```
