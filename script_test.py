"""
Test Suite for Amazon Product Search Automation

Author: George Lin

This test module uses pytest and pytest-playwright to test the
Amazon product search functionality.
"""

import pytest
import asyncio
from playwright.sync_api import Page, expect
from playwright.async_api import async_playwright
from script import handle_continue_shopping_popup, search_product, get_top_result_info


def test_complete_nintendo_switch_2_search_workflow():
    """
    Comprehensive test that validates automated script:
    1. Navigate to Amazon
    2. Handle continue shopping popup
    3. Search for Nintendo Switch 2
    4. Extract product info
    5. Verify price is $499.00

    This test wraps async functions and runs them in an async context.
    """

    async def run_test():
        search_term = "Nintendo Switch 2"

        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            try:
                # Step 1: Navigate to Amazon homepage
                print("\n=== Step 1: Navigating to Amazon ===")
                await page.goto("https://www.amazon.com", timeout=30000)
                assert "amazon.com" in page.url
                print(f"Successfully navigated to: {page.url}")

                # Step 2: Handle continue shopping popup
                print("\n=== Step 2: Handling Continue Shopping Popup ===")
                await handle_continue_shopping_popup(page)
                # Verify still on Amazon after handling popup
                assert "amazon.com" in page.url
                print("Popup handled successfully")

                # Test calling popup handler twice (second time should be safe/no-op)
                await handle_continue_shopping_popup(page)
                assert "amazon.com" in page.url
                print("Second popup handler call completed safely")

                # Step 3: Ensure page is ready and search box is visible
                print("\n=== Step 3: Verifying Search Box ===")
                await page.wait_for_load_state("domcontentloaded")
                search_box = page.get_by_role("searchbox", name="Search Amazon")
                await search_box.wait_for(state="visible", timeout=10000)
                print("Search box is visible and ready")

                # Step 4: Perform search
                print(f"\n=== Step 4: Searching for '{search_term}' ===")
                await search_product(page, search_term)

                # Wait for search results page to load
                await page.wait_for_url("**/s?**", timeout=10000)
                assert "/s?" in page.url or "/s/" in page.url
                print(f"Search results loaded: {page.url}")

                # Step 5: Extract top result info
                print("\n=== Step 5: Extracting Product Information ===")
                product_name, price = await get_top_result_info(page)

                # Verify product name
                assert product_name is not None
                assert isinstance(product_name, str)
                assert len(product_name) > 0
                print(f"Product Name: {product_name}")

                # Verify price format
                assert price is not None
                assert isinstance(price, str)
                assert "$" in price
                print(f"Product Price: {price}")

                # Step 6: Verify price is exactly $499.00
                print("\n=== Step 6: Verifying Price ===")
                from playwright.async_api import expect

                await expect(page.locator(".a-price .a-offscreen").first).to_have_text(
                    "$499.00"
                )
                print("✓ Price verified: $499.00")

                # Verify the extracted price variable also matches
                assert (
                    price == "$499.00"
                ), f"Expected price to be '$499.00' but got '{price}'"
                print("\n=== All Tests Passed Successfully ===")

            finally:
                await browser.close()

    # Run the async test
    asyncio.run(run_test())
