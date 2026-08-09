---
title: Pytest Quick Reference Cheat Sheet
category: 21_CHEAT_SHEETS
subcategory: Pytest
keywords:
  - Pytest Cheat Sheet
  - Fixtures Cheat Sheet
  - Markers Cheat Sheet
  - CLI Flags
audience:
  - Quality Engineer
  - SDET
difficulty: beginner-intermediate
---

# 🧪 Pytest Quick Reference Cheat Sheet

## 💻 Common CLI Commands
```bash
pytest                                # Run all discovered tests
pytest tests/test_p2p.py             # Run specific file
pytest -m smoke                       # Run tests marked 'smoke'
pytest -n auto                        # Run in parallel across CPU cores
pytest --reruns 2                    # Retry failed tests twice
pytest --maxfail=1                    # Stop on first failure
pytest -s -v                          # Print stdout and verbose output
```

## 🏷️ Markers & Decorators
```python
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.skip(reason="Deprecation")
@pytest.mark.xfail(reason="Jira-104 bug")
@pytest.mark.parametrize("input, expected", [(1, 2), (3, 4)])
```

## ⚓ Fixture Scopes & Yield
```python
@pytest.fixture(scope="session")  # session, package, module, class, function
def db_conn():
    conn = connect()
    yield conn
    conn.close()
```
