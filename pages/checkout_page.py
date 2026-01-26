"""
Page Object Model for SauceDemo Checkout Pages.
Handles both checkout information form and checkout overview.
"""
from playwright.sync_api import Page


class CheckoutPage:
    """Represents the SauceDemo checkout pages (information and overview)."""
    
    def __init__(self, page: Page):
        """
        Initialize CheckoutPage with a Playwright page object.
        
        Args:
            page: Playwright Page instance
        """
        self.page = page
        # Checkout Information Step
        self.first_name_input = page.locator('[data-test="firstName"]')
        self.last_name_input = page.locator('[data-test="lastName"]')
        self.postal_code_input = page.locator('[data-test="postalCode"]')
        self.continue_button = page.get_by_role("button", name="Continue")
        self.cancel_button = page.get_by_role("button", name="Cancel")
        self.error_message = page.locator('[data-test="error"]')
        
        # Checkout Overview Step
        self.finish_button = page.get_by_role("button", name="Finish")
        
        # Checkout Complete Step
        self.complete_header = page.locator('.complete-header')
        self.complete_text = page.locator('.complete-text')
        self.back_home_button = page.get_by_role("button", name="Back Home")
    
    def fill_customer_info(self, first_name: str, last_name: str, postal_code: str) -> None:
        """
        Fill in customer information on checkout page.
        
        Args:
            first_name: Customer first name
            last_name: Customer last name
            postal_code: Customer postal/zip code
        """
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)
    
    def continue_to_overview(self) -> None:
        """Click continue button to proceed to checkout overview."""
        self.continue_button.click()
    
    def finish_order(self) -> None:
        """Click finish button to complete the order."""
        self.finish_button.click()
    
    def get_error_message(self) -> str:
        """
        Get the error message text if present.
        
        Returns:
            Error message text, empty string if not present
        """
        if self.error_message.is_visible():
            return self.error_message.inner_text()
        return ""
    
    def get_confirmation_message(self) -> str:
        """
        Get the order confirmation message.
        
        Returns:
            Confirmation header text
        """
        if self.complete_header.is_visible():
            return self.complete_header.inner_text()
        return ""
    
    def is_checkout_complete(self) -> bool:
        """
        Check if checkout is complete.
        
        Returns:
            True if complete header is visible
        """
        return self.complete_header.is_visible()
    
    def back_to_home(self) -> None:
        """Click back home button to return to inventory."""
        self.back_home_button.click()
    
    def cancel_checkout(self) -> None:
        """Cancel checkout and return to cart."""
        self.cancel_button.click()
