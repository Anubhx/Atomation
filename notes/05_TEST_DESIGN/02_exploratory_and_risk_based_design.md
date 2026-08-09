---
title: Exploratory & Risk-Based Test Design
category: 05_TEST_DESIGN
subcategory: Advanced Test Design
keywords:
  - Exploratory Testing
  - SBTM
  - Session-Based Testing
  - Risk-Based Design
  - Heuristics
audience:
  - Quality Engineer
  - Manual Tester
  - SDET
difficulty: intermediate
---

# 🕵️ Exploratory & Risk-Based Test Design

## 🎯 Overview: Structured Exploratory Testing

Exploratory testing is not random "monkey testing". It is **simultaneous learning, test design, and test execution** guided by domain expertise, risk heuristics, and structured session charters.

---

## ⏱️ Session-Based Test Management (SBTM)

To make exploratory testing measurable and accountable, use **SBTM Charters**:

### SBTM Charter Template: `CHARTER_P2P_004`
* **Charter**: Explore the Vendor Invoice file upload modal using invalid PDF file headers, corrupted images, and 50MB oversized payloads to evaluate system stability and security error handling.
* **Timebox**: 60 minutes.
* **Tester**: Quality Engineer.
* **Findings / Defects Logged**:
  - Found 1 Critical Defect: Uploading a 50MB file causes browser tab memory exhaustion (OOM) because the client attempts base64 encoding synchronously on the main thread.

---

## 🔗 Related Topics
* [01. Black-Box Test Design](01_black_box_design_techniques.md)
* [03. Risk-Based Testing](../02_QA_ENGINEERING/03_risk_based_testing.md)
