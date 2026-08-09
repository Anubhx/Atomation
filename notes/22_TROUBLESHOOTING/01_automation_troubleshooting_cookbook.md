---
title: Automation Troubleshooting Cookbook (Playwright & Pytest Issues)
category: 22_TROUBLESHOOTING
subcategory: Automation Troubleshooting
keywords:
  - Playwright Troubleshooting
  - Element Not Found
  - Strict Mode Violation
  - Timeout Waiting For Locator
  - Passes Locally Fails In CI
  - Flaky Test Cookbook
audience:
  - Quality Engineer
  - SDET
  - Automation Engineer
difficulty: intermediate
---

# 🍳 Automation Troubleshooting Cookbook: Diagnostic Decision Recipes

## 🎯 Problem 1: "Playwright Element Not Found" / `TimeoutError`

### Symptoms
Test fails after 30 seconds with error: `playwright._impl._errors.TimeoutError: Timeout 30000ms exceeded waiting for locator(...)`.

### Possible Causes
1. Element is inside an `<iframe>` or Shadow DOM container.
2. Element text changed dynamically due to localization or backend data.
3. Element is hidden behind a loading spinner or modal backdrop.

### Diagnostic Steps
1. Open Trace Viewer: `playwright show-trace trace.zip`.
2. Inspect the DOM Snapshot at the exact timestamp of failure.
3. Check browser console logs for unhandled JS errors suppressing UI render.

### Fix
```python
# ❌ BAD: Direct locator assuming main frame
page.get_by_role("button", name="Pay").click()

# ✅ FIX: Scope locator inside correct iframe
frame = page.frame_locator("iframe[name='payment-frame']")
frame.get_by_role("button", name="Pay").click()
```

---

## 🎯 Problem 2: "Strict Mode Violation Error"

### Symptoms
Error: `playwright._impl._errors.Error: strict mode violation: locator("button") resolved to 4 elements`.

### Possible Causes
Your locator matches multiple elements on the active page.

### Diagnostic Steps
Run `page.locator("button").count()` in debug console to see how many matching elements exist.

### Fix
```python
# ✅ FIX: Chain locator or filter by specific text/container
page.locator("#invoice-form").get_by_role("button", name="Submit", exact=True).click()
```

---

## 🎯 Problem 3: "Test Passes Locally but Fails in CI"

### Symptoms
Test executes 100% green on local developer laptop (headed/headless), but throws intermittent timeouts in GitHub Actions / Jenkins pipelines.

### Possible Causes
1. CI server CPU/memory throttling causes slower UI rendering than local laptop.
2. CI environment network latency to Staging API is higher.
3. Hardcoded local screen resolutions (`1920x1080` vs CI default `1280x720`).

### Fix
1. Explicitly configure viewport size in `conftest.py` / `pytest.ini`: `viewport = {"width": 1920, "height": 1080}`.
2. Use Web-First Assertions (`expect(locator).to_be_visible()`) instead of instantaneous boolean checks.
3. Use `--tracing=retain-on-failure` to inspect CI DOM snapshots.

---

## 🎯 Problem 4: "Login Works Manually but Fails in Automation"

### Symptoms
Manually filling login form works fine in regular browser, but Playwright script triggers "Invalid CAPTCHA" or "Access Denied" bot detection.

### Fix
Pass custom `user_agent` or bypass bot detection in staging via test header flags.

---

## 🔗 Related Topics
* [06. Playwright Debugging & Trace Viewer](../08_PLAYWRIGHT/06_playwright_debugging_trace_viewer_troubleshooting.md)
* [Automation Debugging Cheat Sheet](../21_CHEAT_SHEETS/cheat-sheet-debugging.md)
