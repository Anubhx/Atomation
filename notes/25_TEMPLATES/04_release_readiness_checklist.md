---
title: Release Readiness & Quality Gate Checklist
category: 25_TEMPLATES
subcategory: Quality Gate Templates
keywords:
  - Release Readiness
  - Quality Gate Checklist
  - QA Metrics
  - Sign-off Checklist
audience:
  - Quality Engineer
  - QA Lead
  - Release Manager
difficulty: beginner-intermediate
---

# 🚀 Release Readiness & Quality Gate Checklist

## 🎯 Overview: Pre-Release Quality Gate

This checklist is evaluated prior to promoting any release candidate build to production.

---

## 📊 Core QA Metrics Thresholds

| Metric | Target Threshold | Formula / Calculation | Status |
| :--- | :--- | :--- | :---: |
| **Pass Rate** | $\ge 98.0\%$ | $\frac{\text{Passed Tests}}{\text{Total Executed Tests}} \times 100$ | [ ] |
| **Defect Density** | $\le 0.5 \text{ bugs/KLOC}$ | $\frac{\text{Total Open Defects}}{\text{Thousands Lines of Code}}$ | [ ] |
| **Escaped Defects** | $0 \text{ Critical/High}$ | Defects discovered post-deployment in Production | [ ] |
| **Automation Coverage**| $\ge 80.0\%$ | $\frac{\text{Automated Test Cases}}{\text{Total Regression Scenarios}} \times 100$| [ ] |
| **Flaky Test Rate** | $\le 2.0\%$ | $\frac{\text{Flaky Retried Tests}}{\text{Total Executed Tests}} \times 100$ | [ ] |
| **Mean Time to Detect**| $< 15 \text{ mins}$ | Average time from commit to CI failure notification | [ ] |

---

## 📋 Pre-Release Sign-Off Checklist

- [ ] 1. All automated Playwright UI & API regression suites executed in CI pipeline with $\ge 98\%$ pass rate.
- [ ] 2. Zero `Critical` or `High` severity open defects in JIRA.
- [ ] 3. Database migration scripts verified and tested against pre-prod backup.
- [ ] 4. Security RBAC checks and authorization policies audited.
- [ ] 5. UAT sign-off received from Product Owner.
- [ ] 6. Production rollback procedure documented and verified.
