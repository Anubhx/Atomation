---
title: Test Pyramid vs Test Trophy Frameworks
category: 02_QA_ENGINEERING
subcategory: Automation Strategy
keywords:
  - Test Pyramid
  - Test Trophy
  - Automation Strategy
  - Integration Tests
  - Unit Tests
  - End-to-End Tests
audience:
  - Quality Engineer
  - SDET
  - Software Architect
difficulty: intermediate
---

# 🔺 Test Pyramid vs. Test Trophy: Automation Strategy

## 🎯 Overview & Framework Comparison

Automated testing strategies determine where an engineering team invests its automation efforts. Two prominent models exist: Mike Cohn's **Test Pyramid** and Kent C. Dodds' **Test Trophy**.

```
       TEST PYRAMID                                TEST TROPHY
         /\                                           ┌───┐
        /  \  <── E2E (UI)                           │E2E│  <── Static / Smoke (Top)
       /----\                                      ┌──┴───┴──┐
      / Inte \ <── Integration                     │         │
     /  gration\                                   │ INTEGR- │  <── Integration Tests (Heavy Body)
    /------------\                                 │  ATION  │
   /   Unit       \ <── Unit Tests (Base)          └──┬───┬──┘
  /----------------\                                  │Unit │  <── Unit Tests
                                                      └───┘
```

---

## 📊 Detailed Model Comparison

| Dimension | The Test Pyramid | The Test Trophy |
| :--- | :--- | :--- |
| **Primary Level** | **Unit Tests** (Base of pyramid) | **Integration Tests** (Middle body) |
| **Core Philosophy**| Catch bugs closest to code unit; speed & low execution cost. | Test user behavior and component boundaries; maximum confidence. |
| **Best Suited For**| Algorithmic backends, SDKs, math/financial calculation libraries. | Web applications, REST APIs, Microservices, ERP web portals. |
| **Fragility Risk** | Low (Tests unit logic in memory). | Moderate (Requires reliable test data and mock isolation). |
| **Confidence Level**| Low-Medium (Passing unit tests doesn't guarantee UI connects to API). | **High** (Validates real component and API contracts together). |

---

## 🔬 Enterprise QA Guidance

1. **For ERP & Business Applications**: Adopt the **Test Trophy** mindset. Unit tests verify specific validation algorithms (e.g., tax calculation), but **Integration API tests** (verifying HTTP requests, schema compliance, DB commits) deliver the highest ROI per test case.
2. **Reserving E2E UI Tests**: Limit Playwright UI E2E tests to core revenue-critical workflows (e.g., Procure-to-Pay, Order-to-Cash, Login/SSO). UI tests are expensive to run and maintain.

---

## 🔗 Related Topics
* [01. Quality Engineering vs QA](01_quality_engineering_vs_qa.md)
* [04. Testing Levels](../01_SOFTWARE_TESTING/04_testing_levels.md)
* [03. Combined UI+API+DB Testing](../10_AUTOMATION_ARCHITECTURE/03_combined_ui_api_db_testing_pattern.md)
