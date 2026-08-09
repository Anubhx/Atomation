---
title: Pytest Fixtures, Scopes & conftest.py Architecture
category: 09_PYTHON_PYTEST
subcategory: Fixtures
keywords:
  - Pytest Fixtures
  - conftest.py
  - Fixture Scopes
  - Setup and Teardown
  - Yield Fixture
audience:
  - Quality Engineer
  - SDET
  - Automation Engineer
difficulty: intermediate
---

# ⚓ Pytest Fixtures, Scopes & conftest.py Architecture

## 🎯 Overview: Pytest Fixture Architecture

Fixtures manage setup state, test data creation, API authentication tokens, database connections, and teardown cleanup across pytest suites.

---

## 📊 Pytest Fixture Scope Hierarchy

```
 [ session ]: Executed ONCE per test run (e.g., Launching DB connection pool, OAuth token generation).
       │
       ▼
 [ package / module ]: Executed ONCE per test file / package (e.g., Loading test dataset).
       │
       ▼
 [ class ]: Executed ONCE per test class.
       │
       ▼
 [ function ]: Executed BEFORE & AFTER EVERY test function (Default: Isolated clean state).
```

---

## 💻 Enterprise `conftest.py` Shared Fixture Architecture

```python
# conftest.py
import pytest
import psycopg2
from typing import Generator

@pytest.fixture(scope="session")
def env_config():
    """Session-scoped fixture loading environment variables."""
    return {
        "BASE_URL": "https://staging.erp.client.com",
        "DB_HOST": "localhost",
        "DB_PORT": 5432
    }

@pytest.fixture(scope="session")
def db_connection(env_config):
    """Session-scoped database connection pool."""
    conn = psycopg2.connect(
        host=env_config["DB_HOST"],
        port=env_config["DB_PORT"],
        dbname="erp_db",
        user="qa_user",
        password="qa_password"
    )
    yield conn
    # Teardown: Executed at end of test session
    conn.close()

@pytest.fixture(scope="function")
def isolated_vendor(db_connection) -> Generator[str, None, None]:
    """Function-scoped fixture creating unique test data with automatic teardown cleanup."""
    cursor = db_connection.cursor()
    vendor_id = f"VEND_TEST_{pytest.helpers.random_id()}"
    
    # SETUP
    cursor.execute("INSERT INTO vendors (vendor_id, legal_name, tax_id) VALUES (%s, %s, %s)",
                   (vendor_id, "Test Vendor LLC", f"TAX_{vendor_id}"))
    db_connection.commit()
    
    yield vendor_id  # Pass created ID to test function
    
    # TEARDOWN
    cursor.execute("DELETE FROM vendors WHERE vendor_id = %s", (vendor_id,))
    db_connection.commit()
```

---

## 🔗 Related Topics
* [01. Pytest Core Guide](01_pytest_core_discovery_assertions_markers.md)
* [01. Playwright Setup](../08_PLAYWRIGHT/01_playwright_python_setup_architecture.md)
