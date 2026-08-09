---
title: How to Use This Knowledge Base
category: 00_START_HERE
subcategory: Onboarding & Navigation
keywords:
  - RAG Knowledge Base
  - Field Manual
  - QA Reference
  - Vector Search
  - Searching QA Documentation
audience:
  - Quality Engineer
  - SDET
  - Junior QA
  - Enterprise QA Lead
difficulty: beginner
---

# 📖 How to Use This RAG-Ready QA Knowledge Base

## 🎯 Purpose & Target Audience

This repository is an **operational field manual** designed for early-career Quality Engineers (~1 year of experience) stepping into complex enterprise projects. It equips you to operate independently at a strong enterprise QA/SDET level.

Whether you are validating an ERP purchase workflow, writing Playwright automation in Python, auditing SQL transactions, or interfacing with AI tools like ChatGPT or Claude, this knowledge base provides immediate, non-generic answer blocks.

---

## 🔍 How to Search & Query This KB

### 1. Vector Search / RAG Systems (e.g., Cursor, LangChain, LlamaIndex, Local LLMs)
This repository is optimized for Retrieval-Augmented Generation (RAG):
- Each file begins with structured YAML frontmatter keywords.
- Headers are atomic and semantic (`## Procure-to-Pay Database Validation` instead of `## Step 3`).
- Code blocks contain context comments and expected output.

**Sample RAG Prompts to run against this directory:**
* *"Show me the Playwright locator strategy for dynamic enterprise tables."* → Retrieves `08_PLAYWRIGHT/02_locators_strategy_accessibility_strictness.md`
* *"What SQL query checks 3-way match in Procure-to-Pay?"* → Retrieves `03_ERP_TESTING/03_procure_to_pay_p2p_workflow.md`
* *"Give me a pytest fixture for isolated DB transactions."* → Retrieves `09_PYTHON_PYTEST/02_pytest_fixtures_scopes_conftest.md`

### 2. Manual Keyword Search (Grep / VS Code Search)
* Press `Cmd+Shift+F` (Mac) or `Ctrl+Shift+F` (Windows) in VS Code.
* Search for specific business terms (e.g., `3-Way Match`, `IDOR`, `Strict mode violation`, `Pytest parametrization`).

---

## 🏗️ Folder Navigation Guide

| Folder | What You Will Find |
| :--- | :--- |
| **`01_SOFTWARE_TESTING`** | Core definitions, SDLC/STLC, testing levels, user story analysis. |
| **`02_QA_ENGINEERING`** | Shift-Left, Risk-Based Testing, Quality Gates, RCA, Test Pyramid. |
| **`03_ERP_TESTING`** | P2P, O2C, H2R, R2R, Master Data, RBAC, 100+ ERP Edge Cases. |
| **`04_ENTERPRISE_TESTING`** | Multi-tier app testing, microservices, asynchronous message queues. |
| **`05_TEST_DESIGN`** | Equivalence Partitioning, BVA, Decision Tables, Pairwise matrix. |
| **`06_API_TESTING`** | HTTP methods, status codes, JWT, Postman scripts, Python Requests. |
| **`07_DATABASE_TESTING`** | SQL joins, group by, subqueries, transaction rollback validation. |
| **`08_PLAYWRIGHT`** | Playwright Python, role locators, codegen refactoring, trace viewer. |
| **`09_PYTHON_PYTEST`** | Pytest fixtures, scoping, parametrization, `conftest.py` patterns. |
| **`10_AUTOMATION_ARCHITECTURE`** | Page Object Model (POM), combined UI+API+DB execution pattern. |
| **`11_AI_TEST_AUTOMATION`** | AI prompt templates, LLM boundaries, privacy rules, test generation. |
| **`12_CI_CD`** | GitHub Actions, Jenkins, Playwright HTML report integration. |
| **`13_SECURITY`** | Practical QA security: RBAC, IDOR, SQLi inputs, session timeouts. |
| **`14_HEALTHCARE_MEDTECH`** | HIPAA, FDA design controls, verification vs validation, audit logs. |
| **`15_AGILE`** | Sprint ceremonies, DoR/DoD, grooming, QA role in daily standups. |
| **`16_DEFECT_MANAGEMENT`** | Severity vs priority, high-impact bug reporting templates. |
| **`17_TEST_DATA`** | Test data factories, synthetic data, anonymization, PII rules. |
| **`18_PERFORMANCE`** | Response time, throughput, k6 / Locust load testing basics. |
| **`19_INTEGRATION`** | Network interception, API mocking, stubbing in Playwright. |
| **`20_RELEASE_TESTING`** | Production smoke testing, feature flags, deployment verification. |
| **`21_CHEAT_SHEETS`** | 16 quick-reference cheat sheets (Playwright, Pytest, SQL, ERP, etc.). |
| **`22_TROUBLESHOOTING`** | Step-by-step diagnostic trees for automation and environment failures. |
| **`23_INTERVIEW_PREPARATION`** | Real enterprise interview questions and scenario answers. |
| **`24_REAL_WORLD_SCENARIOS`** | Deep case studies of enterprise outages and QA resolutions. |
| **`25_TEMPLATES`** | Copy-paste templates for Test Strategy, Test Plan, Bug Reports. |

---

## 💡 Best Practices for Daily Project Work

1. **Before grooming a feature**: Open `05_TEST_DESIGN/` and `03_ERP_TESTING/` to generate edge cases during sprint refinement.
2. **When an automated test fails**: Open `22_TROUBLESHOOTING/01_automation_troubleshooting_cookbook.md` or check `21_CHEAT_SHEETS/cheat-sheet-debugging.md`.
3. **When writing API automation**: Check `06_API_TESTING/05_python_api_automation.md` for standard fixture and assertion structure.
4. **When reporting a critical bug**: Use `25_TEMPLATES/03_bug_report_template.md`.

---

## 🔗 Related Topics
* [02. The Enterprise QA Engineer Mindset](02_qa_engineer_mindset.md)
* [Master Index](../README.md)
