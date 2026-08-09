---
title: Risk-Based Testing Strategy
category: 02_QA_ENGINEERING
subcategory: Test Optimization
keywords:
  - Risk-Based Testing
  - Risk Matrix
  - Test Prioritization
  - Impact vs Likelihood
  - QA Strategy
audience:
  - Quality Engineer
  - Test Lead
  - SDET
difficulty: intermediate
---

# 🎯 Risk-Based Testing (RBT) Strategy

## 🎯 Overview & Core Formula

In complex enterprise platforms, executing 100% of test cases on every minor release is impossible due to time and resource constraints. **Risk-Based Testing (RBT)** prioritizes test design and execution based on business exposure and likelihood of failure.

$$\text{Risk Exposure Score} = \text{Probability of Failure (1-5)} \times \text{Business Impact of Failure (1-5)}$$

---

## 📊 The Enterprise Risk Matrix

```
                       BUSINESS IMPACT OF FAILURE
                 Low (1)      Medium (3)     High (5)
             ┌──────────────┬──────────────┬──────────────┐
    High (5) │  MEDIUM (5)  │  HIGH (15)   │ CRITICAL (25)│  <── Sanity & Nightly Regression
PROBABILITY  ├──────────────┼──────────────┼──────────────┤
  OF FAILURE │   LOW (3)    │  MEDIUM (9)  │  HIGH (15)   │
             ├──────────────┼──────────────┼──────────────┤
     Low (1) │  IGNORE (1)  │   LOW (3)    │  MEDIUM (5)  │  <── Ad-hoc / Sprint End
             └──────────────┴──────────────┴──────────────┘
```

---

## 📋 Category Risk Classification Guide

| Risk Level | Score Range | Testing Action / Pipeline Allocation |
| :--- | :--- | :--- |
| **CRITICAL (25)** | 20 - 25 | **Mandatory Pull Request CI Gate**: Automated E2E & API regression blocking merge. |
| **HIGH (12-19)** | 12 - 19 | **Nightly Automated Regression**: Automated Playwright suites running scheduled runs. |
| **MEDIUM (5-11)**| 5 - 11 | **Sprint Execution**: Covered during feature sprint testing and manual exploratory runs. |
| **LOW (1-4)** | 1 - 4 | **Low Priority**: Tested if time permits; excluded from automated CI gates. |

---

## 🔬 Practical Enterprise Risk Assessment Example

### ERP System Features Risk Ranking

1. **Procure-to-Pay 3-Way Invoice Matching Engine**:
   - *Probability*: 4 (Complex logic, frequent custom rules).
   - *Impact*: 5 (Financial ledger corruption, erroneous vendor payouts).
   - *Risk Score*: $4 \times 5 = 20 \rightarrow$ **CRITICAL RISK**. (Must automate in PR pipeline).

2. **User Profile Picture Avatar Upload**:
   - *Probability*: 2 (Standard upload component).
   - *Impact*: 1 (Cosmetic display issue).
   - *Risk Score*: $2 \times 1 = 2 \rightarrow$ **LOW RISK**. (Manual check during story testing).

---

## 🔗 Related Topics
* [02. Shift-Left & Shift-Right Testing](02_shift_left_and_shift_right.md)
* [05. Quality Gates & CI/CD](05_quality_gates_and_ci_cd.md)
* [01. Black-Box Test Design](../05_TEST_DESIGN/01_black_box_design_techniques.md)
