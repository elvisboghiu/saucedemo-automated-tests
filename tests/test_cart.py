"""
Test suite for SauceDemo shopping cart functionality.
Covers adding/removing items, cart persistence, and cart badge updates.
"""
import pytest
from playwright.sync_api import expect
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from utils.config import BASE_URL
from utils.helpers import load_test_data

BASE_URL_NO_SLASH = BASE_URL.rstrip("/")


@pytest.mark.cart
class TestCart:
    """Test cases for shopping cart functionality."""
    
    def test_cart_state_after_inventory_refresh(self, inventory_page: InventoryPage):
        """Cart badge should keep correct count after refreshing inventory page."""
        test_data = load_test_data()
        item1 = test_data["products"]["backpack"]
        item2 = test_data["products"]["bike_light"]

        inventory_page.add_item_to_cart(item1)
        inventory_page.add_item_to_cart(item2)
        assert inventory_page.get_cart_count() == 2, "Cart badge should show 2 items"

        # Refresh inventory and verify cart state is preserved
        inventory_page.page.reload()
        assert inventory_page.is_loaded(), "Inventory page should be loaded after refresh"
        assert inventory_page.get_cart_count() == 2, "Cart badge should still show 2 items after refresh"

    def test_inventory_loads_with_all_products(self, inventory_page: InventoryPage):
        """Inventory page should load all expected products."""
        assert inventory_page.is_loaded(), "Inventory page should be loaded"
        products = inventory_page.get_products()
        # Swag Labs has 6 products by default
        assert len(products) == 6, f"Expected 6 products, got {len(products)}"
        for product in products:
            assert product["name"], "Product name should not be empty"
            assert product["description"], "Product description should not be empty"
            assert "$" in product["price"], "Product price should contain currency symbol"

    def test_inventory_sorting_by_name_and_price(self, inventory_page: InventoryPage):
        """Verify inventory sorting options for name and price."""
        # Sort by Name (A→Z)
        inventory_page.sort_by("az")
        names_az = inventory_page.get_product_names()
        assert names_az == sorted(names_az), "Products should be sorted A→Z by name"

        # Sort by Name (Z→A)
        inventory_page.sort_by("za")
        names_za = inventory_page.get_product_names()
        assert names_za == sorted(names_za, reverse=True), "Products should be sorted Z→A by name"

        # Sort by Price (low→high)
        inventory_page.sort_by("lohi")
        prices_lohi = inventory_page.get_product_prices()
        assert prices_lohi == sorted(prices_lohi), "Products should be sorted low→high by price"

        # Sort by Price (high→low)
        inventory_page.sort_by("hilo")
        prices_hilo = inventory_page.get_product_prices()
        assert prices_hilo == sorted(prices_hilo, reverse=True), "Products should be sorted high→low by price"

    def test_cart_persists_after_page_refresh(self, inventory_page: InventoryPage):
        """Cart contents should persist after refreshing the cart page."""
        test_data = load_test_data()
        item_name = test_data["products"]["backpack"]

        inventory_page.add_item_to_cart(item_name)
        inventory_page.open_cart()
        cart_page = CartPage(inventory_page.page)
        expect(cart_page.cart_items).to_have_count(1)

        # Refresh the page and verify the item is still in the cart
        inventory_page.page.reload()
        cart_page = CartPage(inventory_page.page)
        expect(cart_page.cart_items).to_have_count(1)

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
        expect(cart_page.cart_items).to_have_count(1)
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
        expect(cart_page.cart_items).to_have_count(1)
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
        expect(cart_page.cart_items).to_have_count(1)
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
        expect(inventory_page.page).to_have_url(f"{BASE_URL_NO_SLASH}/checkout-step-one.html")

    def test_inventory_access_in_new_tab_after_login(self, inventory_page: InventoryPage):
        """Inventory should be accessible in a new tab after login."""
        page = inventory_page.page
        context = page.context

        new_page = context.new_page()
        new_page.goto(f"{BASE_URL_NO_SLASH}/inventory.html")

        new_inventory_page = InventoryPage(new_page)
        assert new_inventory_page.is_loaded(), "Inventory should load in new tab for logged-in user"
