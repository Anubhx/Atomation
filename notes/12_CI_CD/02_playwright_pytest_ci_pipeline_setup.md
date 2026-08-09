---
title: Playwright + Pytest CI Pipeline Setup (GitHub Actions YAML)
category: 12_CI_CD
subcategory: Pipeline Automation
keywords:
  - Playwright GitHub Actions
  - pytest CI Pipeline
  - Playwright HTML Report
  - Continuous Testing
  - GitHub Workflow YAML
audience:
  - Quality Engineer
  - SDET
  - DevOps Engineer
difficulty: intermediate
---

# ⚙️ Playwright + Pytest CI Pipeline Setup (GitHub Actions)

## 🎯 Overview: Production GitHub Actions Workflow

This production workflow automatically triggers on every Pull Request to `main`, installs Python dependencies, installs Playwright browsers, executes pytest suites in parallel, and uploads HTML execution reports.

---

## 💻 Working GitHub Actions Workflow File (`.github/workflows/playwright.yml`)

```yaml
name: Playwright Regression Test Suite

on:
  push:
    branches: [ main, release/* ]
  pull_request:
    branches: [ main ]
  schedule:
    # Run nightly regression suite at 2:00 AM UTC
    - cron: '0 2 * * *'

jobs:
  test:
    name: Run Automation Tests
    runs-on: ubuntu-latest
    timeout-minutes: 60

    steps:
      - name: Checkout Code Repository
        uses: actions/checkout@v4

      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install Python Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Install Playwright Browsers with Dependencies
        run: |
          npx playwright install --with-deps chromium

      - name: Execute Playwright Pytest Suite
        env:
          BASE_URL: ${{ secrets.STAGING_BASE_URL }}
          AUTH_TOKEN: ${{ secrets.STAGING_AUTH_TOKEN }}
          DB_HOST: ${{ secrets.STAGING_DB_HOST }}
        run: |
          pytest -n auto --tracing=retain-on-failure --html=reports/report.html --self-contained-html

      - name: Upload HTML Test Report Artifact
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-html-report
          path: reports/report.html
          retention-days: 30

      - name: Upload Failure Traces
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-failure-traces
          path: test-results/
          retention-days: 14
```

---

## 🔗 Related Topics
* [01. CI/CD Foundations](01_ci_cd_concepts_git_github_actions_jenkins.md)
* [01. Playwright Setup](../08_PLAYWRIGHT/01_playwright_python_setup_architecture.md)
