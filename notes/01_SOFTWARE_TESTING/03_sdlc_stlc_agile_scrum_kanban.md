---
title: SDLC, STLC & Development Methodologies (Agile, Scrum, Kanban)
category: 01_SOFTWARE_TESTING
subcategory: Methodologies & Lifecycles
keywords:
  - SDLC
  - STLC
  - Waterfall
  - Agile
  - Scrum
  - Kanban
  - Software Development Lifecycle
  - Software Testing Lifecycle
audience:
  - Quality Engineer
  - SDET
  - Agile QA
difficulty: beginner-intermediate
---

# 🔄 SDLC, STLC & Methodologies: Waterfall vs. Agile vs. Scrum vs. Kanban

## 🎯 Overview: SDLC & STLC Relationship

The **Software Development Lifecycle (SDLC)** defines the overall process of planning, creating, testing, and deploying software.
The **Software Testing Lifecycle (STLC)** is the specialized sequence of testing activities embedded within the SDLC.

```
SDLC:  [Requirements] ──> [Design] ──> [Implementation] ──> [Testing] ──> [Deployment] ──> [Maintenance]
             │                │               │                │                 │
STLC:  [Req Analysis] ──> [Test Plan] ──> [Test Design] ──> [Test Execution] ──> [Defect Reporting] ──> [Closure]
```

---

## 🔁 The Phases of STLC

1. **Requirement Analysis**: Identify testable requirements, flag ambiguities, determine automation feasibility.
2. **Test Planning**: Define test strategy, tool stack (Playwright, Pytest, Postman), resource allocation, entry/exit criteria.
3. **Test Case Development**: Design detailed test cases, equivalence partitions, automated test scripts, and test data generators.
4. **Test Environment Setup**: Configure test databases, API mocks, CI runners, environment variables.
5. **Test Execution**: Execute automated suites and manual exploratory runs, log actual vs expected results.
6. **Defect Management**: Triage defects, report reproducing steps, verify fixes, perform regression.
7. **Test Cycle Closure**: Evaluate exit criteria, generate test summary reports, conduct retrospective analysis.

---

## 📊 Software Methodology Comparison

| Methodology | Waterfall | Agile (Scrum) | Kanban |
| :--- | :--- | :--- | :--- |
| **Delivery Model** | Sequential / Single Big Release | Timeboxed Iterations (Sprints, 2 weeks) | Continuous Flow / Pull System |
| **QA Role** | Gatekeeper at the end of project | Embedded team member throughout sprint | Continuous quality auditor per card |
| **Changes** | Difficult / Heavy Change Requests | Embraced during backlog grooming | Flexible anytime WIP limits allow |
| **Feedback Loop** | Months/Years | Days (Sprint Demos, Retros) | Hours/Days |
| **Automation Need**| Low to Moderate | **Mandatory** (Regression in every sprint) | **Mandatory** (Continuous Deployment) |

---

## 🏃 Agile Scrum Framework for QA Engineers

Scrum structures work into fixed-length iterations called **Sprints** (typically 2 weeks).

### Key Scrum Ceremonies & QA Involvement:

```
                ┌─────────────────────────────────────────────────────────┐
                │                SPRINT PLANNING (Day 1)                  │
                │ QA defines test effort, inputs DoR, estimates user stories│
                └────────────────────────────┬────────────────────────────┘
                                             │
                                             ▼
                ┌─────────────────────────────────────────────────────────┐
                │                 DAILY STANDUP (15 mins)                 │
                │ QA shares progress, blockers, defect status, CI status   │
                └────────────────────────────┬────────────────────────────┘
                                             │
                                             ▼
                ┌─────────────────────────────────────────────────────────┐
                │              BACKLOG GROOMING / REFINEMENT              │
                │ QA reviews user stories, defines Acceptance Criteria    │
                └────────────────────────────┬────────────────────────────┘
                                             │
                                             ▼
                ┌─────────────────────────────────────────────────────────┐
                │                SPRINT DEMO & RETROSPECTIVE              │
                │ QA demonstrates tested features & proposes process fixes │
                └─────────────────────────────────────────────────────────┘
```

---

## 🛑 Agile QA Anti-Patterns

> [!CAUTION]
> **"Mini-Waterfall inside a Sprint"**: Developers code for 9 days, then hand off everything to QA on Day 10.
> **Fix**: Shift-Left! QA collaborates on Day 1 by writing Playwright API automation stubs and test cases while developers write implementation code.

---

## 🔗 Related Topics
* [06. User Stories, AC, DoR & DoD](06_user_stories_ac_dor_dod.md)
* [01. Agile Ceremonies & QA Role](../15_AGILE/01_agile_qa_scrum_kanban_ceremonies.md)
* [02. Shift-Left & Shift-Right Testing](../02_QA_ENGINEERING/02_shift_left_and_shift_right.md)
