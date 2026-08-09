---
title: Postman Mastery Guide (Collections, Environments & Test Scripting)
category: 06_API_TESTING
subcategory: API Tooling
keywords:
  - Postman
  - Postman Scripts
  - Environment Variables
  - Request Chaining
  - Newman CI
  - API Testing Tools
audience:
  - Quality Engineer
  - API Tester
difficulty: beginner-intermediate
---

# 🚀 Postman Mastery Guide: Enterprise API Testing

## 🎯 Overview: Postman Architecture

Postman organizes API testing into **Collections** (request suites), **Environments** (key-value pairs for Dev/Staging/Prod), **Pre-request Scripts** (executed before request dispatch), and **Tests Scripts** (executed after response receipt).

```
 [ Pre-Request Script ] ──> [ Execute HTTP Request ] ──> [ Response Received ] ──> [ Tests Script (Assertions) ]
```

---

## 🛠️ Postman JavaScript Assertions & Request Chaining

### 1. Pre-Request Script: Generating Dynamic Data
```javascript
// Generate unique PO number and set ISO timestamp
pm.variables.set("dynamic_po_number", "PO-" + Math.floor(Math.random() * 1000000));
pm.variables.set("current_timestamp", new Date().toISOString());
```

### 2. Tests Script: Status Code, Schema & Response Extraction
```javascript
// 1. Assert Status Code 201 Created
pm.test("Status code is 201 Created", function () {
    pm.response.to.have.status(201);
});

// 2. Assert Response Time under 500ms
pm.test("Response time is less than 500ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(500);
});

// 3. Extract Bearer Token or Created ID for Request Chaining
var jsonData = pm.response.json();
pm.test("Response contains purchase_order_id", function () {
    pm.expect(jsonData.purchase_order_id).to.exist;
});

// Store extracted ID into Environment Variable for next request
pm.environment.set("created_po_id", jsonData.purchase_order_id);
```

---

## 🏃 Newman CLI Pipeline Execution

Run Postman collections in CI/CD pipelines via Newman:
```bash
newman run P2P_API_Collection.json \
  -e Staging_Environment.json \
  --reporters cli,htmlextra \
  --reporter-htmlextra-export ./reports/api_report.html
```

---

## 🔗 Related Topics
* [01. HTTP REST Methods](01_http_rest_methods_status_codes.md)
* [05. Python API Automation](05_python_api_automation.md)
* [Postman Automation Cheat Sheet](../21_CHEAT_SHEETS/cheat-sheet-postman.md)
