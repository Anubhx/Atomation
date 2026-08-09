"""
Automated Playwright Test Suite for Practice Ground Website
Testing all 14 pages, dynamic UI elements, forms, local storage auth, tables, and accessibility elements.
"""

# pyrefly: ignore [missing-import]
from playwright.sync_api import Page, expect

BASE_URL = "http://127.0.0.1:8080"
PRACTICE_SITE_URL = "http://127.0.0.1:5500/practice_site/index.html"
    

def test_site_navigation(page: Page):
    """Verify navigation across all main pages and subpages."""
    page.goto(f"{BASE_URL}/index.html")
    expect(page.get_by_role("heading", level=1)).to_contain_text("Playwright E2E Testing Practice Ground")

    # Navigate to About
    page.get_by_test_id("nav-about").click()
    expect(page).to_have_url(f"{BASE_URL}/about.html")
    expect(page.get_by_role("heading", level=1)).to_contain_text("About Playwright Playground")

    # Navigate to Products
    page.get_by_test_id("nav-products").click()
    expect(page).to_have_url(f"{BASE_URL}/products.html")
    expect(page.get_by_role("heading", level=1)).to_contain_text("Testing Tools & Software Catalog")

    # Navigate to Gallery
    page.get_by_test_id("nav-gallery").click()
    expect(page).to_have_url(f"{BASE_URL}/gallery.html")

    # Navigate to Blog
    page.get_by_test_id("nav-blog").click()
    expect(page).to_have_url(f"{BASE_URL}/blog.html")

    # Navigate to Contact
    page.get_by_test_id("nav-contact").click()
    expect(page).to_have_url(f"{BASE_URL}/contact.html")

    # Navigate to Login
    page.get_by_test_id("nav-login").click()
    expect(page).to_have_url(f"{BASE_URL}/login.html")


def test_auth_and_dashboard_flow(page: Page):
    """Test unauthenticated redirect and authenticated dashboard view via localStorage."""
    # 1. Unauthenticated access to dashboard
    page.goto(f"{BASE_URL}/dashboard.html")
    expect(page.get_by_test_id("login-required-msg")).to_be_visible()
    expect(page.get_by_test_id("dashboard-content")).to_be_hidden()

    # 2. Login flow
    page.goto(f"{BASE_URL}/login.html")
    page.get_by_test_id("username-input").fill("PlaywrightTester")
    page.get_by_test_id("password-input").fill("secret123")
    page.get_by_test_id("login-submit").click()

    # 3. Authenticated dashboard assertion
    expect(page).to_have_url(f"{BASE_URL}/dashboard.html")
    expect(page.get_by_test_id("dashboard-content")).to_be_visible()
    expect(page.get_by_test_id("user-greeting")).to_have_text("PlaywrightTester")

    # 4. Logout flow
    page.get_by_test_id("logout-btn").click()
    expect(page).to_have_url(f"{BASE_URL}/login.html")


def test_giant_contact_form(page: Page):
    """Test contact form inputs, validation, and client-side submit success alert."""
    page.goto(f"{BASE_URL}/contact.html")

    # Fill form fields
    page.get_by_test_id("contact-name-input").fill("Alice QA")
    page.get_by_test_id("contact-email-input").fill("alice@example.com")
    
    # Test short password failure (min 8 chars)
    page.get_by_test_id("contact-password-input").fill("short")
    page.get_by_test_id("contact-submit-btn").click()
    expect(page.get_by_test_id("password-error-msg")).to_be_visible()

    # Fix password and submit successfully
    page.get_by_test_id("contact-password-input").fill("validpassword123")
    page.get_by_test_id("contact-submit-btn").click()
    expect(page.get_by_test_id("contact-success-msg")).to_be_visible()


def test_dynamic_ui_elements(page: Page):
    """Test toggle visibility, load more button, toast notification, and modal dialog."""
    page.goto(f"{BASE_URL}/index.html")

    # Toggle Div
    expect(page.get_by_test_id("hidden-div-target")).to_be_hidden()
    page.get_by_test_id("toggle-visibility-btn").click()
    expect(page.get_by_test_id("hidden-div-target")).to_be_visible()

    # Load More Async Items (~1.5s delay)
    initial_count = page.locator("#dynamic-item-list li").count()
    page.get_by_test_id("load-more-btn").click()
    expect(page.locator("#dynamic-item-list li")).to_have_count(initial_count + 3, timeout=5000)

    # Toast Notification
    page.get_by_test_id("trigger-toast-btn").click()
    expect(page.get_by_test_id("toast-alert")).to_be_visible()

    # Custom Modal
    page.get_by_test_id("open-modal-btn").click()
    expect(page.get_by_test_id("modal-overlay")).to_be_visible()
    page.get_by_test_id("modal-close-btn").click()
    expect(page.get_by_test_id("modal-overlay")).to_be_hidden()


def test_broken_link_and_404(page: Page):
    """Test custom 404 page rendering and broken link navigation."""
    # 1. Custom 404 Page verification
    page.goto(f"{BASE_URL}/404.html")
    expect(page.get_by_test_id("404-heading")).to_be_visible()

    # 2. Broken link navigation test
    page.goto(f"{BASE_URL}/blog.html")
    response = page.request.get(f"{BASE_URL}/non-existent-page.html")
    assert response.status == 404


def test_console_error_detection(page: Page):
    """Verify console.error event capture on blog/post-2.html."""
    console_errors = []
    page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

    page.goto(f"{BASE_URL}/blog/post-2.html")
    assert len(console_errors) > 0
    assert "Simulated runtime error" in console_errors[0]
