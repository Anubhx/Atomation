---
title: API Strategy: Negative Testing, Schema Contracts & Mocking
category: 06_API_TESTING
subcategory: API Strategy
keywords:
  - API Strategy
  - Negative API Testing
  - Contract Testing
  - OpenAPI
  - Swagger
  - Mocking
  - Pact
audience:
  - Quality Engineer
  - SDET
difficulty: intermediate
---

# 🛡️ API Strategy: Negative Testing, Contracts & Mocking

## 🎯 Overview

Robust API quality assurance requires going beyond happy-path 200 OK responses to test schema contract compliance, negative payload boundaries, and isolated dependency mocking.

---

## 🧪 Negative API Testing Matrix

| Negative Test Category | Test Input Payload / Action | Expected HTTP Code | Expected JSON Error Payload |
| :--- | :--- | :---: | :--- |
| **Missing Mandatory Field**| Omit required `vendor_id` key in POST payload. | `422 Unprocessable` | `{"error": "Field 'vendor_id' is required"}` |
| **Invalid Data Type** | Pass string `"TEN"` to integer field `quantity`. | `400 Bad Request` | `{"error": "Invalid data type for 'quantity'"}` |
| **Out-of-Bounds Value** | Pass quantity `-100` or `$10,000,000,000`. | `422 Unprocessable` | `{"error": "Quantity out of allowed bounds"}` |
| **SQL Injection Payload** | Input `' OR '1'='1` in search field `query`. | `200 OK` (Escaped) | Query returns 0 results cleanly (No DB crash). |
| **Expired Token** | Pass JWT with `exp` timestamp in past. | `401 Unauthorized` | `{"error": "Token has expired"}` |

---

## 📜 Contract Testing & OpenAPI Validation

Contract testing ensures consumer frontend apps and backend API producers conform to an agreed OpenAPI/Swagger specification.
* **Tooling**: Pact, Schemathesis, Dredd.
* **Benefit**: Catches breaking backend field renames before code reaches Staging.

---

## 🔗 Related Topics
* [01. HTTP REST Methods](01_http_rest_methods_status_codes.md)
* [05. Python API Automation](05_python_api_automation.md)
* [01. Mocking & Interception](../19_INTEGRATION/01_mocking_stubbing_interception_virtualization.md)
