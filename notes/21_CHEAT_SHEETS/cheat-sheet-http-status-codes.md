---
title: HTTP Status Codes Quick Reference Cheat Sheet
category: 21_CHEAT_SHEETS
subcategory: HTTP Status Codes
keywords:
  - HTTP Status Codes Cheat Sheet
  - 200 201 400 401 403 404 409 422 500
audience:
  - Quality Engineer
  - SDET
difficulty: beginner
---

# 🚥 HTTP Status Codes Quick Reference Cheat Sheet

| Code | Name | Meaning | Common QA Cause |
| :--- | :--- | :--- | :--- |
| **200** | OK | Success (GET/PUT/PATCH). | Request processed normally. |
| **201** | Created | Resource Created (POST). | New entity saved in DB. |
| **204** | No Content | Success with empty body. | Entity deleted successfully. |
| **400** | Bad Request | Invalid JSON format/syntax. | Malformed request payload. |
| **401** | Unauthorized | Missing or expired token. | Header `Authorization` missing or expired. |
| **403** | Forbidden | User authenticated, lacks RBAC role. | Buyer trying to approve invoice. |
| **404** | Not Found | Entity ID does not exist. | ID `99999` not in database. |
| **409** | Conflict | Duplicate unique key error. | Re-submitting existing invoice number. |
| **422** | Unprocessable | Schema validation failure. | Field regex or boundary failure. |
| **429** | Rate Limited | Exceeded rate limit. | Too many requests in time window. |
| **500** | Server Error | Unhandled backend code crash. | **BUG**: NullPointerException or unhandled exception. |
