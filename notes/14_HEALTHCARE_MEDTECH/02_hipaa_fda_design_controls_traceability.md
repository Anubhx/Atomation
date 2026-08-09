---
title: Regulatory Concepts: HIPAA, FDA, Design Controls & Traceability Matrix
category: 14_HEALTHCARE_MEDTECH
subcategory: Regulatory QA
keywords:
  - HIPAA
  - FDA 21 CFR Part 820
  - Design Controls
  - Traceability Matrix
  - CAPA
  - Change Control
audience:
  - Quality Engineer
  - MedTech QA Specialist
  - Software Validation Engineer
difficulty: advanced
---

# 📜 Regulatory Concepts: HIPAA, FDA, Design Controls & Traceability

> [!NOTE]
> **REGULATORY DISCLAIMER**: This guide presents standard regulatory engineering concepts. It does not constitute legal or regulatory compliance advice. Mark all organizational procedures as *"Verify against current company QMS procedures and applicable regulations."*

---

## 🏛️ Key MedTech Regulatory Frameworks

```
 [ ISO 13485 / FDA 21 CFR Part 820 ] ──> Medical Device Quality System Regulations (QMS).
 [ FDA 21 CFR Part 11 ] ──────────────> Electronic Records & Electronic Signatures (ERES).
 [ HIPAA Privacy & Security Rule ] ───> Protection of Protected Health Information (PHI).
```

---

## 📊 Design Controls & The V-Model Alignment

MedTech software development requires bidirectional **Traceability** from User Needs down to Test Evidence.

```
 [ User Needs ] ──────────────────────────────────────────────> [ User Validation Testing (UAT) ]
       │                                                                      ▲
       ▼                                                                      │
 [ Software Requirements (SRS) ] ───────────────────────────> [ System / Integration Testing ]
       │                                                                      ▲
       ▼                                                                      │
 [ Software Design Spec (SDS) ] ────────────────────────────> [ Unit & Component Testing ]
```

---

## 📋 The Requirement Traceability Matrix (RTM)

A **Requirements Traceability Matrix (RTM)** proves that 100% of software requirements have corresponding design specifications, automated test cases, and passing execution evidence.

| User Need ID | Software Req (SRS) | Design Spec (SDS) | Test Case ID | Test Execution Evidence | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `UN-DOSE-01` | `SRS-ALG-991` | `SDS-MATH-04` | `TC_MED_041` | `EXEC_PASS_20260809.log` | **VERIFIED** |

---

## 🛠️ CAPA (Corrective and Preventive Action) Basics

When a critical safety defect or QMS non-conformance is identified:
1. **Correction**: Immediate fix/containment of the defect.
2. **Root Cause Analysis**: Investigating process breakdown.
3. **Preventive Action**: Updating procedures or automated quality gates to ensure the failure mode cannot recur.

---

## 🔗 Related Topics
* [01. Healthcare QA Fundamentals](01_healthcare_medtech_qa_fundamentals.md)
* [Healthcare QA Cheat Sheet](../21_CHEAT_SHEETS/cheat-sheet-healthcare-qa.md)
