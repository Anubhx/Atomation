"""
STEP 3: The main ways to find elements ("locators") in Playwright.

Priority order (top ones are more robust / recommended by Playwright itself):
  1. get_by_role      - by accessibility role (button, link, heading, textbox...)
  2. get_by_text       - by visible text
  3. get_by_label      - form inputs, by their <label>
  4. get_by_placeholder - form inputs, by placeholder text
  5. get_by_alt_text    - images, by alt attribute
  6. get_by_title       - by the title="" attribute
  7. get_by_test_id     - by data-testid="" (best when devs add it for you)
  8. locator (CSS)      - raw CSS selectors, last resort / most fragile
"""

from playwright.sync_api import Page, expect

BASE_URL = "https://anubhavportfolio.vercel.app"


def test_get_by_role(page: Page):
    """
    BEST OPTION. Finds elements the way a screen reader would -
    by their role (link, button, heading, navigation...) and their
    accessible name. Ignores how the text is split across tags.
    """
    page.goto(BASE_URL)
    expect(page.get_by_role("link", name="Explore Work")).to_be_visible()
    expect(page.get_by_role("navigation", name="Primary navigation")).to_be_visible()
    expect(page.get_by_role("heading", level=1)).to_be_visible()


def test_get_by_text(page: Page):
    """
    Good for plain paragraphs/labels. Use exact=False for partial
    matches, since exact=True (the default) requires the ENTIRE
    text content of the element to match exactly.
    """
    page.goto(BASE_URL)
    expect(page.get_by_text("LTI Mindtree").first).to_be_visible()
    expect(page.get_by_text("Designing with evidence", exact=False)).to_be_visible()


def test_get_by_alt_text(page: Page):
    """
    Targets <img alt="..."> - great for logos/photos.
    From your aria snapshot: img "Anubhav Raj", img "Figma logo", etc.
    """
    page.goto(BASE_URL)
    expect(page.get_by_alt_text("Figma logo")).to_be_visible()
    expect(page.get_by_alt_text("Anubhav Raj")).to_be_visible()


def test_get_by_test_id(page: Page):
    """
    Targets data-testid="..." attributes. MOST STABLE of all -
    doesn't break even if text or styling changes - but only works
    if you (or the dev) added data-testid attributes in the HTML.
    Example if a button had data-testid="hire-me-btn":
        page.get_by_test_id("hire-me-btn").click()
    """
    pass  # your site doesn't have these yet - optional to add later


def test_css_locator_last_resort(page: Page):
    """
    Raw CSS selectors via page.locator(). Works, but brittle - breaks
    the moment class names change. Use only when nothing else fits.
    """
    page.goto(BASE_URL)
    # example: any <a> tag whose href contains "case-studies"
    expect(page.locator('a[href*="case-studies"]').first).to_be_visible()


def test_chaining_and_filtering(page: Page):
    """
    Bonus: you can chain locators to narrow down within a section,
    and use .filter() to pick one of several matching elements.
    """
    page.goto(BASE_URL)

    # find the "Selected case studies" region, then find a link INSIDE it
    case_studies_section = page.get_by_role("region", name="Selected case studies")
    expect(
        case_studies_section.get_by_role("link", name="Read case study: FlowWise")
    ).to_be_visible()

    # filter: among all links, find the one containing this text
    expect(
        page.get_by_role("link").filter(has_text="Zomato Group Ordering")
    ).to_be_visible()