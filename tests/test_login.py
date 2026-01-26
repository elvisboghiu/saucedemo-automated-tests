"""
Test suite for SauceDemo login functionality.
Covers authentication scenarios including valid/invalid credentials and edge cases.
"""
import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.config import STANDARD_USER, STANDARD_PASSWORD, LOCKED_OUT_USER
from utils.helpers import get_user_credentials


@pytest.mark.login
class TestLogin:
    """Test cases for login functionality."""
    
    def test_valid_login(self, login_page: LoginPage):
        """Test successful login with valid credentials."""
        # Perform login
        login_page.login(STANDARD_USER, STANDARD_PASSWORD)
        
        # Verify redirect to inventory page
        inventory_page = InventoryPage(login_page.page)
        expect(login_page.page).to_have_url("https://www.saucedemo.com/inventory.html")
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
