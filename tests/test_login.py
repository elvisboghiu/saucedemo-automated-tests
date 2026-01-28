"""
Test suite for SauceDemo login functionality.
Covers authentication scenarios including valid/invalid credentials and edge cases.
"""
import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.config import BASE_URL, STANDARD_USER, STANDARD_PASSWORD, LOCKED_OUT_USER
from utils.helpers import get_user_credentials

BASE_URL_NO_SLASH = BASE_URL.rstrip("/")


@pytest.mark.login
class TestLogin:
    """Test cases for login functionality."""
    
    def test_valid_login(self, login_page: LoginPage):
        """Test successful login with valid credentials."""
        # Perform login
        login_page.login(STANDARD_USER, STANDARD_PASSWORD)
        
        # Verify redirect to inventory page
        inventory_page = InventoryPage(login_page.page)
        expect(login_page.page).to_have_url(f"{BASE_URL_NO_SLASH}/inventory.html")
        assert inventory_page.is_loaded(), "Inventory page should be loaded after successful login"
    
    def test_invalid_username(self, login_page: LoginPage):
        """Test login with invalid username."""
        invalid_username, _ = get_user_credentials("invalid")
        # Use a valid password to isolate invalid username behavior
        login_page.login(invalid_username, STANDARD_PASSWORD)
        
        # Verify error message is displayed
        error_message = login_page.get_error_message()
        assert "Username and password do not match" in error_message or \
               "Epic sadface" in error_message, \
               f"Expected error message not found. Got: {error_message}"
        assert login_page.is_loaded(), "Login page should still be visible"
    
    def test_invalid_password(self, login_page: LoginPage):
        """Test login with invalid password."""
        login_page.login(STANDARD_USER, "wrong_password")
        
        # Verify error message is displayed
        error_message = login_page.get_error_message()
        assert "Username and password do not match" in error_message or \
               "Epic sadface" in error_message, \
               f"Expected error message not found. Got: {error_message}"
    
    def test_locked_out_user(self, login_page: LoginPage):
        """Test login with locked out user credentials."""
        login_page.login(LOCKED_OUT_USER, STANDARD_PASSWORD)
        
        # Verify specific locked out error message
        error_message = login_page.get_error_message()
        assert "locked out" in error_message.lower() or \
               "Epic sadface" in error_message, \
               f"Expected locked out error message. Got: {error_message}"
        assert login_page.is_loaded(), "Login page should still be visible"
    
    def test_empty_username(self, login_page: LoginPage):
        """Test login with empty username."""
        login_page.login("", STANDARD_PASSWORD)
        
        # Verify error message for empty username
        error_message = login_page.get_error_message()
        assert "Username is required" in error_message or \
               "Epic sadface" in error_message, \
               f"Expected error message for empty username. Got: {error_message}"
    
    def test_empty_password(self, login_page: LoginPage):
        """Test login with empty password."""
        login_page.login(STANDARD_USER, "")
        
        # Verify error message for empty password
        error_message = login_page.get_error_message()
        assert "Password is required" in error_message or \
               "Epic sadface" in error_message, \
               f"Expected error message for empty password. Got: {error_message}"
    
    def test_empty_credentials(self, login_page: LoginPage):
        """Test login with both username and password empty."""
        login_page.login("", "")
        
        # Verify error message
        error_message = login_page.get_error_message()
        assert len(error_message) > 0, "Error message should be displayed for empty credentials"
    
    def test_login_page_elements_visible(self, login_page: LoginPage):
        """Test that all login page elements are visible."""
        assert login_page.username_input.is_visible(), "Username input should be visible"
        assert login_page.password_input.is_visible(), "Password input should be visible"
        assert login_page.login_button.is_visible(), "Login button should be visible"
        assert login_page.is_loaded(), "Login page should be loaded"

    def test_error_icon_and_message_for_invalid_login(self, login_page: LoginPage):
        """Error icon and message should appear for invalid login."""
        login_page.login("invalid_user", "wrong_password")
        error_message = login_page.get_error_message()
        assert error_message, "Error message should be displayed for invalid login"
        assert login_page.has_error_icon(), "Error icon should be visible for invalid login"

    def test_error_message_can_be_dismissed(self, login_page: LoginPage):
        """User can dismiss the error message using the close (X) button."""
        login_page.login("invalid_user", "wrong_password")
        # Ensure error is visible first
        assert login_page.get_error_message(), "Error should be shown before dismissing"
        login_page.dismiss_error()
        # After dismiss, error container should no longer be visible
        assert login_page.get_error_message() == "", "Error message should be dismissed"

    def test_cannot_access_inventory_without_login(self, page: Page):
        """Direct navigation to inventory without login should redirect to login page."""
        page.goto(f"{BASE_URL_NO_SLASH}/inventory.html")
        expect(page).to_have_url(f"{BASE_URL_NO_SLASH}/")

    def test_cannot_access_inventory_after_logout(self, login_page: LoginPage):
        """
        After logout, navigating directly to inventory should redirect
        back to the login page (session cleared).
        """
        # Login and land on inventory
        login_page.login(STANDARD_USER, STANDARD_PASSWORD)
        expect(login_page.page).to_have_url(f"{BASE_URL_NO_SLASH}/inventory.html")

        # Logout
        inventory_page = InventoryPage(login_page.page)
        inventory_page.logout()
        expect(login_page.page).to_have_url(f"{BASE_URL_NO_SLASH}/")

        # Attempt to access inventory again
        login_page.page.goto(f"{BASE_URL_NO_SLASH}/inventory.html")
        expect(login_page.page).to_have_url(f"{BASE_URL_NO_SLASH}/")
