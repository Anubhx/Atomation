---
title: Quality Gates & Continuous Quality in CI/CD
category: 02_QA_ENGINEERING
subcategory: CI/CD Quality Control
keywords:
  - Quality Gates
  - Continuous Quality
  - CI/CD Pipelines
  - SonarQube Gates
  - Automated Release Blockers
audience:
  - Quality Engineer
  - SDET
  - DevOps Lead
difficulty: intermediate
---

# 🚪 Quality Gates & Continuous Quality in CI/CD

## 🎯 Overview: What is a Quality Gate?

A **Quality Gate** is an automated checkpoint in a CI/CD pipeline that evaluates build metrics against predefined quality thresholds. If a build fails to satisfy ANY quality gate threshold, the pipeline immediately halts, blocking code merge or deployment to downstream environments.

```
[Developer Git Push] ──> [Gate 1: Linter & Static Analysis] ──> [Gate 2: Unit Tests (>80% Code Cov)]
                                                                           │
[Deploy Staging] <── [Gate 4: Playwright Regression Suite] <── [Gate 3: API Contract Tests]
```

---

## 📋 Enterprise Quality Gate Threshold Criteria

| Pipeline Stage | Quality Gate Metrics | Action on Failure |
| :--- | :--- | :--- |
| **Pull Request (PR)** | • 0 Linter errors<br>• SonarQube Security Vulnerabilities = 0<br>• Unit Test Coverage >= 80%<br>• PR API Smoke Suite Pass Rate = 100% | **Block Git Merge** |
| **Nightly Staging Build** | • Playwright E2E Regression Pass Rate >= 98%<br>• Flaky Test Rate <= 2%<br>• API Response Latency (p95) < 500ms | **Block Staging Release Candidate** |
| **Pre-Production** | • Security Vulnerability Scan = 0 High/Critical<br>• DB Migration Script Verification = PASS<br>• UAT Sign-off flag = TRUE | **Block Production Deployment** |

---

## 🔗 Related Topics
* [03. Risk-Based Testing](03_risk_based_testing.md)
* [01. CI/CD Concepts & Pipelines](../12_CI_CD/01_ci_cd_concepts_git_github_actions_jenkins.md)
* [02. Playwright CI Pipeline Setup](../12_CI_CD/02_playwright_pytest_ci_pipeline_setup.md)
