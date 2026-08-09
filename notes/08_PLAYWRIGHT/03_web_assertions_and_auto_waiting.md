---
title: Playwright Web Assertions & Auto-Waiting Deep-Dive
category: 08_PLAYWRIGHT
subcategory: Assertions & Waiting
keywords:
  - Playwright Assertions
  - expect
  - auto-waiting
  - to_be_visible
  - to_have_text
  - to_have_url
  - Flaky Test Prevention
audience:
  - Quality Engineer
  - SDET
  - Automation Engineer
difficulty: beginner-intermediate
---

# ⏱️ Playwright Web Assertions & Auto-Waiting Deep-Dive

## 🎯 Overview: Why Playwright Auto-Waiting Eliminates Sleep

In legacy Selenium frameworks, engineers frequently inserted hardcoded delays (`time.sleep(5)`) to wait for elements to render. Playwright eliminates arbitrary sleep through **Auto-Waiting** and **Web-First Assertions**.

```
[ Action Triggered: .click() ] ──> Playwright Checks Automatically:
                                    1. Element Attached to DOM?
                                    2. Element Visible?
                                    3. Element Stable (Not animating)?
                                    4. Element Receives Events (Not obscured)?
                                    5. Element Enabled?
```

---

## 🛠️ Complete Web-First Assertions Cheat Sheet

Web-first assertions (`expect(locator)`) automatically retry until the condition is met or the timeout (default 5,000ms) expires.

```python
from playwright.sync_api import Page, expect

# 1. Visibility Assertions
expect(page.get_by_text("Order Confirmed")).to_be_visible(timeout=10000)
expect(page.locator("#spinner")).to_be_hidden()

# 2. Text Content Assertions
expect(page.get_by_role("heading", level=1)).to_have_text("Vendor Management Dashboard")
expect(page.locator(".status-banner")).to_contain_text("Approved")

# 3. Input Value & Attribute Assertions
expect(page.get_by_label("Tax ID")).to_have_value("TX-994821")
expect(page.get_by_role("button", name="Submit")).to_have_attribute("aria-disabled", "false")

# 4. Element State Assertions
expect(page.get_by_role("button", name="Approve")).to_be_enabled()
expect(page.get_by_role("button", name="Delete")).to_be_disabled()
expect(page.get_by_label("Accept Terms")).to_be_checked()

# 5. Page Level Assertions
expect(page).to_have_url("https://portal.example.com/dashboard")
expect(page).to_have_title("Dashboard - ERP Client")
```

---

## 🛑 Anti-Pattern: Generic Python Assert vs Web-First Expect

```python
# ❌ BAD: Evaluates value ONCE instantly; fails if DOM is still rendering!
assert page.get_by_text("Saved").is_visible()

# ✅ GOOD: Web-first assertion automatically retries for up to 5 seconds!
expect(page.get_by_text("Saved")).to_be_visible()
```

---

## 🔗 Related Topics
* [02. Locators Strategy](02_locators_strategy_accessibility_strictness.md)
* [06. Playwright Debugging & Troubleshooting](06_playwright_debugging_trace_viewer_troubleshooting.md)
