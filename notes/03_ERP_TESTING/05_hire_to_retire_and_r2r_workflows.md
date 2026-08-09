---
title: Hire-to-Retire (H2R) & Record-to-Report (R2R) Workflow Guides
category: 03_ERP_TESTING
subcategory: ERP Business Workflows
keywords:
  - Hire-to-Retire
  - H2R Workflow
  - Record-to-Report
  - R2R Workflow
  - General Ledger
  - Financial Closing
audience:
  - Quality Engineer
  - ERP Tester
difficulty: intermediate
---

# 📑 Hire-to-Retire (H2R) & Record-to-Report (R2R) Field Guide

## 🎯 Overview

Beyond P2P and O2C, enterprise ERP quality assurance covers **Hire-to-Retire (H2R)** (Human Capital Management) and **Record-to-Report (R2R)** (Financial Accounting & General Ledger Closure).

---

## 👥 Hire-to-Retire (H2R) Workflow

### 1. Business Process Stages
1. **Recruitment & Candidate Offer Accept**: Candidate data transferred to HR Master.
2. **Employee Onboarding**: Creating employee master (`emp_id`), assigning organizational unit, pay grade, and tax withholding status.
3. **Time & Attendance Tracking**: Submitting weekly timesheets; approving overtime.
4. **Payroll Execution**: Calculating gross pay, tax deductions, benefit withholdings, net pay.
5. **Termination / Retirement Offboarding**: Revoking system credentials, generating final paycheck, updating status to `TERMINATED`.

### 2. Primary QA Validation Rules
- **Overtime Calculation**: Hours > 40/week must calculate at $1.5 \times \text{Hourly Rate}$.
- **Access Revocation**: When employee status transitions to `TERMINATED`, active SSO session MUST terminate within 60 seconds and block API authorization.

---

## 📊 Record-to-Report (R2R) Workflow

### 1. Business Process Stages
1. **Transaction Posting**: Journal entries posted across sub-ledgers (AP, AR, Fixed Assets).
2. **Period-End Closing**: Locking accounting period (e.g., Month-End August 2026).
3. **Financial Reconciliation**: Verifying Trial Balance ($\text{Total Debits} == \text{Total Credits}$).
4. **Financial Report Generation**: Generating Balance Sheet, Income Statement, Cash Flow statements.

### 2. Primary QA Validation Rules
- **Closed Period Posting Block**: Attempting to post a journal entry to a closed accounting period MUST return a validation error (`PERIOD_LOCKED`).
- **Trial Balance Integrity**: $\sum \text{Debits} - \sum \text{Credits} = 0.00$.

---

## 🔗 Related Topics
* [03. Procure-to-Pay (P2P) Workflow](03_procure_to_pay_p2p_workflow.md)
* [04. Order-to-Cash (O2C) Workflow](04_order_to_cash_o2c_workflow.md)
* [08. RBAC & SoD Testing](08_rbac_security_and_sod_testing.md)
