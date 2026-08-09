---
title: Enterprise Automation Framework Design & Directory Architecture
category: 10_AUTOMATION_ARCHITECTURE
subcategory: Framework Structure
keywords:
  - Automation Framework
  - Framework Architecture
  - Folder Structure
  - Enterprise SDET Architecture
  - Pytest Framework Structure
audience:
  - Quality Engineer
  - SDET
  - Automation Architect
difficulty: advanced
---

# 🏛️ Enterprise Automation Framework Design & Folder Structure

## 🎯 Overview: Standardized Framework Architecture

An enterprise-grade test automation repository must be modular, maintainable, self-contained, and clean.

```
automation/
├── config/             # Environment URLs, DB credentials, API endpoints
├── data/               # Static test data JSON/CSV files & payload templates
├── utils/              # Helper utilities (Database connectors, Logger, Encryption)
├── api/                # API Client Service Classes (Requests wrappers)
├── pages/              # Page Object Model classes (Playwright locators & UI methods)
├── fixtures/           # Modular Pytest fixtures (Auth, Data factories, Cleanup)
├── tests/              # Feature test suites (UI, API, Combined E2E)
├── reports/            # Generated HTML execution reports & Allure results
├── screenshots/        # Auto-captured failure screenshots
├── traces/             # Playwright trace zip files for debugging
├── conftest.py         # Global Pytest fixtures & setup/teardown hooks
├── pytest.ini          # Pytest CLI configuration & marker definitions
└── requirements.txt    # Python dependencies (playwright, pytest, requests, etc.)
```

---

## 📂 Folder Responsibilities Breakdown

| Folder / File | Primary Responsibility | Best Practice Rule |
| :--- | :--- | :--- |
| **`config/`** | Manages environment-specific properties (Dev, Staging, Prod). | Never store unencrypted secrets in git! Use `os.getenv()`. |
| **`data/`** | Contains static JSON payload templates and CSV datasets. | Keep data decoupled from test step logic. |
| **`utils/`** | Generic helper functions (DB queries, SFTP clients, Date formatting). | Keep business domain logic out of utility functions. |
| **`api/`** | Service wrapper classes for REST API endpoints. | Return raw `requests.Response` or pydantic objects. |
| **`pages/`** | Page Object classes defining UI locators and user actions. | Never place `assert` statements inside Page Object classes! |
| **`fixtures/`**| Pytest fixture functions providing test setup & automatic teardowns. | Keep fixture scope as narrow as possible. |
| **`tests/`** | Test case files containing pytest test functions and assertions. | Tests should read like plain English user stories. |

---

## 🔗 Related Topics
* [02. Page Object Model Best Practices](02_page_object_model_pom_best_practices.md)
* [03. Combined UI+API+DB Testing Pattern](03_combined_ui_api_db_testing_pattern.md)
