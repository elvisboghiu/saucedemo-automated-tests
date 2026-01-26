"""
Test suite for SauceDemo shopping cart functionality.
Covers adding/removing items, cart persistence, and cart badge updates.
"""
import pytest
from playwright.sync_api import expect
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from utils.helpers import load_test_data


@pytest.mark.cart
class TestCart:
    """Test cases for shopping cart functionality."""
    
    def test_add_single_item_to_cart(self, inventory_page: InventoryPage):
        """Test adding a single item to cart."""
        test_data = load_test_data()
        item_name = test_data["products"]["backpack"]
        
        # Add item to cart
        initial_count = inventory_page.get_cart_count()
        inventory_page.add_item_to_cart(item_name)
        
        # Verify cart count increased
        assert inventory_page.get_cart_count() == initial_count + 1, \
            f"Cart count should be {initial_count + 1} after adding one item"
    
    def test_add_multiple_items_to_cart(self, inventory_page: InventoryPage):
        """Test adding multiple items to cart."""
        test_data = load_test_data()
        items = [
            test_data["products"]["backpack"],
            test_data["products"]["bike_light"],
            test_data["products"]["bolt_tshirt"]
        ]
        
        # Add multiple items
        for item_name in items:
            inventory_page.add_item_to_cart(item_name)
        
        # Verify cart count matches number of items added
        assert inventory_page.get_cart_count() == len(items), \
            f"Cart count should be {len(items)} after adding {len(items)} items"
    
    def test_remove_item_from_inventory_page(self, inventory_page: InventoryPage):
        """Test removing an item from cart from inventory page."""
        test_data = load_test_data()
        item_name = test_data["products"]["backpack"]
        
        # Add item first
        inventory_page.add_item_to_cart(item_name)
        assert inventory_page.get_cart_count() == 1, "Item should be added to cart"
        
        # Remove item
        inventory_page.remove_item_from_cart(item_name)
        
        # Verify cart count decreased
        assert inventory_page.get_cart_count() == 0, "Cart should be empty after removing item"
    
    def test_remove_item_from_cart_page(self, inventory_page: InventoryPage):
        """Test removing an item from cart page."""
        test_data = load_test_data()
        item_name = test_data["products"]["backpack"]
        
        # Add item and navigate to cart
        inventory_page.add_item_to_cart(item_name)
        inventory_page.open_cart()
        
        cart_page = CartPage(inventory_page.page)
        assert cart_page.is_loaded(), "Cart page should be loaded"
        
        # Verify item is in cart
        items = cart_page.get_items()
        assert len(items) == 1, "Cart should have one item"
        assert items[0]["name"] == item_name, f"Cart should contain {item_name}"
        
        # Remove item from cart page
        cart_page.remove_item(item_name)
        
        # Verify cart is empty
        assert cart_page.is_empty(), "Cart should be empty after removing item"
    
    def test_cart_persistence(self, inventory_page: InventoryPage):
        """Test that cart persists when navigating between pages."""
        test_data = load_test_data()
        item_name = test_data["products"]["fleece_jacket"]
        
        # Add item to cart
        inventory_page.add_item_to_cart(item_name)
        assert inventory_page.get_cart_count() == 1, "Item should be added"
        
        # Navigate to cart
        inventory_page.open_cart()
        cart_page = CartPage(inventory_page.page)
        assert len(cart_page.get_items()) == 1, "Item should be in cart"
        
        # Go back to inventory
        cart_page.continue_shopping()
        inventory_page = InventoryPage(inventory_page.page)
        
        # Verify cart count is still correct
        assert inventory_page.get_cart_count() == 1, \
            "Cart count should persist after navigating back to inventory"
    
    def test_cart_badge_updates(self, inventory_page: InventoryPage):
        """Test that cart badge updates correctly when adding/removing items."""
        test_data = load_test_data()
        item1 = test_data["products"]["backpack"]
        item2 = test_data["products"]["bike_light"]
        
        # Initially cart should be empty (badge not visible)
        assert inventory_page.get_cart_count() == 0, "Cart should start empty"
        
        # Add first item
        inventory_page.add_item_to_cart(item1)
        assert inventory_page.get_cart_count() == 1, "Badge should show 1"
        
        # Add second item
        inventory_page.add_item_to_cart(item2)
        assert inventory_page.get_cart_count() == 2, "Badge should show 2"
        
        # Remove one item
        inventory_page.remove_item_from_cart(item1)
        assert inventory_page.get_cart_count() == 1, "Badge should show 1 after removal"
        
        # Remove last item
        inventory_page.remove_item_from_cart(item2)
        assert inventory_page.get_cart_count() == 0, "Badge should not be visible when cart is empty"
    
    def test_cart_items_display_correctly(self, inventory_page: InventoryPage):
        """Test that cart items display with correct information."""
        test_data = load_test_data()
        item_name = test_data["products"]["onesie"]
        
        # Add item and open cart
        inventory_page.add_item_to_cart(item_name)
        inventory_page.open_cart()
        
        cart_page = CartPage(inventory_page.page)
        items = cart_page.get_items()
        
        # Verify item details
        assert len(items) == 1, "Cart should have one item"
        assert items[0]["name"] == item_name, f"Item name should be {item_name}"
        assert items[0]["quantity"] == "1", "Item quantity should be 1"
        assert "$" in items[0]["price"], "Item price should be displayed"
    
    def test_proceed_to_checkout_from_cart(self, inventory_page: InventoryPage):
        """Test proceeding to checkout from cart page."""
        test_data = load_test_data()
        item_name = test_data["products"]["red_tshirt"]
        
        # Add item and open cart
        inventory_page.add_item_to_cart(item_name)
        inventory_page.open_cart()
        
        cart_page = CartPage(inventory_page.page)
        
        # Proceed to checkout
        cart_page.proceed_to_checkout()
        
        # Verify navigation to checkout page
        expect(inventory_page.page).to_have_url("https://www.saucedemo.com/checkout-step-one.html")
