---
title: Page Object Model (POM) Design Patterns & Example Classes
category: 10_AUTOMATION_ARCHITECTURE
subcategory: Page Object Model
keywords:
  - Page Object Model
  - POM
  - LoginPage
  - DashboardPage
  - PurchaseOrderPage
  - InvoicePage
  - InventoryPage
audience:
  - Quality Engineer
  - SDET
  - Automation Engineer
difficulty: intermediate
---

# 📄 Page Object Model (POM) Design Patterns & Field Guide

## 🎯 Overview: The Page Object Model Principle

The **Page Object Model (POM)** is a design pattern where web pages (or components) are represented by Python classes. Locators and UI actions are encapsulated inside the class, keeping test files clean and readable.

---

## 💻 Enterprise Page Object Class Library

### 1. `LoginPage` (`pages/login_page.py`)
```python
from playwright.sync_api import Page, expect

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.email_input = page.get_by_label("Email Address")
        self.password_input = page.get_by_label("Password")
        self.login_button = page.get_by_role("button", name="Log In")
        self.error_banner = page.locator(".alert-danger")

    def navigate(self):
        self.page.goto("/login")

    def login(self, email: str, password: str):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()
```

---

### 2. `DashboardPage` (`pages/dashboard_page.py`)
```python
from playwright.sync_api import Page, expect

class DashboardPage:
    def __init__(self, page: Page):
        self.page = page
        self.heading = page.get_by_role("heading", level=1)
        self.procurement_menu = page.get_by_role("link", name="Procurement")
        self.finance_menu = page.get_by_role("link", name="Finance")
        self.user_avatar = page.locator("#user-profile-avatar")

    def navigate_to_purchase_orders(self):
        self.procurement_menu.click()
        self.page.get_by_role("link", name="Purchase Orders").click()
```

---

### 3. `PurchaseOrderPage` (`pages/purchase_order_page.py`)
```python
from playwright.sync_api import Page

class PurchaseOrderPage:
    def __init__(self, page: Page):
        self.page = page
        self.create_po_button = page.get_by_role("button", name="Create New PO")
        self.vendor_dropdown = page.get_by_label("Select Vendor")
        self.sku_input = page.get_by_label("SKU / Material")
        self.quantity_input = page.get_by_label("Quantity")
        self.submit_po_button = page.get_by_role("button", name="Submit Purchase Order")

    def create_purchase_order(self, vendor_name: str, sku: str, quantity: int):
        self.create_po_button.click()
        self.vendor_dropdown.select_option(label=vendor_name)
        self.sku_input.fill(sku)
        self.quantity_input.fill(str(quantity))
        self.submit_po_button.click()
```

---

### 4. `InvoicePage` (`pages/invoice_page.py`)
```python
from playwright.sync_api import Page

class InvoicePage:
    def __init__(self, page: Page):
        self.page = page
        self.invoice_number_input = page.get_by_label("Invoice Number")
        self.amount_input = page.get_by_label("Total Invoice Amount")
        self.approve_button = page.get_by_role("button", name="Approve Invoice")
        self.status_badge = page.get_by_test_id("invoice-status-badge")

    def approve_invoice(self, invoice_number: str):
        self.page.goto(f"/finance/invoices/{invoice_number}")
        self.approve_button.click()
```

---

### 5. `InventoryPage` (`pages/inventory_page.py`)
```python
from playwright.sync_api import Page

class InventoryPage:
    def __init__(self, page: Page):
        self.page = page
        self.search_input = page.get_by_placeholder("Search inventory SKU...")
        self.stock_table_row = page.get_by_role("row")

    def get_available_stock(self, sku: str) -> str:
        self.search_input.fill(sku)
        self.page.keyboard.press("Enter")
        return self.page.locator(f"tr[data-sku='{sku}'] .available-qty").text_content()
```

---

## 🔗 Related Topics
* [01. Framework Architecture](01_enterprise_automation_framework_design.md)
* [03. Combined UI+API+DB Testing Pattern](03_combined_ui_api_db_testing_pattern.md)
