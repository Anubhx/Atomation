---
title: Automation Debugging Quick Reference Cheat Sheet
category: 21_CHEAT_SHEETS
subcategory: Debugging
keywords:
  - Debugging Cheat Sheet
  - Playwright Debugging
  - Trace Viewer
audience:
  - Quality Engineer
  - SDET
difficulty: beginner-intermediate
---

# 🐞 Automation Debugging Quick Reference Cheat Sheet

## 🛠️ CLI Debug Commands
```bash
PWDEBUG=1 pytest tests/test_po.py        # Launch Playwright Inspector GUI
pytest --headed --slowmo 500              # Visual slow-motion run
pytest --tracing=retain-on-failure        # Record trace zips on failure
playwright show-trace trace.zip           # Open Trace Viewer GUI
```
