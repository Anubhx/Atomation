---
title: Postman Automation Quick Reference Cheat Sheet
category: 21_CHEAT_SHEETS
subcategory: Postman
keywords:
  - Postman Cheat Sheet
  - Postman Scripts
  - Environment Vars
audience:
  - Quality Engineer
  - API Tester
difficulty: beginner-intermediate
---

# 🚀 Postman Automation Quick Reference Cheat Sheet

```javascript
// Pre-Request: Set Dynamic Variable
pm.variables.set("random_po", "PO-" + Math.floor(Math.random() * 10000));

// Tests: Status Code Assertion
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

// Tests: Extract & Store Variable into Environment
var data = pm.response.json();
pm.environment.set("auth_token", data.token);
```
