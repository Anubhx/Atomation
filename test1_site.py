from playwright.sync_api import Page, expect

BASE_URL = "http://127.0.0.1:8080"

# def test_site_heading(page: Page):
#     page.goto(f"{BASE_URL}/index.html")
#     expect(
#         page.get_by_role("heading", level=1)
#     ).to_contain_text("Playwright E2E Testing Practice Ground")

#     print(
#         "Page heading verified successfully: Playwright E2E Testing Practice Ground"
#     )

# def test_download_file_link(page: Page):

#     """Verify the download button link is working and file is downloaded successfully."""    
#     page.goto(f"{BASE_URL}/index.html")
#     verifty_download = page.get_by_role("link", name="Download Sample File")

#     expect(verifty_download).to_be_visible()
#     with page.expect_download() as download_info:
#         verifty_download.click()
#     download = download_info.value
#     assert download.suggested_filename == "sample.txt"
#     print(f"File downloaded successfully: {download.suggested_filename}")
# def test_about_link(page: Page):
#     """Verify the About link navigation and page content."""

#     page.goto(f"{BASE_URL}/index.html")

#     about_link = page.get_by_test_id("nav-about")

#     expect(about_link).to_be_visible()
#     about_link.click()

#     expect(page).to_have_url(f"{BASE_URL}/about.html") 
#     print(f"Navigation to About page successful: {page.url}")

def test_contact_link(page: Page):
    """Verify the Contact link navigation and page content."""

    page.goto(f"{BASE_URL}/index.html")

    contact_link = page.get_by_test_id("nav-contact")

    expect(contact_link).to_be_visible()
    contact_link.click()

    expect(page).to_have_url(f"{BASE_URL}/contact.html") 
    print(f"Navigation to Contact page successful: {page.url}") 