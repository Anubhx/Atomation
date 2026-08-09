---
title: Pytest Core Guide (Test Discovery, Assertions & Custom Markers)
category: 09_PYTHON_PYTEST
subcategory: Core Pytest
keywords:
  - Pytest
  - Test Discovery
  - Pytest Markers
  - Custom Markers
  - pytest.ini
  - Test Runner
audience:
  - Quality Engineer
  - SDET
  - Python Automation Engineer
difficulty: beginner-intermediate
---

# 🧪 Pytest Core Guide: Discovery, Assertions & Markers

## 🎯 Overview: Pytest Test Discovery Conventions

Pytest automatically discovers and runs tests based on standard naming conventions:
- **Files**: `test_*.py` or `*_test.py`
- **Classes**: `Test*` (without `__init__` constructor)
- **Functions / Methods**: `test_*()`

---

## 🏷️ Pytest Markers & Custom Tagging

Pytest markers tag tests for selective execution, skipping, or expected failures.

### Built-in Markers Example:
```python
import pytest

@pytest.mark.smoke
def test_user_login():
    pass

@pytest.mark.slow
@pytest.mark.regression
def test_end_to_end_p2p_workflow():
    pass

@pytest.mark.skip(reason="Legacy payment provider deprecated")
def test_legacy_payment():
    pass

@pytest.mark.xfail(reason="Known bug JIRA-8814: Pending backend fix")
def test_known_bug_scenario():
    pass
```

### Configuration (`pytest.ini`):
```ini
[pytest]
markers =
    smoke: High-priority smoke tests
    regression: Full system regression suite
    p2p: Procure-to-Pay workflow tests
    api: API tier automation tests
```

### Execution CLI Commands:
```bash
# Run only smoke tests
pytest -m smoke

# Run regression tests excluding slow tests
pytest -m "regression and not slow"
```

---

## 🔗 Related Topics
* [02. Pytest Fixtures & conftest.py](02_pytest_fixtures_scopes_conftest.md)
* [03. Pytest Parametrization & Parallel Execution](03_pytest_parametrization_parallel_retries.md)
* [Pytest Cheat Sheet](../21_CHEAT_SHEETS/cheat-sheet-pytest.md)
