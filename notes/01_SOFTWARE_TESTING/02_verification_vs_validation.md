---
title: Verification vs Validation in Software Engineering
category: 01_SOFTWARE_TESTING
subcategory: Core Definitions
keywords:
  - Verification
  - Validation
  - Static Testing
  - Dynamic Testing
  - Requirements Verification
  - System Validation
audience:
  - Quality Engineer
  - SDET
  - MedTech QA
difficulty: beginner-intermediate
---

# ⚖️ Verification vs. Validation: Enterprise QA Perspective

## 🎯 Overview & Classic Definitions

The distinction between **Verification** and **Validation** is central to software engineering, regulated systems (Healthcare/MedTech), and enterprise quality audits.

```
       ┌─────────────────────────────────────────────────────────────┐
       │                       VERIFICATION                          │
       │  "Are we building the product RIGHT?"                       │
       │  Static activities checking process & requirements.         │
       │  (Code Reviews, Schema Audits, Architecture Inspections)    │
       └──────────────────────────────┬──────────────────────────────┘
                                      │
                                      ▼
       ┌─────────────────────────────────────────────────────────────┐
       │                        VALIDATION                           │
       │  "Are we building the RIGHT product?"                       │
       │  Dynamic activities checking operational user needs.         │
       │  (System Testing, API E2E Workflows, UAT, Performance)      │
       └─────────────────────────────────────────────────────────────┘
```

---

## 📊 Verification vs. Validation Comparison Matrix

| Feature | Verification | Validation |
| :--- | :--- | :--- |
| **Core Question** | *"Are we building the product right?"* | *"Are we building the right product?"* |
| **Execution State** | **Static** (No code execution) | **Dynamic** (Executing system code) |
| **Focus** | Specifications, designs, architecture, documents | Real operational behavior and user needs |
| **Evaluation Method** | Reviews, walkthroughs, static code analysis, inspections | Functional testing, integration tests, E2E automation, UAT |
| **Timing** | Early in SDLC (Shift-Left) | Mid-to-Late SDLC (Build verification, release readiness) |
| **Primary Artifacts** | Requirement Specifications (SRS), Design Docs, ER Diagrams | Running Application (Staging, Pre-prod, UAT environments) |

---

## 🔬 Practical Enterprise Examples

### Enterprise ERP Scenario: Vendor Payment Processing

1. **Verification Activities**:
   - Inspecting the Jira User Story to ensure explicit boundary values exist for high-value payments ($50,000+).
   - Reviewing OpenAPI/Swagger documentation to confirm the `POST /api/v1/payments` schema includes mandatory currency codes (`USD`, `EUR`).
   - Running static code analysis (SonarQube) to catch hardcoded secrets or unhandled SQL exceptions.

2. **Validation Activities**:
   - Submitting a $75,000 vendor payment via Playwright automation and validating that the financial ledger updates correctly.
   - Performing API testing with invalid currencies (`XYZ`) and confirming HTTP 422 Unprocessable Entity responses.
   - Conducting User Acceptance Testing (UAT) with Finance Executives to confirm the approval workflow matches real business operations.

---

## 🏥 MedTech & Regulated System Context

In Healthcare and Medical Device software (FDA 21 CFR Part 820 / ISO 13485):

* **Software Verification**: Demonstrates that the software output of a design phase meets the input requirements specified (e.g., verifying software code conforms to software design specifications).
* **Software Validation**: Demonstrates that software satisfies intended use and user needs in its actual operating environment (e.g., validating that clinician workflow software prevents improper drug dosing under load).

---

## 🛑 Common Failure Modes

* **Failing Verification, Passing Validation**: You build software that satisfies the user's manual expectations, but the underlying database schema violates normalization or lacks foreign keys, leading to data corruption later.
* **Passing Verification, Failing Validation**: You perfectly implement a flawed specification. The code matches the user story 100%, but the business process fails because the user story missed an edge case.

---

## 🔗 Related Topics
* [01. Testing Fundamentals](01_testing_fundamentals_qc_qa_testing.md)
* [04. Testing Levels](04_testing_levels.md)
* [02. Regulatory Concepts in MedTech](../14_HEALTHCARE_MEDTECH/02_hipaa_fda_design_controls_traceability.md)
