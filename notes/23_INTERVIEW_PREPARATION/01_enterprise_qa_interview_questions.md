---
title: Enterprise QA & SDET Technical Interview Scenarios & Answers
category: 23_INTERVIEW_PREPARATION
subcategory: Interview Preparation
keywords:
  - QA Interview Questions
  - SDET Interview Scenarios
  - ERP QA Interview
  - Playwright Python Interview
  - Quality Engineering Interview
audience:
  - Quality Engineer
  - SDET Candidates
difficulty: intermediate-advanced
---

# 🎯 Enterprise QA & SDET Technical Interview Scenarios

## 🎯 Question 1: "How do you test a 3-Way Match in an ERP Procure-to-Pay workflow?"

### Expected Senior QA Answer
"Testing a 3-Way Match requires full-stack validation across three entities: Purchase Order, Goods Receipt, and Invoice.
1. **Happy Path**: Verify Invoice matching when Invoice Quantity == Goods Receipt Quantity AND Invoice Unit Price == PO Unit Price within configured tolerance. Status updates to `APPROVED` and GL posts AP liability.
2. **Negative Boundary**: Submit Invoice exceeding PO price by >5%. Verify 3-Way Match engine sets status to `HELD_VARIANCE_EXCEEDED` and triggers approval hold.
3. **Database & Audit Verification**: Run SQL queries to ensure foreign keys match across `purchase_orders`, `goods_receipts`, and `invoices`, and verify `audit_logs` records `VARIANCE_BLOCK_TRIGGERED` with timestamp and user ID."

---

## 🎯 Question 2: "Why prefer Playwright over Selenium for modern Python web automation?"

### Expected Senior QA Answer
"Playwright operates out-of-process via WebSocket directly contacting Chrome DevTools Protocol (CDP) and browser engines, eliminating Selenium's HTTP WebDriver polling latency. Key benefits include:
- Native **Auto-Waiting** on locators before executing actions (eliminating fragile `time.sleep()`).
- Accessibility-first locators (`get_by_role`, `get_by_label`) promoting resilient tests.
- Isolated **BrowserContexts** allowing multi-role incognito testing in milliseconds.
- Built-in **Trace Viewer** for full DOM snapshot and network log debugging."

---

## 🔗 Related Topics
* [03. Procure-to-Pay Workflow](../03_ERP_TESTING/03_procure_to_pay_p2p_workflow.md)
* [01. Playwright Setup](../08_PLAYWRIGHT/01_playwright_python_setup_architecture.md)
