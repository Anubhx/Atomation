---
title: Defect Prevention & Root Cause Analysis (RCA)
category: 02_QA_ENGINEERING
subcategory: Process Improvement
keywords:
  - Defect Prevention
  - Root Cause Analysis
  - RCA
  - 5 Whys
  - Fishbone Diagram
  - Escape Analysis
audience:
  - Quality Engineer
  - Test Lead
  - Engineering Manager
difficulty: intermediate
---

# 🔍 Defect Prevention & Root Cause Analysis (RCA)

## 🎯 Overview: Fixing the Process, Not Just the Bug

A Quality Engineer does not simply log bugs; a QE investigates **why** the bug was created and **how** to prevent an entire class of similar bugs from occurring in the future. This process is called **Root Cause Analysis (RCA)**.

---

## 🛠️ Practical RCA Methodologies

### 1. The "5 Whys" Technique
Asking "Why?" five consecutive times to drill past superficial symptoms down to the process breakdown.

#### Real Enterprise Example: Production Outage in ERP Payment Gateway
1. **Why did production fail?** → Vendor payments threw 500 Internal Server Errors for 2 hours.
2. **Why were 500 errors thrown?** → The payment API timed out trying to connect to the third-party Tax service.
3. **Why did it time out?** → The API request timeout was hardcoded to 120 seconds with zero retry logic.
4. **Why was there no retry or circuit breaker?** → The developer did not implement resilience patterns when building the HTTP client.
5. **Why was resilience omitted?** → The non-functional requirements for API resilience were never defined in the User Story DoR, and code review did not check network resilience.

**Preventative Action Items**:
- Update DoR checklist to require explicit timeout/retry specs for third-party HTTP clients.
- Implement Resilience4j / Tenacity circuit breaker in payment backend microservice.
- Add mock network latency test cases in Playwright/Pytest suite.

---

### 2. The Fishbone (Ishikawa) Diagram Strategy
Categorizing potential failure causes across:
- **Requirements**: Ambiguous specifications, missing acceptance criteria.
- **Environment**: Staging database out of sync with production schemas.
- **Tooling/Automation**: Flaky locators masking real backend failures.
- **Process**: Missing peer code reviews, rushed deployments before weekend.

---

## 🔗 Related Topics
* [01. Quality Engineering vs QA](01_quality_engineering_vs_qa.md)
* [01. Defect Lifecycle & Severity](../16_DEFECT_MANAGEMENT/01_defect_lifecycle_severity_priority.md)
* [02. Shift-Left & Shift-Right Testing](02_shift_left_and_shift_right.md)
