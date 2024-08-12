import pytest
import logging
from playwright.sync_api import sync_playwright

@pytest.fixture(scope='module')
def browser():
    """Set up and tear down Playwright browser."""
    logging.info("Starting the browser...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set headless=True if you don't need a UI
        yield browser
        browser.close()
    logging.info("Browser closed.")