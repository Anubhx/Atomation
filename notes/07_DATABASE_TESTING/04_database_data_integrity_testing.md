---
title: Database Data Integrity, Schema Validation & Constraints
category: 07_DATABASE_TESTING
subcategory: Data Integrity
keywords:
  - Database Integrity
  - Foreign Keys
  - Unique Constraints
  - Check Constraints
  - Schema Validation
audience:
  - Quality Engineer
  - SDET
  - Database QA
difficulty: intermediate
---

# 🛡️ Database Data Integrity & Schema Validation Guide

## 🎯 Overview: Database Constraints as Quality Defense

Database constraints enforce structural data integrity directly at the storage engine level—preventing corrupted inputs regardless of application bugs.

---

## 📋 Core Constraint Types & QA Verification Tests

| Constraint Type | Purpose | Test Case Execution | Expected Behavior |
| :--- | :--- | :--- | :--- |
| **PRIMARY KEY** | Uniquely identifies each row; prohibits NULLs. | Insert row with existing PK value. | `ERROR: duplicate key value violates unique constraint` |
| **FOREIGN KEY** | Enforces referential integrity between tables. | Insert `purchase_orders` row with invalid `vendor_id='9999'`. | `ERROR: insert or update violates foreign key constraint` |
| **UNIQUE** | Prohibits duplicate non-null entries (e.g. Tax ID). | Insert Vendor with registered `tax_id`. | `ERROR: unique constraint violation` |
| **CHECK** | Evaluates boolean expression (e.g., `amount >= 0`). | Insert Invoice with `invoice_amount = -50.00`. | `ERROR: new row for relation violates check constraint` |
| **NOT NULL** | Mandatory field requirement. | Insert User without `email`. | `ERROR: null value in column violates not-null constraint` |

---

## 🔗 Related Topics
* [01. SQL Basics for QA](01_sql_for_qa_select_where_joins.md)
* [03. ERP Database Schema](03_erp_database_schema_and_qa_queries.md)
