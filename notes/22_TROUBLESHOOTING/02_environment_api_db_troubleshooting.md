---
title: Environment, API & Database Failure Troubleshooting Cookbook
category: 22_TROUBLESHOOTING
subcategory: Infrastructure Troubleshooting
keywords:
  - API Troubleshooting
  - API Returns 401
  - API Returns 403
  - DB Record Missing
  - Test Data Already Exists
audience:
  - Quality Engineer
  - SDET
  - API Tester
difficulty: intermediate
---

# 🔧 Environment, API & DB Failure Troubleshooting Cookbook

## 🎯 Problem 1: "API Returns 401 Unauthorized"

### Symptoms
API automation calls return HTTP 401 status with message `"Token expired or invalid"`.

### Fix
1. Inspect JWT expiration payload timestamp (`exp`).
2. Refresh bearer token via `POST /oauth/token` prior to running test suite.

---

## 🎯 Problem 2: "API Returns 403 Forbidden"

### Symptoms
HTTP 403 Forbidden response when executing an endpoint.

### Fix
Verify assigned user role in DB: `SELECT role FROM user_roles WHERE user_id = 'qa_test_user'`. Ensure test user possesses mandatory RBAC permissions.

---

## 🎯 Problem 3: "Test Data Already Exists" / Key Collisions

### Symptoms
Test fails on 2nd run with `HTTP 409 Conflict` or DB `Duplicate Key Violation`.

### Fix
Use dynamic UUIDs for all primary test entity keys:
```python
import uuid
unique_po_number = f"PO-{uuid.uuid4()[:8]}"
```

---

## 🔗 Related Topics
* [01. HTTP REST Methods](../06_API_TESTING/01_http_rest_methods_status_codes.md)
* [01. Automation Troubleshooting Cookbook](01_automation_troubleshooting_cookbook.md)
