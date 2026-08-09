---
title: CI/CD Foundations for QA (Git, GitHub Actions, Jenkins, Azure DevOps)
category: 12_CI_CD
subcategory: CI/CD Concepts
keywords:
  - CI CD
  - Git Branching
  - GitHub Actions
  - Jenkins
  - Azure DevOps
  - Quality Pipeline
audience:
  - Quality Engineer
  - SDET
  - DevOps Engineer
difficulty: intermediate
---

# 🚀 CI/CD Foundations for QA: Continuous Integration Pipelines

## 🎯 Overview: The Enterprise Delivery Pipeline

Continuous Integration (CI) and Continuous Deployment (CD) automate the building, testing, and deployment of software applications.

```
 [ Developer Git Push ] ──> [ 1. Build Container ]
                                   │
                                   ▼
 [ 2. Deploy QA Env ] ────> [ 3. Run Smoke Suite (100% Pass Required) ]
                                   │
                                   ▼
 [ 4. Run API Tests ] ───> [ 5. Run Playwright UI Suite ] ──> [ 6. Quality Gate Evaluation ]
                                                                       │ (Pass)
                                                                       ▼
                                                           [ 7. Generate Allure Report ]
```

---

## 🛠️ Comparison of Popular CI/CD Platforms

| Feature | GitHub Actions | Jenkins | Azure DevOps Pipelines |
| :--- | :--- | :--- | :--- |
| **Config Format** | `.github/workflows/*.yml` | `Jenkinsfile` (Groovy) | `azure-pipelines.yml` |
| **Hosting Model** | Cloud Hosted / Self-Hosted Runner | Self-Hosted Master / Agent | Cloud / Self-Hosted Agent |
| **Artifact Storage**| Built-in (`actions/upload-artifact`) | HTML Publisher Plugin | Built-in Pipeline Artifacts |
| **Ease of Setup** | Extremely High (Native to GitHub) | Moderate (Requires plugin admin) | High (Native to Azure ecosystem) |

---

## 🔗 Related Topics
* [02. Playwright CI Pipeline Setup](02_playwright_pytest_ci_pipeline_setup.md)
* [05. Quality Gates & Continuous Quality](../02_QA_ENGINEERING/05_quality_gates_and_ci_cd.md)
* [CI/CD Pipeline Cheat Sheet](../21_CHEAT_SHEETS/cheat-sheet-ci-cd.md)
