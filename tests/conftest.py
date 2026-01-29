"""
Pytest configuration and fixtures for Playwright tests.
"""
import pytest
from playwright.sync_api import Page, expect
from utils.config import BASE_URL, STANDARD_USER, STANDARD_PASSWORD
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

BASE_URL_NO_SLASH = BASE_URL.rstrip("/")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context arguments."""
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
    }


@pytest.fixture(scope="function")
def login_page(page: Page) -> LoginPage:
    """Navigate to login page and return LoginPage instance."""
    login_page = LoginPage(page)
    login_page.goto()
    return login_page


@pytest.fixture(scope="function")
def logged_in_page(login_page: LoginPage) -> Page:
    """
    Login as standard user and return the page.
    Use this fixture when your test needs to start from the inventory page.
    """
    login_page.login(STANDARD_USER, STANDARD_PASSWORD)
    # Wait for navigation to inventory page
    expect(login_page.page).to_have_url(f"{BASE_URL_NO_SLASH}/inventory.html")
    # Wait for inventory page to be fully loaded
    inventory_page = InventoryPage(login_page.page)
    inventory_page.is_loaded()
    return login_page.page


@pytest.fixture(scope="function")
def inventory_page(logged_in_page: Page) -> InventoryPage:
    """
    Return InventoryPage instance after logging in.
    Use this fixture when your test needs to interact with inventory page.
    """
    return InventoryPage(logged_in_page)
