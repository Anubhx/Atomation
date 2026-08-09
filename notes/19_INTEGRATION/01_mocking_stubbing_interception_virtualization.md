---
title: Mocking, Stubbing & Service Virtualization in Playwright & Python
category: 19_INTEGRATION
subcategory: Mocking & Stubbing
keywords:
  - Mocking
  - Stubbing
  - Playwright Network Interception
  - page.route
  - Service Virtualization
  - unittest.mock
audience:
  - Quality Engineer
  - SDET
  - Automation Engineer
difficulty: intermediate
---

# 🎭 Mocking, Stubbing & Service Virtualization Field Guide

## 🎯 Overview: Definitions & Distinction

When testing isolated application components, external dependencies (payment gateways, third-party tax APIs, email services) are replaced with test double objects.

| Term | Definition & Behavior | Enterprise Example |
| :--- | :--- | :--- |
| **Stub** | Returns canned, hardcoded responses to calls made during test. | Hardcoded JSON payload for Tax API. |
| **Mock** | Object with expectation rules programmed to verify call count & parameters.| Verifying email service `send_email()` was called exactly once. |
| **Fake** | Working simplified implementation unsuitable for production. | In-memory SQLite DB replacing PostgreSQL. |
| **Service Virtualization**| Simulating entire third-party enterprise services over network protocols. | WireMock server simulating Stripe payment API responses. |

---

## 💻 Playwright Network Interception Example (`page.route`)

Intercept HTTP network calls at the browser level and return mock JSON payloads:

```python
from playwright.sync_api import Page, expect

def test_mock_third_party_payment_api(page: Page):
    # Intercept outgoing API request to third-party payment provider
    def handle_payment_route(route):
        # Full control: Return custom mock JSON and HTTP 200 code
        route.fulfill(
            status=200,
            content_type="application/json",
            body='{"status": "SUCCESS", "transaction_id": "MOCK-TX-994821"}'
        )

    # Register route interception pattern
    page.route("**/api/v1/external-payment-provider", handle_payment_route)

    # Trigger UI action that invokes the payment API
    page.goto("/checkout")
    page.get_by_role("button", name="Pay Now").click()

    # Assert UI renders mock success state
    expect(page.get_by_text("Transaction MOCK-TX-994821 Approved")).to_be_visible()
```

---

## 🔗 Related Topics
* [04. API Strategy & Mocking](../06_API_TESTING/04_api_testing_strategy_negative_contract_mocking.md)
* [01. Playwright Setup](../08_PLAYWRIGHT/01_playwright_python_setup_architecture.md)
