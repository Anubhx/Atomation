---
title: Python API Automation Framework (Requests + Pytest)
category: 06_API_TESTING
subcategory: API Automation
keywords:
  - Python API Automation
  - Requests Library
  - Pytest API Testing
  - API Client Pattern
  - Schema Validation
audience:
  - Quality Engineer
  - SDET
  - Automation Engineer
difficulty: intermediate
---

# 🐍 Python API Automation Framework (Requests + Pytest)

## 🎯 Overview: Designing a Clean Python API Client

In enterprise automation, API calls should not be hardcoded in test files. Wrap HTTP logic inside an **API Client Service Class** using Python's `requests` library.

---

## 💻 Production-Grade API Client Implementation

### 1. API Client Class (`api_client.py`)

```python
import requests
from typing import Dict, Any

class ERPApiClient:
    def __init__(self, base_url: str, token: str = None):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"

    def create_purchase_order(self, payload: Dict[str, Any]) -> requests.Response:
        url = f"{self.base_url}/api/v1/purchase-orders"
        response = self.session.post(url, json=payload, timeout=10)
        return response

    def get_purchase_order(self, po_number: str) -> requests.Response:
        url = f"{self.base_url}/api/v1/purchase-orders/{po_number}"
        return self.session.get(url, timeout=10)
```

---

### 2. Pytest Test Suite (`test_purchase_order_api.py`)

```python
import pytest
from api_client import ERPApiClient

@pytest.fixture
def api_client(env_config):
    # Setup API client with valid bearer token
    token = env_config["AUTH_TOKEN"]
    return ERPApiClient(base_url=env_config["BASE_URL"], token=token)

def test_create_valid_purchase_order(api_client):
    payload = {
        "vendor_id": "VEND_991",
        "items": [
            {"sku": "MAT-104", "quantity": 10, "unit_price": 50.00}
        ],
        "currency": "USD"
    }
    
    response = api_client.create_purchase_order(payload)
    
    # Assert Status Code
    assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
    
    # Assert JSON Data
    data = response.json()
    assert "po_number" in data
    assert data["total_amount"] == 500.00
    assert data["status"] == "ISSUED"
```

---

## 🔗 Related Topics
* [01. HTTP REST Methods](01_http_rest_methods_status_codes.md)
* [01. Pytest Core Concepts](../09_PYTHON_PYTEST/01_pytest_core_discovery_assertions_markers.md)
* [API Testing Cheat Sheet](../21_CHEAT_SHEETS/cheat-sheet-api-testing.md)
