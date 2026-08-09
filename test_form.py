from playwright.sync_api import Page, expect

BASE_URL = "http://127.0.0.1:8080"

def test_contact_form(page: Page):
    page.goto(f"{BASE_URL}/contact.html")

    # Fill text fields
    page.get_by_label("Full Name (Required):").fill("Anubhav Raj")
    page.get_by_label("Email Address (Required):").fill("anubhav@example.com")
    page.get_by_label("Account Password (Min 8 Characters):").fill("Password123")
    page.get_by_label("Telephone Number:").fill("+91 9876543210")
    page.get_by_label("Website URL:").fill("https://example.com")
    page.get_by_label("Search Term:").fill("Playwright")

    # Verify values
    expect(page.get_by_label("Full Name (Required):")).to_have_value(
        "Anubhav Raj"
    )

    expect(page.get_by_label("Email Address (Required):")).to_have_value(
        "anubhav@example.com"
    )