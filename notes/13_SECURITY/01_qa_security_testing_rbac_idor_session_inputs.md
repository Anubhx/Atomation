---
title: Practical QA Security Testing (RBAC, IDOR, Sessions & Input Validation)
category: 13_SECURITY
subcategory: QA Security
keywords:
  - QA Security Testing
  - IDOR
  - Insecure Direct Object Reference
  - RBAC Security
  - Privilege Escalation
  - Session Management
  - Input Validation
audience:
  - Quality Engineer
  - SDET
  - Security Champion
difficulty: intermediate
---

# 🛡️ Practical QA Security Testing: RBAC, IDOR & Sessions

## 🎯 Overview: QA Security Testing vs. Penetration Testing

Quality Engineers perform **Functional & Business Logic Security Checks**. QA security testing is NOT specialized penetration testing (which involves reverse-engineering binary exploits or kernel zero-days). QA security verifies authorization rules, session expirations, data masking, and input validation.

```
       ┌─────────────────────────────────────────────────────────────┐
       │                   QA SECURITY SCOPE                         │
       │ Functional RBAC, IDOR API checks, Input sanitization,       │
       │ Session timeout verification, Masked PII/Secrets audit.     │
       └──────────────────────────────┬──────────────────────────────┘
                                      │ Distinct From
                                      ▼
       ┌─────────────────────────────────────────────────────────────┐
       │                SPECIALIZED PENETRATION TESTING              │
       │ Reverse engineering, memory corruptions, zero-day exploits. │
       └─────────────────────────────────────────────────────────────┘
```

---

## 🔒 Primary Vulnerabilities & QA Test Procedures

### 1. Insecure Direct Object References (IDOR)
* **Vulnerability**: Modifying a URL parameter or JSON key (`user_id=104`) to access another user's private data without authorization.
* **QA Test Procedure**:
  1. Log in as `User A` (ID: 104) and intercept `GET /api/v1/invoices/104`.
  2. Swap authentication token to `User B` token, keeping `invoice_id=104`.
  3. **Assertion**: API MUST respond with HTTP `403 Forbidden` (NOT `200 OK`).

### 2. Privilege Escalation (Vertical & Horizontal)
* **Vulnerability**: A `Buyer` role user accessing `/api/v1/admin/delete-user` endpoint.
* **QA Test Procedure**: Perform API testing by invoking administrative endpoints using low-privilege Bearer tokens.

### 3. Session Management & Timeout
* **QA Test Procedure**: Verify that logging out invalidates the server-side session token immediately, and that idling for >15 minutes invalidates the JWT session.

### 4. Input Validation & XSS/SQLi Checks
* **QA Test Procedure**: Inject special payload strings into form fields:
  - XSS payload: `<script>alert('xss')</script>` → Must render as plain text string, NOT execute.
  - SQLi payload: `' OR 1=1 --` → Must be parameterized safely by DB ORM.

---

## 🔗 Related Topics
* [08. ERP RBAC & SoD Testing](../03_ERP_TESTING/08_rbac_security_and_sod_testing.md)
* [02. Headers, Auth & JWT](../06_API_TESTING/02_headers_auth_jwt_oauth_cookies.md)
