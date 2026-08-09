---
title: Complex Enterprise ERP & E2E Case Studies
category: 24_REAL_WORLD_SCENARIOS
subcategory: Case Studies
keywords:
  - Enterprise Case Studies
  - ERP Production Outage
  - QA Incident Analysis
  - Real World Scenarios
audience:
  - Quality Engineer
  - SDET
  - QA Lead
difficulty: advanced
---

# 🏢 Complex Enterprise ERP & E2E Case Studies

## 🎯 Case Study 1: The Multi-Million Dollar Rounding Discrepancy

### Incident Summary
A major enterprise client experienced a $420,000 monthly discrepancy between Accounts Payable sub-ledgers and the General Ledger following a cloud ERP migration.

### Root Cause
Line item tax calculations applied JavaScript standard floating-point division (`amount * 0.08875`) on individual lines and rounded to 2 decimal places before summing, whereas the General Ledger calculated tax on the grand total. Over 1,200,000 monthly transactions, 1-cent rounding errors accumulated to hundreds of thousands of dollars.

### QA Remediation & Prevention
1. Enforced standard **Banker's Rounding (`ROUND_HALF_EVEN`)** in backend pricing microservices using Decimal data types (never floating-point floats!).
2. Created an automated SQL regression test running nightly to verify $\sum \text{Line Item Taxes} == \text{Header Total Tax} \pm \$0.00$.

---

## 🔗 Related Topics
* [09. ERP Data Integrity Verification](../03_ERP_TESTING/09_erp_data_integrity_ui_api_db_audit.md)
* [06. Defect Prevention & RCA](../02_QA_ENGINEERING/06_defect_prevention_rca.md)
