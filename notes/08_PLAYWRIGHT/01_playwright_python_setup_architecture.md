---
title: Playwright Python Setup, Architecture & Pytest Integration
category: 08_PLAYWRIGHT
subcategory: Core Setup
keywords:
  - Playwright Python
  - Playwright Setup
  - BrowserContext
  - Page
  - Chromium Firefox WebKit
  - Pytest Playwright
audience:
  - Quality Engineer
  - SDET
  - Automation Engineer
difficulty: beginner-intermediate
---

# 🎭 Playwright Python Setup & Architecture Field Guide

## 🎯 Overview: Playwright Architecture

Playwright operates out-of-process via WebSocket connection to browser engines (Chromium, Firefox, WebKit). Unlike Selenium (WebDriver HTTP polling), Playwright communicates directly with Chrome DevTools Protocol (CDP) and browser engines—delivering fast, reliable, auto-waiting execution.

```
 [ Pytest Runner ] ──(Python Sync/Async API)──> [ Playwright Driver Node ] ──(WebSocket / CDP)──> [ Chromium / WebKit / Firefox ]
```

---

## ⚙️ Environment Setup & Installation

```bash
# 1. Install pytest-playwright plugin
pip install pytest-playwright

# 2. Download browser binaries (Chromium, Firefox, WebKit)
playwright install

# 3. Verify installation
pytest --version
```

---

## 🏛️ Playwright Object Model: Browser vs. Context vs. Page

```
 [ Browser ]: Single instance of Chromium/Firefox (Expensive to launch, shared).
       │
       ▼
 [ BrowserContext ]: Isolated incognito session (Fast <10ms, isolated cookies/storage).
       │
       ▼
 [ Page ]: Single browser tab / window.
```

### Pytest Fixture Lifecycle Example

```python
import pytest
from playwright.sync_api import Page, expect

def test_isolated_browser_session(page: Page):
    """
    pytest-playwright automatically injects an isolated `page` fixture
    belonging to a new `BrowserContext` for every test function!
    """
    page.goto("https://portal.example.com/login")
    expect(page).to_have_title("Enterprise Portal - Login")
```

---

## 🔗 Related Topics
* [02. Locators Strategy](02_locators_strategy_accessibility_strictness.md)
* [03. Web Assertions & Auto-Waiting](03_web_assertions_and_auto_waiting.md)
* [Playwright Cheat Sheet](../21_CHEAT_SHEETS/cheat-sheet-playwright.md)
