---
title: HTTP Protocols, REST Methods & Status Codes Guide
category: 06_API_TESTING
subcategory: HTTP & REST Basics
keywords:
  - HTTP
  - HTTPS
  - REST API
  - GET POST PUT PATCH DELETE
  - HTTP Status Codes
  - 200 201 400 401 403 404 409 422 500
audience:
  - Quality Engineer
  - SDET
  - API Tester
difficulty: beginner-intermediate
---

# 🌐 HTTP Protocols, REST Methods & Status Codes Guide

## 🎯 Overview: REST API Communication

Representational State Transfer (REST) APIs use HTTP verbs to perform CRUD (Create, Read, Update, Delete) operations on resources.

---

## 🛠️ HTTP Verbs & Idempotency Matrix

| HTTP Verb | CRUD Action | Primary Purpose | Idempotent? | Safe (Read-Only)? | Expected Success Code |
| :--- | :--- | :--- | :---: | :---: | :---: |
| `GET` | Read | Retrieve resource representation. | ✅ Yes | ✅ Yes | `200 OK` |
| `POST` | Create | Submit payload to create new resource. | ❌ No | ❌ No | `201 Created` |
| `PUT` | Replace / Update | Complete replacement of target resource. | ✅ Yes | ❌ No | `200 OK` / `204 No Content` |
| `PATCH` | Partial Update | Modify specific fields of a resource. | ❌ No | ❌ No | `200 OK` |
| `DELETE` | Delete | Remove target resource. | ✅ Yes | ❌ No | `200 OK` / `204 No Content` |
| `OPTIONS` | CORS Metadata | Query allowed HTTP methods & headers. | ✅ Yes | ✅ Yes | `204 No Content` |
| `HEAD` | Read Headers | Same as GET but returns body-less headers.| ✅ Yes | ✅ Yes | `200 OK` |

---

## 📊 Complete HTTP Status Code Reference for QA

```
1xx: Informational (100 Continue)
2xx: Success (200 OK, 201 Created, 202 Accepted, 204 No Content)
3xx: Redirection (301 Moved Permanently, 304 Not Modified)
4xx: Client Errors (400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 409 Conflict, 422 Unprocessable, 429 Too Many Requests)
5xx: Server Errors (500 Internal Error, 502 Bad Gateway, 503 Service Unavailable, 504 Gateway Timeout)
```

### Detailed Breakdown & QA Assertions

| Code | Status Name | Meaning & When Expected | QA Assertion Check |
| :--- | :--- | :--- | :--- |
| `200` | OK | Successful GET, PUT, or PATCH call. | Assert body contains expected object fields. |
| `201` | Created | Resource successfully created via POST. | Assert `Location` header or returned `id`. |
| `204` | No Content | Successful DELETE or request with empty response. | Assert response body length is 0. |
| `400` | Bad Request | Malformed JSON syntax or invalid data type. | Assert response body contains error message. |
| `401` | Unauthorized | Missing or expired Authentication token. | Assert `WWW-Authenticate` header present. |
| `403` | Forbidden | Authenticated user lacks permission (RBAC). | Assert access denied response payload. |
| `404` | Not Found | Resource ID does not exist in database. | Assert error payload `RESOURCE_NOT_FOUND`. |
| `409` | Conflict | Duplicate unique key (e.g., duplicate Tax ID). | Assert conflict error details in body. |
| `422` | Unprocessable | Schema validation failure (e.g., field failed regex). | Assert list of field validation errors. |
| `429` | Rate Limited | Client exceeded API rate limit threshold. | Assert `Retry-After` header present. |
| `500` | Server Error | Unhandled exception / crash in backend code. | **DEFECT**: Log bug immediately with stack trace. |

---

## 🔗 Related Topics
* [02. Headers, Authentication & OAuth](02_headers_auth_jwt_oauth_cookies.md)
* [05. Python API Automation](05_python_api_automation.md)
* [HTTP Status Codes Cheat Sheet](../21_CHEAT_SHEETS/cheat-sheet-http-status-codes.md)
