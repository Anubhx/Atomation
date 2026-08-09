---
title: API Testing Quick Reference Cheat Sheet
category: 21_CHEAT_SHEETS
subcategory: API Testing
keywords:
  - API Cheat Sheet
  - HTTP Verbs
  - Requests Python
  - Headers Auth
audience:
  - Quality Engineer
  - SDET
difficulty: beginner-intermediate
---

# 🌐 API Testing Quick Reference Cheat Sheet

## 🛠️ Python Requests Syntax
```python
import requests

# GET with Query Params & Bearer Token
headers = {"Authorization": "Bearer eyJhbG..."}
res = requests.get("https://api.example.com/po", params={"status": "APPROVED"}, headers=headers)

# POST JSON Payload
payload = {"vendor_id": "VEND_101", "total": 500.00}
res = requests.post("https://api.example.com/po", json=payload, headers=headers)

# Assertions
assert res.status_code == 201
assert res.json()["status"] == "ISSUED"
```
