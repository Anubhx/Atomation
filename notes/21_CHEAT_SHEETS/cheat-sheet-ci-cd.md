---
title: CI/CD Pipeline Quick Reference Cheat Sheet
category: 21_CHEAT_SHEETS
subcategory: CI/CD
keywords:
  - CI CD Cheat Sheet
  - GitHub Actions Playwright
  - Pipeline Syntax
audience:
  - Quality Engineer
  - SDET
difficulty: beginner-intermediate
---

# ⚙️ CI/CD Pipeline Quick Reference Cheat Sheet

## 💻 Essential GitHub Actions Workflow Snippet
```yaml
- name: Run Playwright Tests
  env:
    BASE_URL: ${{ secrets.STAGING_URL }}
  run: pytest -n auto --tracing=retain-on-failure --html=report.html

- name: Upload HTML Report
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: html-report
    path: report.html
```
