import pytest
from playwright.sync_api import sync_playwright
from locators import SEARCH_BOX_SELECTOR, SEARCH_RESULTS_SELECTOR

def write_results_to_file(results, filename='search_results.txt'):
    """Write the search results to a text file."""
    with open(filename, 'w') as file:
        for result in results:
            file.write(result + '\n')

def print_results_to_console(results):
    """Print the search results to the console."""
    for result in results:
        print(result)

@pytest.fixture(scope='module')
def browser():
    """Set up and tear down Playwright browser."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set headless=True if you don't need a UI
        yield browser
        browser.close()

def test_google_search(browser):
    """Perform a Google search and handle the results."""
    page = browser.new_page()
    page.goto('https://www.google.com')

    # Wait for the search box to be available
    page.wait_for_selector(SEARCH_BOX_SELECTOR, timeout=60000)  # Increase timeout to 60 seconds
    
    # Perform search
    page.fill(SEARCH_BOX_SELECTOR, 'keyboard')
    page.press(SEARCH_BOX_SELECTOR, 'Enter')
    
    # Wait for search results to be visible
    page.wait_for_selector(SEARCH_RESULTS_SELECTOR, timeout=60000)  # Increase timeout to 60 seconds
    
    # Extract search results
    results = [result.text_content() for result in page.query_selector_all(SEARCH_RESULTS_SELECTOR)]
    
    # Get the first 10 results
    top_results = results[:10]
    
    # Print and write results
    print_results_to_console(top_results)
    write_results_to_file(top_results)
    
    # Close the page
    page.close()
