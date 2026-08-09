"""
STEP 1: Portfolio E2E UI Automation Test Suite

REQUIREMENT SPECIFICATION:
This test suite verifies basic accessibility, landing page content visibility,
navigation header links, and main call-to-action routing for the portfolio web application.

Target Application: Anubhav Portfolio (https://anubhavportfolio.vercel.app)

Execution Commands:
    pytest test_step1.py --headed --slowmo 1000
    pytest test_step1.py
"""

# pyrefly: ignore [missing-import]
from playwright.sync_api import Page, expect

# REQUIREMENT: Global target base URL for portfolio deployment environment
BASE_URL = "https://anubhavportfolio.vercel.app"


# REQUIREMENT: [REQ-01] Homepage Initial Load & Core Identity Verification
# Objective: Ensure the homepage loads successfully and main navigation header / brand identity ("Home") is visible.
# Acceptance Criteria:
#   1. Navigate to BASE_URL.
#   2. Verify that the "Home" navigation link is rendered and visible.
def test_homepage_loads(page: Page):
    # 1. Go to the homepage
    page.goto(BASE_URL)

    # 2. Check that your name / brand identity appears somewhere on the page
    expect(page.get_by_role("link", name="Home")).to_be_visible()


# REQUIREMENT: [REQ-02] Hero Banner Content Visibility
# Objective: Verify that primary value proposition headlines and professional role tags are displayed on the landing page.
# Acceptance Criteria:
#   1. Navigate to BASE_URL.
#   2. Verify presence of hero text snippet "people actually use".
#   3. Verify presence of role title text "UX Designer".
def test_hero_heading_visible(page: Page):
    # 1. Go to the homepage
    page.goto(BASE_URL)

    # 2. Check that the hero heading appears somewhere on the page
    # expect(page.get_by_text("I turn messy").first).to_be_visible()
    expect(page.get_by_text("people actually use", exact=False).first).to_be_visible()
    expect(page.get_by_text("UX Designer",exact=False ).first).to_be_visible() 


# REQUIREMENT: [REQ-03] Navigation Bar Elements Visibility
# Objective: Ensure critical navigation elements are rendered on the header navigation menu.
# Acceptance Criteria:
#   1. Navigate to BASE_URL.
#   2. Verify that the exact "Work" navigation link is rendered and visible.
#testing the navbar elements
def test_navbar_elements(page: Page):
    # 1. Go to the homepage
    page.goto(BASE_URL)

    # 2. Check that the navbar elements are visible
    # expect(page.get_by_role("link", name="About")).to_be_visible()
    expect(page.get_by_role("link", name="Work", exact=True)).to_be_visible()
    # expect(page.get_by_role("link", name="Contact")).to_be_visible()


# REQUIREMENT: [REQ-04] Navigation Header - "Work" Link Routing
# Objective: Validate routing from homepage header to Case Studies / Work portfolio page.
# Acceptance Criteria:
#   1. Navigate to BASE_URL.
#   2. Click "Work" header navigation link.
#   3. Verify URL updates to BASE_URL + "/case-studies".
def test_work_link(page: Page):
    # 1. Go to the homepage
    page.goto(BASE_URL)
    # 2. Click on the "Work" link and check that it navigates to the case studies page

    page.get_by_role("link", name="Work", exact=True).click()
    expect(page).to_have_url(BASE_URL + "/case-studies")


# REQUIREMENT: [REQ-05] Navigation Header - "About" Link Routing
# Objective: Validate routing from homepage header to About Me section/page.
# Acceptance Criteria:
#   1. Navigate to BASE_URL.
#   2. Click "About" header navigation link.
#   3. Verify URL updates to BASE_URL + "/about".
def test_about_link(page: Page):
    # 1. Go to the homepage
    page.goto(BASE_URL)
    # 2. Click on the about link and check that it navigates to the about page
    page.get_by_role("link", name="About").click()
    expect(page).to_have_url(BASE_URL + "/about")


# REQUIREMENT: [REQ-06] Navigation Header - "Contact" Link Routing
# Objective: Validate routing from homepage header to Contact section/page.
# Acceptance Criteria:
#   1. Navigate to BASE_URL.
#   2. Click "Contact" header navigation link.
#   3. Verify URL updates to BASE_URL + "/contact".
def test_contact_link(page: Page):
    # 1. Go to the homepage
    page.goto(BASE_URL)
    # 2. Click on the contact link and check that it navigates to the contact page
    page.get_by_role("link", name="Contact").click()
    expect(page).to_have_url(BASE_URL + "/contact")


# REQUIREMENT: [REQ-07] Hero CTA Button - "Explore Work →" Navigation & Page Verification
# Objective: Validate Hero section primary Call-To-Action button visibility, click interaction, page navigation, and target page content loading.
# Acceptance Criteria:
#   1. Navigate to BASE_URL.
#   2. Verify CTA link "Explore Work →" is visible.
#   3. Click "Explore Work →" CTA link.
#   4. Verify URL navigates to BASE_URL + "/case-studies".
#   5. Confirm target page renders heading text "Case Studies".
def test_explore_work_link_button (page: Page):
    # 1. Go to the homepage
    page.goto(BASE_URL)
    expect(
        page.get_by_role(
            "link",
            name="Explore Work →",
            exact=True
        )
    ).to_be_visible()

    page.get_by_role(
        "link",
        name="Explore Work →",
        exact=True
    ).click()

    expect(page).to_have_url(
        BASE_URL + "/case-studies"
    )
    expect(
        page.get_by_text(
            "Case Studies",
            exact=True
        )
    ).to_be_visible()
    
def test_hero_heading_visible_by_role(page: Page):
    page.goto(BASE_URL)

    # Target it by ROLE instead of exact text. 
    # Playwright automatically flattens all the text inside the
    # heading (across the <em> tag and everything) into one string
    # when you search by role + name. This is the more robust way.
    heading = page.get_by_role(
        "heading",
        name="I turn messy problems into products people actually use.",
        level=1,
    )
    expect(heading).to_be_visible()
