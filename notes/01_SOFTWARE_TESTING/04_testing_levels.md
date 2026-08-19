---
title: Software Testing Levels (Unit, Component, Integration, System, E2E, UAT)
category: 01_SOFTWARE_TESTING
subcategory: Testing Hierarchy
keywords:
  - Testing Levels
  - Unit Testing
  - Component Testing
  - Integration Testing
  - System Testing
  - End-to-End Testing
  - Acceptance Testing
  - UAT
audience:
  - Quality Engineer
  - SDET
  - Software Engineer
difficulty: beginner-intermediate
---

# 🪜 Software Testing Levels: From Unit to Acceptance Testing

## 🎯 Overview: The Testing Hierarchy

Software testing is structured in progressive levels. Each level targets a different scope, abstraction, and set of failure risks.

```
                  ┌──────────────────────────────────────────┐
                  │        USER ACCEPTANCE TESTING (UAT)     │
                  │   Business validation & user workflows   │
                  └────────────────────┬─────────────────────┘
                                       │
                  ┌────────────────────┴─────────────────────┐
                  │            SYSTEM TESTING (E2E)          │
                  │  Integrated system: UI, API, DB, Cloud    │
                  └────────────────────┬─────────────────────┘
                                       │
                  ┌────────────────────┴─────────────────────┐
                  │            INTEGRATION TESTING           │
                  │ Component interactions & API interfaces   │
                  └────────────────────┬─────────────────────┘
                                       │
                  ┌────────────────────┴─────────────────────┐
                  │            COMPONENT / UNIT TESTING      │
                  │   Isolated functions, classes & modules   │
                  └──────────────────────────────────────────┘
```

---

## 📊 Comprehensive Level Breakdown

| Testing Level | Scope | Who Executes? | Primary Tools | Execution Speed | Cost of Defect Fix |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Unit Testing** | Individual functions, methods, or classes in isolation. | Developers | pytest, JUnit, Jest | Milliseconds | Extremely Low |
| **Component Testing** | Individual UI widgets or microservices with mocked dependencies. | Developers / SDETs | Storybook, Pytest-mock | Fast (Seconds) | Low |
| **Integration Testing**| Interface between two or more modules (e.g., Service A calling DB or Service B API). | SDETs / Quality Engineers | Pytest, Requests, Postman | Medium (Seconds) | Moderate |
| **System Testing** | Full integrated application against functional requirements. | Quality Engineers | Playwright, Selenium | Slow (Minutes) | High |
| **End-to-End (E2E)** | Complete business user journeys across multiple applications (e.g., Web UI → ERP → Payment Gateway → Email). | Quality Engineers | Playwright Python, Cypress | Slowest | Very High |
| **Acceptance (UAT)**| Business users validating product against real business needs. | Product Owners / End Users | Manual execution / Demo | Manual | Critical |

---

## 🔬 Practical Enterprise Scenarios

### ERP Procure-to-Pay (P2P) Level Mapping

1. **Unit Test**: Testing the `calculate_tax(amount, region)` Python function inside the pricing module to ensure $100 in region `US_CA` yields $107.25.
2. **Integration Test**: Invoking `POST /api/v1/purchase-orders` and verifying the backend creates a database row in `purchase_orders` with foreign keys referencing `vendors`.
3. **System Test**: Logging into the Web ERP, navigating to Procurement, submitting a Purchase Requisition, and ensuring the requisition status updates to `SUBMITTED`.
4. **End-to-End Test**: Creating a Purchase Order in the Web ERP via Playwright UI, approving it via Manager API, triggering Goods Receipt via Warehouse API, verifying the Invoice via SQL, and checking Payment dispatch in Stripe mock.
5. **Acceptance Test (UAT)**: Procurement Lead logging in to execute an actual monthly purchasing cycle before go-live sign-off.

---

## 🛑 Common Pitfalls

> [!WARNING]
> **"Ice Cream Cone" Anti-Pattern**: Writing zero Unit/Integration tests and attempting to cover 100% of application logic via heavy, slow, fragile End-to-End UI tests.
> **Solution**: Follow the **Test Pyramid**-place the majority of tests at Unit and Integration levels, reserving E2E UI tests for critical user journeys.

---

## 🔗 Related Topics
* [05. Testing Types](05_testing_types_functional_nonfunctional.md)
* [04. Test Pyramid & Trophy](../02_QA_ENGINEERING/04_test_pyramid_and_trophy.md)
* [03. Combined UI+API+DB Pattern](../10_AUTOMATION_ARCHITECTURE/03_combined_ui_api_db_testing_pattern.md)
