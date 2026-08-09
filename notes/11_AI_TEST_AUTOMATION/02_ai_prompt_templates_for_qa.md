---
title: Battle-Tested QA AI Prompt Templates
category: 11_AI_TEST_AUTOMATION
subcategory: AI Prompt Engineering
keywords:
  - QA Prompts
  - AI Prompt Templates
  - Test Case Generation Prompt
  - Playwright Refactoring Prompt
  - SQL QA Prompt
audience:
  - Quality Engineer
  - SDET
difficulty: beginner-intermediate
---

# 🤖 Battle-Tested QA AI Prompt Templates

## 🎯 Overview: Prompt Engineering for QA Engineers

To get precise, production-grade outputs from LLMs, structure prompts using the **Role-Context-Instruction-Constraint-Output (RCICO)** framework.

---

## 📋 Ready-to-Use Enterprise QA Prompt Templates

### 1. Template: "Generate Test Cases from Requirement"
```text
ROLE: Senior Quality Engineering Architect.
CONTEXT: We are building an enterprise ERP Procure-to-Pay system.
REQUIREMENT: [Paste User Story & Acceptance Criteria here]
INSTRUCTION: Generate a comprehensive test case matrix covering Happy Path, Boundary Values (BVA), Equivalence Partitions (EP), and Negative Scenarios.
CONSTRAINTS: Format output as a Markdown table with columns: ID, Type, Scenario Title, Input Data, Expected Behavior, Priority.
```

### 2. Template: "Find Edge Cases"
```text
ROLE: QA Security Specialist and Edge-Case Analyst.
CONTEXT: I am testing a multi-currency vendor invoice processing engine.
INSTRUCTION: Analyze this feature description and list 10 subtle, complex edge cases or failure modes (such as rounding discrepancies, concurrent updates, timezone mismatches, or network drops).
```

### 3. Template: "Review & Refactor Playwright Test"
```text
ROLE: Playwright Python SDET Architect.
CODE TO REVIEW:
[Paste raw Playwright Python script here]
INSTRUCTION: Refactor this code to follow Page Object Model (POM) standards. Replace CSS/XPath locators with accessibility-first role locators (get_by_role, get_by_label), remove arbitrary hardcoded sleeps, and add robust web assertions (expect).
```

### 4. Template: "Convert Manual Test into Automation"
```text
ROLE: SDET Automation Specialist.
MANUAL TEST STEPS:
[Paste manual test case steps here]
INSTRUCTION: Convert these manual steps into a clean pytest Playwright test script. Use fixtures for browser page setup and page objects. Include comments explaining key assertions.
```

### 5. Template: "Analyze Playwright Failure & Log Trace"
```text
ROLE: Automation Debugging Specialist.
STACK TRACE & LOG:
[Paste error log / stack trace here]
INSTRUCTION: Analyze this failure. Identify:
1. What failed (Timeout, Strictness violation, API 500 error).
2. The most likely root cause.
3. Recommended diagnostic steps to confirm.
4. Exact code fix in Python.
```

### 6. Template: "Generate SQL Validation Query"
```text
ROLE: Enterprise Database QA Engineer.
SCHEMA:
[Paste table DDL or schema definitions here]
INSTRUCTION: Write an advanced SQL verification query to validate [specific business rule, e.g. 3-way match variance or duplicate invoices]. Use standard PostgreSQL dialect. Include comments explaining the logic.
```

### 7. Template: "Create API Negative Tests"
```text
ROLE: API Test Engineer.
OPENAPI ENDPOINT SCHEMA:
[Paste Swagger / OpenAPI JSON or YAML payload here]
INSTRUCTION: Generate a list of negative test payloads for testing boundary conditions, missing fields, invalid data types, oversized strings, and SQL injection inputs. Include expected HTTP status code for each payload.
```

### 8. Template: "Generate Test Data"
```text
ROLE: Test Data Management Specialist.
REQUIREMENT: Need realistic synthetic test data for testing Vendor Master creation.
INSTRUCTION: Provide a Python dictionary or JSON array containing 5 realistic vendor records with varied tax IDs, payment terms (NET30, NET60), ISO currency codes, and edge case company names (including special characters like O'Connor & Sons).
```

---

## 🔗 Related Topics
* [01. AI Opportunities & Privacy Rules](01_ai_in_testing_opportunities_limits_privacy.md)
* [03. AI-Assisted Test Generation](03_ai_assisted_test_generation_debugging.md)
* [AI Prompting Cheat Sheet](../21_CHEAT_SHEETS/cheat-sheet-ai-testing.md)
