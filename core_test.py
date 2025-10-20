"""
Test Suite for Amazon Product Search Automation

Author: George Lin

This test module uses pytest and pytest-playwright to test the
Amazon product search functionality.
"""

import pytest
from playwright.sync_api import Page, expect
from core import handle_continue_shopping_popup, search_product, get_top_result_info
