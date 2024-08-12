import pytest
import logging
from playwright.sync_api import sync_playwright
from locators import SEARCH_BOX_SELECTOR, SEARCH_RESULTS_SELECTOR

# Configure the logger
logger = logging.getLogger()  # Get the root logger
logger.setLevel(logging.INFO)  # Set the logging level

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Set the level for the console handler

# Create a file handler
file_handler = logging.FileHandler("GoogleLog.log")
file_handler.setLevel(logging.INFO)  # Set the level for the file handler

# Define the log format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

def write_results_to_file(results, filename='search_results.txt'):
    """Write the search results to a text file."""
    logging.info(f"Writing results to file: {filename}")
    with open(filename, 'w') as file:
        for result in results:
            file.write(result + '\n')
    logging.info("Results successfully written to file.")

def print_results_to_console(results):
    """Print the search results to the console."""
    logging.info("Printing results to console:")
    for result in results:
        print(result)

@pytest.fixture(scope='module')
def browser():
    """Set up and tear down Playwright browser."""
    logging.info("Starting the browser...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set headless=True if you don't need a UI
        yield browser
        browser.close()
    logging.info("Browser closed.")

def test_google_search(browser):
    """Perform a Google search and handle the results."""
    page = browser.new_page()
    logging.info("Navigating to Google...")
    page.goto('https://www.google.com')

    # Wait for the search box to be available
    logging.info("Waiting for the search box to be available...")
    page.wait_for_selector(SEARCH_BOX_SELECTOR, timeout=60000)  # Increase timeout to 60 seconds
    
    # Perform search
    logging.info("Performing search for 'keyboard'...")
    page.fill(SEARCH_BOX_SELECTOR, 'keyboard')
    page.press(SEARCH_BOX_SELECTOR, 'Enter')
    
    # Wait for search results to be visible
    logging.info("Waiting for search results...")
    page.wait_for_selector(SEARCH_RESULTS_SELECTOR, timeout=60000)  # Increase timeout to 60 seconds
    
    # Extract search results
    logging.info("Extracting search results...")
    results = [result.text_content() for result in page.query_selector_all(SEARCH_RESULTS_SELECTOR)]
    
    # Get the first 10 results
    top_results = results[:10]
    
    # Print and write results
    print_results_to_console(top_results)
    write_results_to_file(top_results)
    
    # Close the page
    logging.info("Closing the page...")
    page.close()
    logging.info("Test completed.")
