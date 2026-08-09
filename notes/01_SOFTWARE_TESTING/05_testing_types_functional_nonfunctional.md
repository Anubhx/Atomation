---
title: Software Testing Types (Functional & Non-Functional Breakdown)
category: 01_SOFTWARE_TESTING
subcategory: Testing Types
keywords:
  - Functional Testing
  - Non-Functional Testing
  - Regression Testing
  - Retesting
  - Smoke Testing
  - Sanity Testing
  - Exploratory Testing
  - Compatibility Testing
  - Usability Testing
  - Accessibility Testing
  - Security Testing
  - Performance Testing
audience:
  - Quality Engineer
  - SDET
  - Manual Tester
difficulty: beginner-intermediate
---

# 🎨 Software Testing Types: Functional vs. Non-Functional Field Guide

## 🎯 Overview & Classification

Testing types describe **what** attribute of the software is being evaluated. Broadly, testing types are divided into **Functional** ("What the system does") and **Non-Functional** ("How well the system performs").

```
                              ┌─────────────────────────────────────────┐
                              │          SOFTWARE TESTING TYPES         │
                              └────────────────────┬────────────────────┘
                                                   │
                   ┌───────────────────────────────┴───────────────────────────────┐
                   │                                                               │
    ┌──────────────┴──────────────┐                                 ┌──────────────┴──────────────┐
    │     FUNCTIONAL TESTING      │                                 │   NON-FUNCTIONAL TESTING    │
    │   (Behavior & Workflows)    │                                 │ (Quality Attributes & Performance)│
    └──────────────┬──────────────┘                                 └──────────────┬──────────────┘
                   │                                                               │
    ├── Smoke / Sanity Testing                                       ├── Performance (Load/Stress)
    ├── Regression Testing                                           ├── Security (RBAC/Auth/IDOR)
    ├── Retesting                                                    ├── Accessibility (WCAG / a11y)
    ├── Exploratory Testing                                          ├── Usability & UX
    └── System / E2E Testing                                         └── Compatibility & Localization
```

---

## 📋 Comprehensive Testing Types Reference

### 1. Functional Testing Types

| Testing Type | Purpose / Definition | When to Use | Enterprise Example |
| :--- | :--- | :--- | :--- |
| **Smoke Testing** | High-level build verification test (BVT) ensuring critical path works. | Immediately after new build deployment to QA/Staging. | Verifying login, homepage render, and API ping return HTTP 200 before running full test suite. |
| **Sanity Testing** | Quick unscripted check focusing on a specific bug fix or narrow feature area. | After minor bug fix or patch release. | Verifying that modifying tax calculation on Invoice step 3 no longer causes NaN errors. |
| **Retesting** | Executing specific test cases that previously failed to confirm fix. | When developer marks bug state as `RESOLVED`. | Re-running test case `TC_PAY_042` to verify credit card decline error message displays. |
| **Regression Testing**| Verifying that recent code changes have NOT broken existing features. | Before every release candidate or pull request merge. | Running full 500-scenario automated Playwright regression suite on Staging. |
| **Exploratory Testing**| Unscripted, creative testing driven by tester intuition and domain knowledge. | Throughout sprint, especially after major feature completion. | Trying concurrent form submissions, double-clicks, dynamic browser back button navigation. |

---

### 2. Non-Functional Testing Types

| Testing Type | Purpose / Definition | Key Tools | Enterprise Example |
| :--- | :--- | :--- | :--- |
| **Performance** | Evaluating speed, responsiveness, throughput, and stability under load. | k6, JMeter, Locust | Simulating 5,000 concurrent ERP users placing orders during Black Friday sale. |
| **Security** | Identifying vulnerabilities, access control flaws, and data exposure risks. | OWASP ZAP, Postman | Checking if `Buyer` role user can call `DELETE /api/v1/admin/users/1` (IDOR / Privilege Escalation). |
| **Accessibility (a11y)**| Ensuring software usable by people with disabilities (WCAG 2.1 AA). | axe-core, Playwright | Verifying all form fields have explicit `<label>` tags and high-contrast color ratios (>4.5:1). |
| **Usability** | Evaluating how intuitive and user-friendly the user interface is. | User feedback, Analytics | Checking if a user can complete purchase order approval in under 3 clicks. |
| **Compatibility** | Ensuring app works across various browsers, OS, and viewport sizes. | Playwright, BrowserStack | Testing ERP portal on Chrome (Mac), Edge (Windows), Safari (iOS), and Firefox (Linux). |

---

## 🆚 Critical Distinction: Smoke vs. Sanity vs. Regression vs. Retesting

```
                     ┌──────────────────────────────────────────────┐
                     │          NEW BUILD DEPLOYED TO QA            │
                     └──────────────────────┬───────────────────────┘
                                            │
                                            ▼
                     ┌──────────────────────────────────────────────┐
                     │  SMOKE TEST: Does critical path work?         │
                     │  (Pass: Proceed | Fail: Reject Build)        │
                     └──────────────────────┬───────────────────────┘
                                            │
                                            ▼
                     ┌──────────────────────────────────────────────┐
                     │  RETESTING: Did specific bug fixes work?      │
                     └──────────────────────┬───────────────────────┘
                                            │
                                            ▼
                     ┌──────────────────────────────────────────────┐
                     │  SANITY TEST: Did bug fix break nearby code?  │
                     └──────────────────────┬───────────────────────┘
                                            │
                                            ▼
                     ┌──────────────────────────────────────────────┐
                     │  REGRESSION TEST: Did overall system remain  │
                     │  unaffected across all modules?              │
                     └──────────────────────────────────────────────┘
```

---

## 🔗 Related Topics
* [04. Testing Levels](04_testing_levels.md)
* [01. Playwright Automation Architecture](../08_PLAYWRIGHT/01_playwright_python_setup_architecture.md)
* [01. QA Security Testing](../13_SECURITY/01_qa_security_testing_rbac_idor_session_inputs.md)
