"""
City of Los Angeles General Services Department
Evaluation Program - Core Driver

Author: George Lin

Amazon Product Search Script

This script automates searching for products on Amazon and extracts
the name and price of the top search result.
"""

import asyncio
from playwright.async_api import Browser, Page, async_playwright


async def handle_continue_shopping_popup(page: Page) -> None:
    """
    Handle the 'Continue shopping' button if it appears on Amazon.

    Args:
        page: The Playwright page object
    """
    try:
        # Locate the continue shopping button using semantic role selector
        continue_button = page.get_by_role("button", name="Continue shopping")

        # Check if button is visible within 2 second timeout
        if await continue_button.is_visible(timeout=2000):
            await continue_button.click()
            print("Clicked 'Continue shopping' button")
    except:
        # If button doesn't exist or timeout occurs, continue silently
        print("No 'Continue shopping' button found, proceeding...")


async def search_product(page: Page, search_term: str) -> None:
    """
    Search for a product on Amazon.

    Args:
        page: The Playwright page object
        search_term: The product name to search for
    """
    # Locate search box using semantic role and aria-label
    search_box = page.get_by_role("searchbox", name="Search Amazon")
    await search_box.fill(search_term)

    # Click submit button using exact match to avoid ambiguity with other "Go" buttons
    submit_button = page.get_by_role("button", name="Go", exact=True)
    await submit_button.click()


async def get_top_result_info(page: Page) -> tuple[str, str]:
    """
    Extract the product name and price from the top search result.

    Args:
        page: The Playwright page object

    Returns:
        A tuple containing (product_name, price)
    """
    # Wait for search results to fully load before extracting data
    await page.wait_for_selector('[data-component-type="s-search-result"]')

    # return the first search result item
    first_result = page.locator('[data-component-type="s-search-result"]').first

    # get product name from the heading span element
    product_name = await first_result.locator("h2 span").text_content()

    # get price from the offscreen element (used for screen readers, contains clean price text)
    price = await first_result.locator(".a-price .a-offscreen").first.text_content()

    return product_name, price


async def main() -> None:
    """
    Main function to orchestrate the Amazon product search automation.
    """
    search_term = "Nintendo Switch 2"

    # Initialize Playwright and launch browser
    async with async_playwright() as p:
        # Launch Chromium in headed mode (headless=False shows browser window)
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            # Navigate to Amazon homepage with timeout handling
            print("Loading Amazon homepage...")
            await page.goto("https://www.amazon.com", timeout=30000)
            print("Amazon homepage loaded successfully")

            # Handle optional continue shopping popup
            await handle_continue_shopping_popup(page)

            # Perform product search
            await search_product(page, search_term)

            # Extract and display top result information
            product_name, price = await get_top_result_info(page)
            print(f"Successfully Found Product: {product_name}")
            print(f"Price: {price}")

            # Wait briefly to view results before closing
            await asyncio.sleep(2)

        except Exception as e:
            print(f"Error occurred: {type(e).__name__}: {e}")
            if "Timeout" in type(e).__name__:
                print("Amazon homepage failed to load within 30 seconds")
        finally:
            # Clean up browser resources
            await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
