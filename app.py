"""
City of Los Angeles General Services Department
Evaluation Program - Web Service (Bonus Challenge)

Author: George Lin

Flask Web Application for Amazon Product Search Automation

This module provides a web interface and REST API endpoint to trigger
the Amazon product search automation remotely via HTTP requests.
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import asyncio
from datetime import datetime
import sys
from io import StringIO
from playwright.async_api import async_playwright

from script import handle_continue_shopping_popup, search_product, get_top_result_info

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for API requests

# Simple in-memory rate limiting (per IP)
request_tracker = {}
RATE_LIMIT_SECONDS = 15  # Minimum seconds between requests per IP


def check_rate_limit(ip_address):
    """Check if the IP has exceeded rate limits"""
    current_time = datetime.now()

    if ip_address in request_tracker:
        last_request = request_tracker[ip_address]
        time_diff = (current_time - last_request).total_seconds()

        if time_diff < RATE_LIMIT_SECONDS:
            remaining = RATE_LIMIT_SECONDS - time_diff
            return False, remaining

    request_tracker[ip_address] = current_time
    return True, 0


@app.route("/")
def index():
    """Serve the main web interface"""
    return render_template("index.html")


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({"status": "healthy", "service": "Amazon Product Search API"})


@app.route("/api/search", methods=["POST"])
def search_product_api():
    """
    API endpoint to search for a product on Amazon.

    Request JSON:
        {
            "search_term": "Nintendo Switch 2",
            "headless": true
        }

    Returns:
        JSON with product information, logs, and status
    """
    # Get client IP for rate limiting
    client_ip = request.remote_addr

    # Check rate limit
    allowed, remaining = check_rate_limit(client_ip)
    if not allowed:
        return (
            jsonify(
                {
                    "success": False,
                    "error": f"Rate limit exceeded. Please wait {int(remaining)} seconds before trying again.",
                    "logs": [],
                }
            ),
            429,
        )

    # Get request data
    data = request.get_json()
    if not data or "search_term" not in data:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Missing 'search_term' in request",
                    "logs": [],
                }
            ),
            400,
        )

    search_term = data.get("search_term", "").strip()
    headless = data.get("headless", True)

    if not search_term:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Search term cannot be empty",
                    "logs": [],
                }
            ),
            400,
        )

    # Capture logs
    logs = []

    def log(message):
        """Helper to capture logs"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        logs.append(log_entry)
        print(log_entry)

    # Run the automation
    try:
        log(f"Starting search for: {search_term}")

        # Run async automation
        result = asyncio.run(run_automation(search_term, headless, log))

        if result["success"]:
            log(f"Success! Found: {result['product_name']}")
            log(f"Price: {result['price']}")
        else:
            log(f"Error: {result['error']}")

        return jsonify(
            {
                "success": result["success"],
                "product_name": result.get("product_name"),
                "price": result.get("price"),
                "error": result.get("error"),
                "logs": logs,
            }
        )

    except Exception as e:
        log(f"Unexpected error: {type(e).__name__}: {str(e)}")
        return (
            jsonify(
                {
                    "success": False,
                    "error": f"Unexpected error: {str(e)}",
                    "logs": logs,
                }
            ),
            500,
        )


async def run_automation(search_term, headless, log_func):
    """
    Run the Amazon product search automation.

    Args:
        search_term: Product to search for
        headless: Whether to run browser in headless mode
        log_func: Function to call for logging

    Returns:
        Dictionary with success status, product info, or error
    """
    try:
        log_func("Initializing browser...")

        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(headless=headless)
            page = await browser.new_page()

            try:
                # Navigate to Amazon
                log_func("Navigating to Amazon.com...")
                await page.goto("https://www.amazon.com", timeout=30000)
                log_func("Amazon homepage loaded")

                # Handle popup if present
                log_func("Checking for popups...")
                await handle_continue_shopping_popup(page)

                # Perform search
                log_func(f"Searching for: {search_term}")
                await search_product(page, search_term)

                # Extract results
                log_func("Extracting product information...")
                product_name, price = await get_top_result_info(page)

                return {
                    "success": True,
                    "product_name": product_name,
                    "price": price,
                    "error": None,
                }

            except Exception as e:
                error_msg = f"{type(e).__name__}: {str(e)}"
                log_func(f"Error during automation: {error_msg}")
                return {
                    "success": False,
                    "product_name": None,
                    "price": None,
                    "error": error_msg,
                }

            finally:
                log_func("Closing browser...")
                await browser.close()

    except Exception as e:
        error_msg = f"Failed to initialize browser: {str(e)}"
        log_func(error_msg)
        return {
            "success": False,
            "product_name": None,
            "price": None,
            "error": error_msg,
        }


if __name__ == "__main__":
    print("=" * 60)
    print("Amazon Product Search Web Service")
    print("=" * 60)
    print("\nStarting development server...")
    print("Web UI: http://localhost:5000")
    print("API Endpoint: http://localhost:5000/api/search")
    print("Health Check: http://localhost:5000/api/health")
    print("\nPress CTRL+C to stop the server")
    print("=" * 60)

    # Run in debug mode for development
    app.run(host="0.0.0.0", port=5000, debug=True)
