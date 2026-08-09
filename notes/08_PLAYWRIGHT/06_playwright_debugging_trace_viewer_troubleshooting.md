---
title: Playwright Debugging & Trace Viewer Cookbook
category: 08_PLAYWRIGHT
subcategory: Debugging
keywords:
  - Playwright Debugging
  - Trace Viewer
  - headed slowmo
  - Playwright Inspector
  - TimeoutError
  - Debugging Decision Tree
audience:
  - Quality Engineer
  - SDET
  - Automation Engineer
difficulty: intermediate
---

# 🐞 Playwright Debugging & Trace Viewer Cookbook

## 🎯 Overview: Playwright Debugging Toolkit

When a Playwright test fails, Playwright provides a complete diagnostic suite: **Headed Execution**, **PWDEBUG Inspector**, **Trace Viewer**, **Console/Network Logs**, and **Video Artifacts**.

---

## 🛠️ CLI Debugging Flags

```bash
# 1. Run tests in Headed mode (opens visual browser)
pytest --headed

# 2. Run tests with Slow-Motion delay (slows down actions by 500ms)
pytest --headed --slowmo 500

# 3. Launch Playwright Inspector GUI (pauses execution on every step)
PWDEBUG=1 pytest tests/test_purchase_order.py

# 4. Record Trace file for failure analysis
pytest --tracing=retain-on-failure
```

---

## 🔍 Using Playwright Trace Viewer

The **Trace Viewer** is Playwright's most powerful debugging tool. It records DOM snapshots before/after every action, network request/response headers, console logs, and execution timelines.

```bash
# View recorded trace file
playwright show-trace test-results/test-purchase-order-python/trace.zip
```

```
┌────────────────────────────────────────────────────────────────────────┐
│                        PLAYWRIGHT TRACE VIEWER                         │
├───────────────────┬────────────────────────────────────────────────────┤
│  ACTION TIMELINE  │  DOM SNAPSHOT (BEFORE / AFTER ACTION)              │
│  1. goto(/login)  │  [ Displays visual page at step 3: click button ]  │
│  2. fill(Email)   │                                                    │
│  3. click(Submit) │────────────────────────────────────────────────────┤
│  4. expect(URL)   │  CONSOLE LOGS  │  NETWORK PAYLOADS  │ SOURCE CODE  │
└───────────────────┴────────────────┴────────────────────┴──────────────┘
```

---

## 🌳 Automation Failure Diagnostics Decision Tree

```
                      [ TEST FAILURE OCCURRED ]
                                  │
          ┌───────────────────────┴───────────────────────┐
          ▼                                               ▼
 [ TimeoutError / Element Not Found ]             [ Assertion Error / URL Mismatch ]
          │                                               │
  1. Check Trace Viewer DOM Snapshot.             1. Inspect API Response Payload.
  2. Verify if locator changed in UI.             2. Verify DB state via SQL query.
  3. Verify element is inside iFrame/shadow DOM.  3. Check console logs for JS errors.
```

---

## 🔗 Related Topics
* [01. Automation Troubleshooting Cookbook](../22_TROUBLESHOOTING/01_automation_troubleshooting_cookbook.md)
* [Automation Debugging Cheat Sheet](../21_CHEAT_SHEETS/cheat-sheet-debugging.md)
