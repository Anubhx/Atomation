---
title: Playwright User Interactions (Forms, Uploads, Dialogs & iFrames)
category: 08_PLAYWRIGHT
subcategory: Interactions
keywords:
  - Playwright Interactions
  - click
  - fill
  - select_option
  - file upload
  - dialogs
  - iframe
audience:
  - Quality Engineer
  - SDET
difficulty: beginner-intermediate
---

# 🖱️ Playwright User Interactions: Forms, Files, Dialogs & iFrames

## 🎯 Overview: Simulating Real User Actions

Playwright provides high-level APIs to trigger clicks, text entry, file uploads, select dropdowns, handle native browser alert dialogs, and interact with nested iFrames.

---

## 💻 Form Input & Selection Interaction Recipes

```python
from playwright.sync_api import Page

def test_user_form_interactions(page: Page):
    # 1. Fill Text Inputs
    page.get_by_label("Username").fill("admin_user")
    
    # 2. Key Press (Keyboard shortcuts, Enter key)
    page.get_by_label("Search").fill("PO-9941")
    page.get_by_label("Search").press("Enter")
    
    # 3. Dropdown Select Option (by value, label, or index)
    page.get_by_label("Payment Terms").select_option(label="NET 30 Days")
    
    # 4. Checkbox & Radio Buttons
    page.get_by_label("I agree to terms").check()
    page.get_by_label("Express Shipping").check()
    
    # 5. Mouse Hover & Drag-and-Drop
    page.get_by_role("menuitem", name="Reports").hover()
    page.locator("#source-item").drag_to(page.locator("#target-bin"))
```

---

## 📁 File Uploads, Native Dialogs & iFrames

### 1. File Upload Interaction
```python
# Upload single file
page.get_by_label("Upload Invoice PDF").set_input_files("tests/data/invoice_sample.pdf")

# Clear uploaded file
page.get_by_label("Upload Invoice PDF").set_input_files([])
```

### 2. Native Alert / Confirm Dialog Handling
```python
# Register dialog handler BEFORE triggering the action!
page.on("dialog", lambda dialog: dialog.accept()) # Or dialog.dismiss()

page.get_by_role("button", name="Delete Account").click()
```

### 3. Nested iFrame Interaction
```python
# Access frame by name attribute or locator selector
frame = page.frame_locator("iframe[name='payment-frame']")
frame.get_by_label("Credit Card Number").fill("4111222233334444")
frame.get_by_role("button", name="Pay Now").click()
```

---

## 🔗 Related Topics
* [02. Locators Strategy](02_locators_strategy_accessibility_strictness.md)
* [03. Web Assertions & Auto-Waiting](03_web_assertions_and_auto_waiting.md)
