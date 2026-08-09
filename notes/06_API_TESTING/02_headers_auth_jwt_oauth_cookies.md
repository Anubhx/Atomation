---
title: HTTP Headers, Authentication (JWT, OAuth2) & Sessions
category: 06_API_TESTING
subcategory: API Security & Headers
keywords:
  - HTTP Headers
  - Bearer Token
  - JWT
  - OAuth2
  - Session Cookies
  - API Keys
audience:
  - Quality Engineer
  - SDET
  - API Security Tester
difficulty: intermediate
---

# 🔑 HTTP Headers, Authentication (JWT, OAuth2) & Cookies

## 🎯 Overview: API Headers & Authentication Mechanics

HTTP Headers transmit metadata between client and server. Authentication mechanisms ensure requests are verified and authorized.

---

## 📋 Essential HTTP Headers for QA Testing

| Header Name | Type | Purpose | Example Value |
| :--- | :--- | :--- | :--- |
| `Content-Type` | Request / Response | MIME type of request body. | `application/json` |
| `Accept` | Request | Expected response format. | `application/json` |
| `Authorization` | Request | Credentials for authenticating request. | `Bearer eyJhbGciOiJIUzI1...` |
| `X-API-Key` | Request | Custom header API token authentication. | `key_live_9941a8bc` |
| `Cookie` | Request | Client session identifiers. | `session_id=s%3A9942a...` |
| `Location` | Response | URI of newly created or redirected resource.| `/api/v1/users/994` |

---

## 🔐 Authentication Protocols Breakdown

### 1. Bearer Token & JWT (JSON Web Token)
JWTs consist of three dot-separated base64 encoded parts: `Header.Payload.Signature`.
* **Header Format**: `Authorization: Bearer <jwt_token>`
* **QA Validation Point**: Verify that decoding the JWT payload reveals expected `sub`, `roles`, and `exp` (expiration timestamp) values, and that expired JWTs return HTTP 401.

### 2. OAuth 2.0 Flow
1. Client requests authorization code via `POST /oauth/token` providing `grant_type=client_credentials`, `client_id`, and `client_secret`.
2. Authorization server returns JSON with `access_token` and `expires_in: 3600`.
3. Client attaches `access_token` as Bearer token in subsequent requests.

---

## 🔗 Related Topics
* [01. HTTP REST Methods](01_http_rest_methods_status_codes.md)
* [05. Python API Automation](05_python_api_automation.md)
* [01. QA Security Testing](../13_SECURITY/01_qa_security_testing_rbac_idor_session_inputs.md)
