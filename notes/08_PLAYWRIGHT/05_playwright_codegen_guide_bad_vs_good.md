---
title: Playwright Codegen Mastery (Bad Generated Code vs Production POM)
category: 08_PLAYWRIGHT
subcategory: Codegen & Refactoring
keywords:
  - Playwright Codegen
  - npx playwright codegen
  - Code Refactoring
  - Page Object Model
  - Fragile Locators
audience:
  - Quality Engineer
  - SDET
  - Automation Engineer
difficulty: beginner-intermediate
---

# 🎥 Playwright Codegen Mastery: Refactoring Generated Code

## 🎯 Overview: The Role of Playwright Codegen

Playwright Codegen (`npx playwright codegen https://portal.example.com`) is an interactive recorder that auto-generates test scripts as you perform actions in the browser. 

> [!IMPORTANT]
> **Codegen is a kickstarter, NOT production code**. Raw generated scripts contain fragile locators, hardcoded values, and zero Page Object abstraction.

---

## 🆚 BAD (Raw Codegen) vs. GOOD (Production Page Object)

### ❌ BAD: Raw Auto-Generated Script (`test_raw_codegen.py`)
```python
# Raw output from playwright codegen - DO NOT USE IN PRODUCTION
def test_login_raw(page):
    page.goto("https://portal.example.com/login")
    page.locator("div:nth-child(2) > input").click() # ❌ Fragile CSS
    page.locator("div:nth-child(2) > input").fill("admin@example.com") # ❌ Hardcoded creds
    page.locator("xpath=//button[contains(text(),'Submit')]").click() # ❌ Unbound XPath
    page.wait_for_timeout(5000) # ❌ Hardcoded Sleep!
```

---

### ✅ GOOD: Refactored Production Page Object (`test_refactored_pom.py`)
```python
# Production-grade Page Object Model structure
class LoginPage:
    def __init__(self, page):
        self.page = page
        self.email_input = page.get_by_label("Email Address")
        self.password_input = page.get_by_label("Password")
        self.submit_button = page.get_by_role("button", name="Log In")

    def login(self, email: str, password: str):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()

def test_login_production(page: Page, user_credentials):
    login_page = LoginPage(page)
    page.goto("/login")
    login_page.login(user_credentials["email"], user_credentials["password"])
    
    # Web-first assertion (No hardcoded sleep!)
    expect(page).to_have_url("/dashboard")
```

---

## 🔗 Related Topics
* [02. Locators Strategy](02_locators_strategy_accessibility_strictness.md)
* [02. Page Object Model Best Practices](../10_AUTOMATION_ARCHITECTURE/02_page_object_model_pom_best_practices.md)
