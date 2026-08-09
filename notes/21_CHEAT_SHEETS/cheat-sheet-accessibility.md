---
title: Accessibility (a11y) Quick Reference Cheat Sheet
category: 21_CHEAT_SHEETS
subcategory: Accessibility
keywords:
  - Accessibility Cheat Sheet
  - WCAG
  - axe-core
  - Playwright a11y
audience:
  - Quality Engineer
  - SDET
difficulty: beginner
---

# ♿ Accessibility (a11y) Quick Reference Cheat Sheet

## 📋 Core WCAG Checkpoints
* **Keyboard Navigation**: All interactive controls accessible via `Tab` key without keyboard traps.
* **Accessible Names**: All buttons, inputs, links have discernible accessible names via text, `<label>`, or `aria-label`.
* **Color Contrast**: Normal text contrast ratio $\ge 4.5:1$; large text $\ge 3:1$.

## 💻 Playwright axe-core Verification
```python
from axe_playwright_python.sync_playwright import Axe

def test_page_accessibility(page):
    page.goto("https://portal.example.com")
    results = Axe().run(page)
    assert len(results.violations) == 0, f"a11y violations found: {results.violations_summary()}"
```
