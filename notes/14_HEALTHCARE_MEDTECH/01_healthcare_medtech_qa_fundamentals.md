---
title: Healthcare & MedTech Software QA Fundamentals
category: 14_HEALTHCARE_MEDTECH
subcategory: Healthcare QA
keywords:
  - Healthcare QA
  - MedTech Testing
  - Patient Safety
  - Medical Device Software
  - Software Lifecycle
  - Audit Trails
audience:
  - Quality Engineer
  - MedTech QA Specialist
  - Software Validation Engineer
difficulty: intermediate
---

# 🏥 Healthcare & MedTech Software QA Fundamentals

> [!NOTE]
> **REGULATORY DISCLAIMER**: This document serves as an engineering overview of healthcare quality practices. Regulatory requirements vary by regional jurisdiction and device classification. Always verify specific implementation details against current company Quality Management System (QMS) procedures and applicable regulations.

---

## 🎯 Overview: Patient Safety as the Primary Metric

In Healthcare, EHR (Electronic Health Record) systems, and Medical Device Software (SaMD - Software as a Medical Device), a software defect does not merely cause financial loss—it can directly compromise **Patient Safety**.

```
  ┌─────────────────────────────────────────────────────────────┐
  │                   MEDTECH QA CORE TRIAD                     │
  └──────────────────────────────┬──────────────────────────────┘
                                 │
     ┌───────────────────────────┼───────────────────────────┐
     ▼                           ▼                           ▼
┌──────────────┐          ┌──────────────┐          ┌──────────────┐
│PATIENT SAFETY│          │DATA INTEGRITY│          │TRACEABILITY  │
│ Zero harm to │          │ HIPAA & PHI  │          │Req -> Test ->│
│ patients     │          │ Privacy      │          │Evidence      │
└──────────────┘          └──────────────┘          └──────────────┘
```

---

## 📋 Core Principles of Healthcare Software QA

1. **Patient Safety Centricity**: Software algorithms calculating drug dosages, patient vitals, or diagnostic imaging must undergo rigorous boundary value testing.
2. **Strict Immutable Audit Trails**: System logs must record every read, write, modification, or deletion of Patient Health Information (PHI)—storing `user_id`, `timestamp`, `ip_address`, and `action`.
3. **Data Privacy (HIPAA Compliance)**: PHI data must be encrypted at rest (AES-256) and in transit (TLS 1.3), and masked in test environments.

---

## 🔗 Related Topics
* [02. HIPAA, FDA, Design Controls & Traceability](02_hipaa_fda_design_controls_traceability.md)
* [Healthcare QA Cheat Sheet](../21_CHEAT_SHEETS/cheat-sheet-healthcare-qa.md)
