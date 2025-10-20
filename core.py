"""
City of Los Angeles General Services Department
Evaluation Program - Core Driver

Author: George Lin

Amazon Product Search Script

This script automates searching for products on Amazon and extracts
the name and price of the top search result.
"""

from playwright.sync_api import Page, sync_playwright
import time


def handle_continue_shopping_popup(page: Page) -> None:
    """
    Handle the 'Continue shopping' button if it appears on Amazon.

    Args:
        page: The Playwright page object
    """
    try:
        # Locate the continue shopping button using semantic role selector
        continue_button = page.get_by_role("button", name="Continue shopping")

        # Check if button is visible within 2 second timeout
        if continue_button.is_visible(timeout=2000):
            continue_button.click()
            print("Clicked 'Continue shopping' button")
    except:
        # If button doesn't exist or timeout occurs, continue silently
        print("No 'Continue shopping' button found, proceeding...")


def search_product(page: Page, search_term: str) -> None:
    """
    Search for a product on Amazon.

    Args:
        page: The Playwright page object
        search_term: The product name to search for
    """
    # Locate search box using semantic role and aria-label
    search_box = page.get_by_role("searchbox", name="Search Amazon")
    search_box.fill(search_term)

    # Click submit button using exact match to avoid ambiguity with other "Go" buttons
    submit_button = page.get_by_role("button", name="Go", exact=True)
    submit_button.click()


def get_top_result_info(page: Page) -> tuple[str, str]:
    """
    Extract the product name and price from the top search result.

    Args:
        page: The Playwright page object

    Returns:
        A tuple containing (product_name, price)
    """
    # Wait for search results to fully load before extracting data
    page.wait_for_selector('[data-component-type="s-search-result"]')

    # Get the first search result item
    first_result = page.locator('[data-component-type="s-search-result"]').first

    # Extract product name from the heading span element
    product_name = first_result.locator("h2 span").text_content()

    # Extract price from the offscreen element (used for screen readers, contains clean price text)
    price = first_result.locator(".a-price .a-offscreen").first.text_content()

    return product_name, price


def main() -> None:
    """
    Main function to orchestrate the Amazon product search automation.
    """
    search_term = "Nintendo Switch 2"

    # Initialize Playwright and launch browser
    with sync_playwright() as p:
        # Launch Chromium in headed mode (headless=False shows browser window)
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Navigate to Amazon homepage
        page.goto("https://www.amazon.com")

        # Handle optional continue shopping popup
        handle_continue_shopping_popup(page)

        # Perform product search
        search_product(page, search_term)

        # Extract and display top result information
        product_name, price = get_top_result_info(page)
        print(f"Successfully Found Product: {product_name}")
        print(f"Price: {price}")

        # Wait briefly to view results before closing
        time.sleep(2)

        # Clean up browser resources
        browser.close()


if __name__ == "__main__":
    main()
