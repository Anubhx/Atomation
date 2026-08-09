---
title: Playwright Locator Strategy, Accessibility & Strict Mode
category: 08_PLAYWRIGHT
subcategory: Locators
keywords:
  - Playwright Locator
  - get_by_role
  - get_by_label
  - get_by_text
  - get_by_placeholder
  - get_by_test_id
  - Strict Mode Violation
  - Locator Chaining
audience:
  - Quality Engineer
  - SDET
  - Automation Engineer
difficulty: intermediate
---

# 🎯 Playwright Locator Strategy, Accessibility & Strict Mode

## 🎯 Overview: Locator Hierarchy & Priority

Playwright recommends **Accessibility-First Locators** that reflect how real users and screen readers interact with the application.

```
Priority 1: page.get_by_role("button", name="Submit") ──> Accessibility Tree (Resilient)
Priority 2: page.get_by_label("Email Address")      ──> Form Labels (User-centric)
Priority 3: page.get_by_placeholder("Enter password")──> Input Placeholders
Priority 4: page.get_by_test_id("submit-po-btn")   ──> Dedicated Test Attribute
Priority 5: page.locator("css=button.btn-primary")  ──> CSS / XPath (Last Resort)
```

---

## 🛠️ Complete Locator API Reference

```python
# 1. Role-based Locator (Buttons, Links, Checkboxes, Dialogs)
page.get_by_role("button", name="Approve Invoice")
page.get_by_role("heading", name="Purchase Orders", level=1)

# 2. Form Label Locator
page.get_by_label("Vendor Tax Identifier")

# 3. Text Locator (Exact vs Partial)
page.get_by_text("Order submitted successfully", exact=True)

# 4. Placeholder & Test ID
page.get_by_placeholder("Search by PO number...")
page.get_by_test_id("invoice-status-badge")

# 5. Locator Filtering & Chaining
page.get_by_role("listitem").filter(has_text="Product 1").get_by_role("button", name="Add")

# 6. Ordinal Selectors (.first, .last, .nth)
page.get_by_role("row").nth(2)
```

---

## ⚠️ Strict Mode Violations & Resolution

Playwright enforces **Strict Mode**: if a locator matches MORE THAN ONE element on the DOM, calling an action (like `.click()`) raises a `StrictnessViolationError`.

### BAD Code (Triggers Strict Mode Error):
```python
# Fails if 5 submit buttons exist on page!
page.locator("button").click() 
```

### GOOD Code (Resolved Strict Mode):
```python
# Option A: Scope to specific form container
page.locator("#invoice-form").get_by_role("button", name="Submit").click()

# Option B: Use exact text matching
page.get_by_role("button", name="Submit Invoice", exact=True).click()

# Option C: Use filtering
page.get_by_role("button").filter(has_text="Submit Invoice").click()
```

---

## 🔗 Related Topics
* [01. Playwright Setup](01_playwright_python_setup_architecture.md)
* [03. Web Assertions & Auto-Waiting](03_web_assertions_and_auto_waiting.md)
* [05. Playwright Codegen Mastery](05_playwright_codegen_guide_bad_vs_good.md)
