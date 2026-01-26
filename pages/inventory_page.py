"""
Page Object Model for SauceDemo Inventory/Products Page.
"""
from playwright.sync_api import Page, Locator


class InventoryPage:
    """Represents the SauceDemo inventory/products page."""
    
    def __init__(self, page: Page):
        """
        Initialize InventoryPage with a Playwright page object.
        
        Args:
            page: Playwright Page instance
        """
        self.page = page
        self.cart_icon = page.locator('.shopping_cart_link')
        self.sort_dropdown = page.locator('[data-test="product_sort_container"]')
        self.product_items = page.locator('.inventory_item')
        self.menu_button = page.locator('#react-burger-menu-btn')
        self.logout_link = page.locator('#logout_sidebar_link')
    
    def is_loaded(self) -> bool:
        """
        Check if inventory page is loaded.
        
        Returns:
            True if products are visible
        """
        return self.product_items.first.is_visible()
    
    def add_item_to_cart(self, item_name: str) -> None:
        """
        Add an item to cart by its name.
        
        Args:
            item_name: Name of the product to add
        """
        # Find the product item container
        item = self.page.locator('.inventory_item').filter(has_text=item_name)
        # Click the "Add to cart" button for this item
        add_button = item.locator('button').filter(has_text='Add to cart')
        add_button.click()
    
    def remove_item_from_cart(self, item_name: str) -> None:
        """
        Remove an item from cart by its name.
        
        Args:
            item_name: Name of the product to remove
        """
        item = self.page.locator('.inventory_item').filter(has_text=item_name)
        remove_button = item.locator('button').filter(has_text='Remove')
        remove_button.click()
    
    def get_cart_count(self) -> int:
        """
        Get the number of items in the cart from the badge.
        
        Returns:
            Number of items in cart, 0 if badge is not visible
        """
        cart_badge = self.page.locator('.shopping_cart_badge')
        if cart_badge.count() == 0:
            return 0
        if cart_badge.is_visible(timeout=0):
            return int(cart_badge.inner_text())
        return 0
    
    def sort_by(self, option: str) -> None:
        """
        Sort products by the given option.
        
        Args:
            option: Sort option value (e.g., 'az', 'za', 'lohi', 'hilo')
        """
        self.sort_dropdown.select_option(option)
    
    def open_cart(self) -> None:
        """Click on the cart icon to navigate to cart page."""
        self.cart_icon.click()
    
    def get_product_names(self) -> list[str]:
        """
        Get list of all product names on the page.
        
        Returns:
            List of product names
        """
        product_name_elements = self.page.locator('.inventory_item_name')
        return [name.inner_text() for name in product_name_elements.all()]
    
    def logout(self) -> None:
        """Logout from the application."""
        self.menu_button.click()
        self.logout_link.wait_for(state="visible")
        self.logout_link.click()
