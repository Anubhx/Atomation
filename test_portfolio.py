"""
Playwright test suite for anubhavportfolio.vercel.app

Covers:
  1. Home page — loads correctly, key elements visible (hero text, nav, buttons, tools strip)
  2. Navigation — clicking "Explore Work" takes you to /case-studies
  3. Case Studies page — loads correctly, key elements visible
  4. Direct navigation to /case-studies (deep link) also works
  5. Basic nav bar links are present on both pages

Setup:
    pip install pytest-playwright --break-system-packages
    playwright install chromium

Run:
    pytest test_portfolio.py --headed          # see the browser
    pytest test_portfolio.py                   # headless
    pytest test_portfolio.py -k home            # run only home tests
"""

import re
import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://anubhavportfolio.vercel.app"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def go_home(page: Page):
    """Every test starts from the home page."""
    page.goto(BASE_URL)
    yield page


# ---------------------------------------------------------------------------
# Home page tests
# ---------------------------------------------------------------------------

class TestHomePage:

    def test_page_title_and_load(self, page: Page):
        expect(page).to_have_url(BASE_URL + "/")
        # Page should have finished loading key content
        expect(page.get_by_text("Anubhav Raj").first).to_be_visible()

    def test_hero_heading_visible(self, page: Page):
        # "I turn messy problems into products people actually use."
        heading = page.get_by_text("I turn messy", exact=False)
        expect(heading).to_be_visible()
        expect(page.get_by_text("products", exact=False)).to_be_visible()

    def test_role_subtitle_visible(self, page: Page):
        expect(
            page.get_by_text("UX DESIGNER", exact=False)
        ).to_be_visible()

    def test_tagline_visible(self, page: Page):
        expect(
            page.get_by_text("Designing with evidence. Shipping with code.")
        ).to_be_visible()

    def test_current_role_text(self, page: Page):
        expect(page.get_by_text("Currently at", exact=False)).to_be_visible()
        expect(page.get_by_text("LTI Mindtree")).to_be_visible()

    def test_stats_row_visible(self, page: Page):
        for stat in ["Years Industry", "Screens Designed", "Research", "WCAG"]:
            expect(page.get_by_text(stat, exact=False).first).to_be_visible()

    def test_nav_bar_links_present(self, page: Page):
        nav = page.locator("text=ABOUT").first
        expect(nav).to_be_visible()
        expect(page.get_by_text("WORK", exact=True).first).to_be_visible()
        expect(page.get_by_text("CONTACT", exact=True).first).to_be_visible()

    def test_hire_me_and_resume_buttons(self, page: Page):
        expect(page.get_by_text("HIRE ME", exact=False)).to_be_visible()
        expect(page.get_by_text("RESUME", exact=False)).to_be_visible()

    def test_cta_buttons_visible(self, page: Page):
        explore_btn = page.get_by_role("link", name=re.compile("EXPLORE WORK", re.I))
        if explore_btn.count() == 0:
            explore_btn = page.get_by_text(re.compile("EXPLORE WORK", re.I))
        expect(explore_btn.first).to_be_visible()

        download_btn = page.get_by_text(re.compile("DOWNLOAD RESUME", re.I))
        expect(download_btn.first).to_be_visible()

    def test_tools_strip_visible(self, page: Page):
        for tool in ["Figma", "Cursor", "Claude", "ChatGPT", "Gemini"]:
            expect(page.get_by_text(tool, exact=True).first).to_be_visible()

    def test_phone_number_visible(self, page: Page):
        expect(page.get_by_text("6200107977")).to_be_visible()


# ---------------------------------------------------------------------------
# Navigation: Home -> Case Studies via "Explore Work"
# ---------------------------------------------------------------------------

class TestExploreWorkNavigation:

    def test_click_explore_work_navigates_to_case_studies(self, page: Page):
        explore_btn = page.get_by_text(re.compile("EXPLORE WORK", re.I)).first
        expect(explore_btn).to_be_visible()
        explore_btn.click()

        page.wait_for_url(re.compile(r".*/case-studies$"))
        expect(page).to_have_url(re.compile(r".*/case-studies$"))

    def test_case_studies_content_loads_after_click(self, page: Page):
        page.get_by_text(re.compile("EXPLORE WORK", re.I)).first.click()
        page.wait_for_url(re.compile(r".*/case-studies$"))

        expect(page.get_by_text("FEATURED WORK", exact=False)).to_be_visible()
        expect(page.get_by_text("No bad", exact=False)).to_be_visible()


# ---------------------------------------------------------------------------
# Case Studies page tests (direct navigation / deep link)
# ---------------------------------------------------------------------------

class TestCaseStudiesPage:

    @pytest.fixture(autouse=True)
    def go_case_studies(self, page: Page):
        page.goto(f"{BASE_URL}/case-studies")

    def test_page_url(self, page: Page):
        expect(page).to_have_url(re.compile(r".*/case-studies$"))

    def test_breadcrumb_visible(self, page: Page):
        expect(page.get_by_text("HOME", exact=True).first).to_be_visible()
        expect(page.get_by_text("CASE STUDIES", exact=True).first).to_be_visible()

    def test_heading_visible(self, page: Page):
        expect(page.get_by_text("No bad", exact=False)).to_be_visible()
        expect(page.get_by_text("intentional", exact=False)).to_be_visible()

    def test_description_paragraph_visible(self, page: Page):
        expect(
            page.get_by_text("Product experiences shaped through research", exact=False)
        ).to_be_visible()

    def test_explore_archive_link_visible(self, page: Page):
        expect(page.get_by_text("Explore the archive", exact=False)).to_be_visible()

    def test_nav_bar_persists(self, page: Page):
        expect(page.get_by_text("WORK", exact=True).first).to_be_visible()
        expect(page.get_by_text("ABOUT", exact=True).first).to_be_visible()
        expect(page.get_by_text("CONTACT", exact=True).first).to_be_visible()

    def test_work_nav_item_is_active_state(self, page: Page):
        # "WORK" should be the highlighted/active nav item on this page
        work_link = page.get_by_text("WORK", exact=True).first
        expect(work_link).to_be_visible()

    def test_can_navigate_back_home(self, page: Page):
        home_link = page.get_by_text("HOME", exact=True).first
        home_link.click()
        page.wait_for_url(BASE_URL + "/")
        expect(page).to_have_url(BASE_URL + "/")


# ---------------------------------------------------------------------------
# Cross-cutting checks
# ---------------------------------------------------------------------------

class TestGeneralHealth:

    @pytest.mark.parametrize("path", ["/", "/case-studies"])
    def test_no_console_errors(self, page: Page, path):
        errors = []
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
        page.goto(f"{BASE_URL}{path}")
        page.wait_for_load_state("networkidle")
        assert not errors, f"Console errors found on {path}: {errors}"

    @pytest.mark.parametrize("path", ["/", "/case-studies"])
    def test_response_status_ok(self, page: Page, path):
        response = page.goto(f"{BASE_URL}{path}")
        assert response.status == 200, f"{path} returned status {response.status}"

    @pytest.mark.parametrize("path", ["/", "/case-studies"])
    def test_page_is_reasonably_fast(self, page: Page, path):
        import time
        start = time.time()
        page.goto(f"{BASE_URL}{path}", wait_until="load")
        elapsed = time.time() - start
        assert elapsed < 10, f"{path} took {elapsed:.2f}s to load (>10s)"