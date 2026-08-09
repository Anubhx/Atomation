---
title: Python for QA Engineers Cheat Sheet
category: 21_CHEAT_SHEETS
subcategory: Python
keywords:
  - Python Cheat Sheet
  - List Comprehension
  - Dict Operations
  - Exception Handling
audience:
  - Quality Engineer
  - SDET
difficulty: beginner-intermediate
---

# 🐍 Python for QA Engineers Cheat Sheet

## 📦 Data Structures & Methods
```python
# List Comprehension
active_vendors = [v["name"] for v in vendors if v["is_active"]]

# Dictionary Operations
status = response.json().get("status", "UNKNOWN")

# String Formatting & UUID
user_email = f"qa_user_{uuid.uuid4()[:8]}@example.com"
```

## 🛡️ Exception Handling
```python
try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
except requests.exceptions.RequestException as err:
    logger.error(f"API Error: {err}")
```
