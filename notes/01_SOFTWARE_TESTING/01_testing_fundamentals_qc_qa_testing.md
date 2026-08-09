---
title: Software Testing Fundamentals (QA vs QC vs Testing)
category: 01_SOFTWARE_TESTING
subcategory: Core Definitions
keywords:
  - Software Testing
  - Quality Assurance
  - Quality Control
  - QA vs QC
  - STLC
  - Defect Identification
audience:
  - Quality Engineer
  - Junior QA
  - SDET
difficulty: beginner
---

# 🧪 Software Testing Fundamentals: QA vs. QC vs. Testing

## 🎯 Overview & Core Definitions

In enterprise software development, the terms **Quality Assurance (QA)**, **Quality Control (QC)**, and **Software Testing** are frequently conflated. Understanding their precise definitions and operational scopes is essential for any Quality Engineer.

```
       ┌─────────────────────────────────────────────────────────────┐
       │                 QUALITY ASSURANCE (QA)                      │
       │  Process-oriented: Prevents defects before they occur.      │
       │  (Audits, Process Standards, Grooming, CI Gates)            │
       │                                                             │
       │   ┌─────────────────────────────────────────────────────┐   │
       │   │              QUALITY CONTROL (QC)                   │   │
       │   │  Product-oriented: Identifies defects in artifacts.   │   │
       │   │  (Code Reviews, Build Verification, Audits)         │   │
       │   │                                                     │   │
       │   │   ┌─────────────────────────────────────────────┐   │   │
       │   │   │             SOFTWARE TESTING                │   │   │
       │   │   │  Execution-oriented: Evaluates software     │   │   │
       │   │   │  against requirements (UI, API, DB tests).   │   │   │
       │   │   └─────────────────────────────────────────────┘   │   │
       │   └─────────────────────────────────────────────────────┘   │
       └─────────────────────────────────────────────────────────────┘
```

---

## 📊 Comprehensive Comparison Matrix

| Dimension | Quality Assurance (QA) | Quality Control (QC) | Software Testing |
| :--- | :--- | :--- | :--- |
| **Primary Focus** | Defect **Prevention** | Defect **Detection** | Defect **Identification** |
| **Orientation** | Process-oriented | Product-oriented | Execution-oriented |
| **Activity Type** | Proactive (Grooming, Standards) | Reactive (Inspection, Reviews) | Dynamic (Executing Test Cases) |
| **Scope** | Entire SDLC & Engineering Process | Deliverable Build Verification | Functional/Non-Functional Code |
| **Responsibility** | Whole Engineering Team | QC / QA Specialists | Testers & SDETs |
| **Key Example** | Establishing DoD & Code Review guidelines. | Inspecting build artifacts for release readiness. | Running Playwright tests against Staging API. |

---

## 🔍 Detailed Breakdown of Concepts

### 1. Quality Assurance (QA)
QA focuses on the **processes** used to build software. Its goal is to prevent defects from being introduced in the first place.
- **Activities**: Defining Definition of Ready (DoR) and Definition of Done (DoD), setting up CI/CD quality gates, standardizing coding guidelines, conducting retrospective process audits.
- **Mindset**: *"Is our development process designed to produce high quality reliably?"*

### 2. Quality Control (QC)
QC focuses on evaluating the **product quality** against defined quality standards before release.
- **Activities**: Technical inspections, peer code reviews, release candidate readiness audits, regression sign-offs.
- **Mindset**: *"Does this specific release candidate meet our quality standards?"*

### 3. Software Testing
Testing is the dynamic or static execution of system components to evaluate whether they satisfy specified requirements and identify differences between **Expected** and **Actual** results.
- **Activities**: Executing automated Playwright test suites, performing API postman checks, querying database state, executing boundary value test cases.
- **Mindset**: *"Does the software behave as expected when given specific inputs under specific conditions?"*

---

## 🏢 Enterprise Example: Procure-to-Pay (P2P) ERP Implementation

To see how these three operate together in an enterprise client project:

1. **QA Activity**: Defining a process requirement during Sprint Refinement that all Purchase Order API schemas must undergo contract verification before developer implementation starts.
2. **QC Activity**: Conducting a static review of the Purchase Order database migration scripts to verify foreign key constraints exist between `purchase_orders` and `vendors`.
3. **Testing Activity**: Automating a Playwright script that submits a Purchase Order with $1,000,000 value, verifying that the UI triggers an "Executive Approval Required" prompt and the DB status updates to `PENDING_APPROVAL`.

---

## 🛑 Common Misconceptions & Pitfalls

> [!WARNING]
> **Anti-Pattern**: Believing that "QA" means simply clicking buttons at the end of a sprint.
> **Correction**: Button clicking is manual test execution (Testing). True QA starts during initial product design and requirement writing.

---

## 🔗 Related Topics
* [02. Verification vs Validation](02_verification_vs_validation.md)
* [01. Quality Engineering vs QA](../02_QA_ENGINEERING/01_quality_engineering_vs_qa.md)
* [06. User Stories & Acceptance Criteria](06_user_stories_ac_dor_dod.md)
