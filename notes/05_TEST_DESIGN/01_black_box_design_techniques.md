---
title: Black-Box Test Design Techniques (EP, BVA, Decision Tables, State Transition)
category: 05_TEST_DESIGN
subcategory: Design Techniques
keywords:
  - Equivalence Partitioning
  - Boundary Value Analysis
  - BVA
  - Decision Tables
  - State Transition
  - Pairwise Testing
  - Error Guessing
audience:
  - Quality Engineer
  - SDET
  - Manual Tester
difficulty: intermediate
---

# 📐 Black-Box Test Design Techniques Field Guide

## 🎯 Overview & Purpose

Test design techniques provide mathematical and systematic frameworks to derive optimal test cases-achieving maximum requirement coverage with minimum redundant test execution.

---

## 1. Equivalence Partitioning (EP)

### Definition
Dividing input data into valid and invalid partitions where the system is expected to process all values within a partition identically.

### Practical Enterprise Example: Age Eligibility for Corporate Loan (Valid: 18 - 65)
* **Valid Partition**: `18 <= Age <= 65` (Test values: `25`, `40`)
* **Invalid Partition 1 (Too young)**: `Age < 18` (Test value: `15`)
* **Invalid Partition 2 (Too old)**: `Age > 65` (Test value: `70`)

---

## 2. Boundary Value Analysis (BVA)

### Definition
Testing at the boundaries between partitions. Errors occur predominantly at partition edges.

### 2-Point vs. 3-Point Boundary Technique (Range: 18 to 65)
* **2-Point BVA**: Min (`18`), Min-1 (`17`), Max (`65`), Max+1 (`66`).
* **3-Point BVA**: Min-1 (`17`), Min (`18`), Min+1 (`19`), Max-1 (`64`), Max (`65`), Max+1 (`66`).

---

## 3. Decision Table Testing

### Definition
Mapping complex business logic rules into a matrix of Condition Inputs ($\text{C}_1, \text{C}_2$) against Action Outputs ($\text{A}_1, \text{A}_2$).

### Decision Table Matrix: E-Commerce Discount Rules

| Conditions / Rules | Rule 1 | Rule 2 | Rule 3 | Rule 4 |
| :--- | :---: | :---: | :---: | :---: |
| **User is VIP Member?** | Y | Y | N | N |
| **Order Total > $500?** | Y | N | Y | N |
| **Actions** | | | | |
| **Apply 20% Discount** | ✅ | ❌ | ❌ | ❌ |
| **Apply 10% Discount** | ❌ | ✅ | ✅ | ❌ |
| **Apply Free Shipping** | ✅ | ✅ | ✅ | ❌ |

---

## 4. State Transition Testing

### Definition
Modeling system behavior as a state machine transitioning between states upon receiving specific events.

```
 [ DRAFT ] ──(Submit)──> [ PENDING_APPROVAL ] ──(Approve)──> [ APPROVED ]
                                │
                            (Reject)
                                │
                                ▼
                           [ REJECTED ] ──(Resubmit)──> [ PENDING_APPROVAL ]
```

---

## 5. Pairwise (All-Pairs) Testing & Error Guessing

* **Pairwise**: Testing all possible discrete pairs of input parameters (reduces combinations from $10 \times 10 \times 10 = 1000$ to ~25 tests).
* **Error Guessing**: Using QA experience to target historical weak points (e.g., paste long strings, emoji characters, SQL injection snippets `' OR '1'='1`).

---

## 🔗 Related Topics
* [02. Exploratory & Risk-Based Design](02_exploratory_and_risk_based_design.md)
* [07. ERP Scenario Library](../03_ERP_TESTING/07_erp_scenario_library.md)
* [Test Design Cheat Sheet](../21_CHEAT_SHEETS/cheat-sheet-test-design.md)
