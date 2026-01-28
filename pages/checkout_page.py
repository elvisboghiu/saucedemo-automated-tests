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
        self.overview_items = page.locator(".cart_item")
        self.subtotal_label = page.locator(".summary_subtotal_label")
        self.tax_label = page.locator(".summary_tax_label")
        self.total_label = page.locator(".summary_total_label")
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

    def is_step_one_loaded(self) -> bool:
        """
        Check whether checkout step one (customer information) is loaded.

        Returns:
            True if all required input fields are visible.
        """
        return (
            self.first_name_input.is_visible()
            and self.last_name_input.is_visible()
            and self.postal_code_input.is_visible()
        )
    
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

    def get_overview_items(self) -> list[dict]:
        """
        Get all items listed on the checkout overview page.

        Returns:
            List of dictionaries containing item name, price and quantity.
        """
        items: list[dict] = []
        for item in self.overview_items.all():
            name = item.locator(".inventory_item_name").inner_text()
            price = item.locator(".inventory_item_price").inner_text()
            quantity = item.locator(".cart_quantity").inner_text()
            items.append(
                {
                    "name": name,
                    "price": price,
                    "quantity": quantity,
                }
            )
        return items

    @staticmethod
    def _parse_amount_from_label(label_text: str) -> float:
        """
        Parse a monetary amount from a summary label such as
        'Item total: $39.98' or 'Tax: $3.20'.
        """
        parts = label_text.split("$")
        if len(parts) < 2:
            return 0.0
        number_part = parts[-1].strip()
        try:
            return float(number_part)
        except ValueError:
            return 0.0

    def get_subtotal(self) -> float:
        """Return the item subtotal value from the overview page."""
        text = self.subtotal_label.inner_text()
        return self._parse_amount_from_label(text)

    def get_tax(self) -> float:
        """Return the tax value from the overview page."""
        text = self.tax_label.inner_text()
        return self._parse_amount_from_label(text)

    def get_total(self) -> float:
        """Return the total value from the overview page."""
        text = self.total_label.inner_text()
        return self._parse_amount_from_label(text)

    def is_overview_loaded(self) -> bool:
        """
        Check whether checkout overview (step two) is loaded.

        Returns:
            True if the subtotal label is visible.
        """
        return self.subtotal_label.is_visible()
