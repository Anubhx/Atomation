---
title: Defect Lifecycle, Severity & Priority Matrix
category: 16_DEFECT_MANAGEMENT
subcategory: Defect Management
keywords:
  - Defect Lifecycle
  - Severity vs Priority
  - Bug Life Cycle
  - Defect Triage
  - Reproducibility
audience:
  - Quality Engineer
  - SDET
  - Scrum Team
difficulty: beginner-intermediate
---

# 🐞 Defect Lifecycle, Severity & Priority Matrix

## 🎯 Overview: Defect State Transition Lifecycle

A defect follows a standardized state transition model from initial identification by QA to resolution by engineering and final verification.

```
 [ NEW ] ──(Triage)──> [ OPEN ] ──(Assign)──> [ IN_PROGRESS ] ──(Fix)──> [ RESOLVED ]
   │                     │                                                     │
(Duplicate/              │                                              (QA Verification)
 Invalid)                ▼                                                     │
   │               [ REJECTED ]                                      ┌─────────┴─────────┐
   ▼                                                                 ▼                   ▼
 [ CLOSED ] <───────────────────────────────────────────────── [ VERIFIED ]       [ REOPENED ]
```

---

## ⚖️ Severity vs. Priority Distinction

* **Severity**: The technical/operational impact of the bug on system functionality. (Set by QA).
* **Priority**: The business urgency of fixing the bug in relation to release goals. (Set by Product Owner/Lead).

```
                      SEVERITY (Technical Impact)
                 Low             Medium            High/Blocker
             ┌──────────────┬──────────────┬──────────────────────────┐
    High (5) │ High Priority│ High Priority│   CRITICAL PRIORITY      │
             │ Low Severity │ Med Severity │   High Severity          │
             │ (e.g. Logo   │ (e.g. Broken │  (e.g. P2P Payment Engine│
PRIORITY     │  typo on     │  checkout    │   throwing 500 error)    │
(Business    │  homepage)   │  filter)     │                          │
Urgency)     ├──────────────┼──────────────┼──────────────────────────┤
     Low (1) │ Low Priority │ Low Priority │   High Severity          │
             │ Low Severity │ Med Severity │   Low Priority           │
             │ (e.g. Minor  │ (e.g. Admin  │  (e.g. Crash in legacy   │
             │ alignment)   │ export typo) │   IE11 browser)          │
             └──────────────┴──────────────┴──────────────────────────┘
```

---

## 🔗 Related Topics
* [02. High-Impact Bug Report Writing](02_bug_report_templates_good_vs_bad.md)
* [03. Industry Bug Report Template](../25_TEMPLATES/03_bug_report_template.md)
* [Bug Reporting Cheat Sheet](../21_CHEAT_SHEETS/cheat-sheet-bug-reporting.md)
