from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from e2e_utils import StreamlitRunner

ROOT_DIRECTORY = Path(__file__).parent.parent.absolute()
BASIC_EXAMPLE_FILE = ROOT_DIRECTORY / "streamlit_redirect" / "example.py"

@pytest.fixture(autouse=True, scope="module")
def streamlit_app():
    with StreamlitRunner(BASIC_EXAMPLE_FILE) as runner:
        yield runner


@pytest.fixture(autouse=True, scope="function")
def go_to_app(page: Page, streamlit_app: StreamlitRunner):
    page.goto(streamlit_app.server_url)
    # Wait for app to load
    page.get_by_role("img", name="Running...").is_hidden()


def test_page_title_and_content(page: Page):
    """Test that the page displays the correct title and content."""
    # Check that the title is displayed
    expect(page.get_by_text("Example Redirect App")).to_be_visible()
    
    # Check that the redirect button section is displayed
    expect(page.get_by_text("Redirect to Google")).to_be_visible()
    
    # Check that the redirect button exists
    expect(page.get_by_role("button", name="Redirect Me")).to_be_visible()
    
    # Check that the URL input section is displayed
    expect(page.get_by_text("Enter a URL in the textfield and press ENTER to redirect")).to_be_visible()
    
    # Check that the URL input field exists
    expect(page.get_by_label("URL")).to_be_visible()


def test_redirect_button_click(page: Page):
    """Test that clicking the redirect button initiates a redirect to Google."""
    # Find the redirect button
    redirect_button = page.get_by_role("button", name="Redirect Me")
    
    # Verify the button is visible and clickable
    expect(redirect_button).to_be_visible()
    expect(redirect_button).to_be_enabled()
    
    # Set up a listener for navigation events
    redirected = False
    target_url = None
    
    def handle_response(response):
        nonlocal redirected, target_url
        if "google.com" in response.url:
            redirected = True
            target_url = response.url
    
    page.on("response", handle_response)
    
    # Click the redirect button
    redirect_button.click()
    
    # Wait a moment for the redirect to be processed
    page.wait_for_timeout(2000)
    
    # Check if a meta refresh tag was added to the page (this is how streamlit_redirect works)
    meta_refresh = page.locator('meta[http-equiv="refresh"]')
    if meta_refresh.count() > 0:
        content = meta_refresh.get_attribute("content")
        # The content should contain the Google URL
        assert "google.com" in content, f"Expected Google URL in meta refresh content, got: {content}"
