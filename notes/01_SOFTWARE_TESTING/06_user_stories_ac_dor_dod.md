---
title: User Stories, Acceptance Criteria, Definition of Ready (DoR) & Definition of Done (DoD)
category: 01_SOFTWARE_TESTING
subcategory: Agile Requirements
keywords:
  - User Stories
  - Acceptance Criteria
  - Given When Then
  - Gherkin
  - Definition of Ready
  - Definition of Done
  - DoR
  - DoD
audience:
  - Quality Engineer
  - Product Owner
  - Scrum Master
difficulty: beginner-intermediate
---

# 📜 User Stories, Acceptance Criteria, DoR & DoD Field Guide

## 🎯 Overview: Agile Requirements Engineering for QA

In Agile development, requirements are expressed as **User Stories** accompanied by **Acceptance Criteria (AC)**. To prevent low-quality inputs from stalling sprints, teams enforce quality gates: **Definition of Ready (DoR)** and **Definition of Done (DoD)**.

---

## ✍️ Writing Great User Stories & Acceptance Criteria

### 1. User Story Format
A standard User Story follows the template:
> **As a** `<role/user type>`  
> **I want** `<feature/action>`  
> **So that** `<business value/benefit>`

*Example*:  
*"As a Procurement Manager, I want to approve purchase orders exceeding $10,000 via email link so that procurement cycles are not delayed when I am traveling."*

---

### 2. Acceptance Criteria: Gherkin (Given-When-Then) Standard
Acceptance Criteria define the exact boundary conditions under which a story is considered complete. Using **Gherkin syntax** makes AC executable as automated test specifications.

```gherkin
Scenario: Manager approves high-value Purchase Order successfully
  Given a Purchase Order "PO-99421" exists with total amount $15,000
  And the Purchase Order status is "PENDING_APPROVAL"
  When the Manager clicks the approval link in the notification email
  Then the system updates Purchase Order status to "APPROVED"
  And an entry is logged in audit_logs with action "PO_APPROVED_VIA_EMAIL"
  And a confirmation message "Purchase Order approved successfully" is displayed
```

```gherkin
Scenario: Non-manager attempts to approve high-value Purchase Order
  Given a Purchase Order "PO-99421" exists with total amount $15,000
  And the logged-in user has role "Warehouse Specialist"
  When the user accesses the approval URL "/api/v1/po/PO-99421/approve"
  Then the API returns HTTP 403 Forbidden
  And the Purchase Order status remains "PENDING_APPROVAL"
```

---

## 🚦 Definition of Ready (DoR) vs. Definition of Done (DoD)

```
  ┌──────────────────────────────────────────────────────────────────┐
  │                 DEFINITION OF READY (DoR)                        │
  │  Gating criteria BEFORE a story enters a Sprint for development. │
  └────────────────────────────────┬─────────────────────────────────┘
                                   │
                                   ▼
  ┌──────────────────────────────────────────────────────────────────┐
  │                       DEVELOPMENT SPRINT                         │
  └────────────────────────────────┬─────────────────────────────────┘
                                   │
                                   ▼
  ┌──────────────────────────────────────────────────────────────────┐
  │                 DEFINITION OF DONE (DoD)                         │
  │  Gating criteria BEFORE a story is merged & marked Shippable.    │
  └──────────────────────────────────────────────────────────────────┘
```

### 1. Definition of Ready (DoR) Checklist
A story CANNOT enter a sprint unless:
- [ ] User story follows the standard format with clear business rationale.
- [ ] Acceptance Criteria are defined using Given-When-Then format covering happy path and edge cases.
- [ ] UI wireframes/Figma designs are finalized and linked.
- [ ] API contract endpoints/schemas are defined.
- [ ] QA has reviewed the story and provided effort estimation.
- [ ] Third-party dependencies are identified and available in test environment.

### 2. Definition of Done (DoD) Checklist
A story CANNOT be closed or released unless:
- [ ] Code matches developer coding standards and passes static analysis (SonarQube 0 code smells).
- [ ] Developers wrote unit tests with >80% code coverage.
- [ ] QA completed functional, boundary, and negative test execution.
- [ ] Playwright automated UI/API regression tests are written and passing in CI pipeline.
- [ ] Security checks (RBAC & authorization) are verified.
- [ ] Database migration scripts are executed and validated in Staging.
- [ ] Product Owner accepts the sprint demo.

---

## 🔗 Related Topics
* [03. SDLC, STLC & Methodologies](03_sdlc_stlc_agile_scrum_kanban.md)
* [07. Test Artifacts](07_test_artifacts_scenarios_cases_conditions.md)
* [01. Agile Ceremonies](../15_AGILE/01_agile_qa_scrum_kanban_ceremonies.md)
