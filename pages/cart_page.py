"""
Page Object Model for SauceDemo Shopping Cart Page.
"""
from playwright.sync_api import Page, Locator


class CartPage:
    """Represents the SauceDemo shopping cart page."""
    
    def __init__(self, page: Page):
        """
        Initialize CartPage with a Playwright page object.
        
        Args:
            page: Playwright Page instance
        """
        self.page = page
        self.cart_items = page.locator('.cart_item')
        self.continue_shopping_button = page.get_by_role("button", name="Continue Shopping")
        self.checkout_button = page.get_by_role("button", name="Checkout")
    
    def is_loaded(self) -> bool:
        """
        Check if cart page is loaded.
        
        Returns:
            True if cart page elements are visible
        """
        return self.checkout_button.is_visible() or self.continue_shopping_button.is_visible()
    
    def get_items(self) -> list[dict]:
        """
        Get all items in the cart with their details.
        
        Returns:
            List of dictionaries containing item information
        """
        # Wait for cart items to be visible before reading them
        # This ensures items are fully rendered before we try to read their content
        if self.cart_items.count() > 0:
            self.cart_items.first.wait_for(state="visible")
        
        items = []
        for item in self.cart_items.all():
            name = item.locator('.inventory_item_name').inner_text()
            price = item.locator('.inventory_item_price').inner_text()
            quantity = item.locator('.cart_quantity').inner_text()
            items.append({
                'name': name,
                'price': price,
                'quantity': quantity
            })
        return items
    
    def remove_item(self, item_name: str) -> None:
        """
        Remove an item from cart by its name.
        
        Args:
            item_name: Name of the product to remove
        """
        item = self.cart_items.filter(has_text=item_name)
        remove_button = item.locator('button').filter(has_text='Remove')
        remove_button.click()
    
    def proceed_to_checkout(self) -> None:
        """Click the checkout button to proceed to checkout."""
        self.checkout_button.click()
    
    def continue_shopping(self) -> None:
        """Click continue shopping to return to inventory page."""
        self.continue_shopping_button.click()
    
    def is_empty(self) -> bool:
        """
        Check if cart is empty.
        
        Returns:
            True if cart has no items
        """
        return self.cart_items.count() == 0
