"""
Page Object Model for SauceDemo Login Page.
"""
from playwright.sync_api import Page
from utils.config import BASE_URL


class LoginPage:
    """Represents the SauceDemo login page."""
    
    def __init__(self, page: Page):
        """
        Initialize LoginPage with a Playwright page object.
        
        Args:
            page: Playwright Page instance
        """
        self.page = page
        self.username_input = page.get_by_placeholder("Username")
        self.password_input = page.get_by_placeholder("Password")
        self.login_button = page.get_by_role("button", name="Login")
        self.error_message = page.locator('[data-test="error"]')
    
    def goto(self) -> None:
        """Navigate to the login page."""
        self.page.goto(BASE_URL)
    
    def login(self, username: str, password: str) -> None:
        """
        Perform login action.
        
        Args:
            username: Username to login with
            password: Password to login with
        """
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
    
    def get_error_message(self) -> str:
        """
        Get the error message text if present.
        
        Returns:
            Error message text, empty string if not present
        """
        if self.error_message.is_visible():
            return self.error_message.inner_text()
        return ""
    
    def is_loaded(self) -> bool:
        """
        Check if login page is loaded.
        
        Returns:
            True if login button is visible
        """
        return self.login_button.is_visible()
