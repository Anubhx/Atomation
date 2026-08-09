---
title: Pytest Parametrization, Parallel Execution (xdist) & Retries
category: 09_PYTHON_PYTEST
subcategory: Advanced Execution
keywords:
  - pytest parametrize
  - pytest-xdist
  - pytest-rerunfailures
  - Parallel Testing
  - Flaky Test Retry
  - Data-Driven Testing
audience:
  - Quality Engineer
  - SDET
  - Automation Architect
difficulty: intermediate
---

# ⚡ Pytest Parametrization, Parallel Execution & Flaky Retries

## 🎯 Overview: Data-Driven & Parallel Execution

Pytest natively supports **Data-Driven Testing** via `@pytest.mark.parametrize` and parallel multi-CPU test execution via `pytest-xdist`.

---

## 💻 1. Data-Driven Testing (`@pytest.mark.parametrize`)

```python
import pytest

@pytest.mark.parametrize("invalid_email, expected_error", [
    ("missing_at_symbol.com", "Invalid email format"),
    ("user@", "Email domain missing"),
    ("", "Email is required"),
    ("admin@domain..com", "Double dot in domain invalid")
])
def test_login_email_negative_validation(page, invalid_email, expected_error):
    page.goto("/login")
    page.get_by_label("Email").fill(invalid_email)
    page.get_by_role("button", name="Log In").click()
    
    expect(page.locator(".error-banner")).to_contain_text(expected_error)
```

---

## ⚡ 2. Parallel Test Execution (`pytest-xdist`)

Accelerate test execution times by running tests in parallel across multiple CPU cores:

```bash
# Run tests in parallel utilizing all available CPU cores
pytest -n auto

# Run tests in parallel across 4 worker processes
pytest -n 4 --dist loadscope
```

---

## 🔄 3. Handling Flaky Tests (`pytest-rerunfailures`)

Automatically retry failed tests to distinguish real defects from temporary network glitches:

```bash
# Retry failed tests up to 2 times with a 1-second delay between retries
pytest --reruns 2 --reruns-delay 1
```

---

## 🔗 Related Topics
* [01. Pytest Core Guide](01_pytest_core_discovery_assertions_markers.md)
* [02. Playwright CI Pipeline Setup](../12_CI_CD/02_playwright_pytest_ci_pipeline_setup.md)
