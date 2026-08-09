---
title: Playwright Python Quick Reference Cheat Sheet
category: 21_CHEAT_SHEETS
subcategory: Playwright
keywords:
  - Playwright Cheat Sheet
  - Playwright Python Syntax
  - Locators Cheat Sheet
  - Page Actions
audience:
  - Quality Engineer
  - SDET
difficulty: beginner-intermediate
---

# 🎭 Playwright Python Quick Reference Cheat Sheet

## 🚀 Navigation & Page Basics
```python
page.goto("https://portal.example.com")
page.reload()
page.go_back()
```

## 🎯 Locators (Accessibility-First)
```python
page.get_by_role("button", name="Submit").click()
page.get_by_label("Email Address").fill("user@example.com")
page.get_by_text("Order Confirmed", exact=True)
page.get_by_placeholder("Search...")
page.get_by_test_id("po-status")
page.locator("css=button.primary")
```

## ⚡ User Interactions
```python
page.get_by_label("Username").fill("admin")
page.get_by_role("button", name="Save").click()
page.get_by_label("Country").select_option(label="United States")
page.get_by_label("Accept Terms").check()
page.get_by_label("Accept Terms").uncheck()
page.get_by_role("button", name="Upload").set_input_files("invoice.pdf")
page.get_by_role("menu").hover()
```

## ⏱️ Web Assertions (`expect`)
```python
from playwright.sync_api import expect

expect(locator).to_be_visible()
expect(locator).to_be_hidden()
expect(locator).to_have_text("Approved")
expect(locator).to_contain_text("Pending")
expect(locator).to_have_value("TX-9941")
expect(locator).to_be_enabled()
expect(locator).to_be_disabled()
expect(page).to_have_url("https://portal.example.com/dashboard")
```

## 🌐 Network Interception
```python
page.route("**/api/v1/tax", lambda route: route.fulfill(
    status=200, body='{"tax_rate": 0.08}'
))
```
